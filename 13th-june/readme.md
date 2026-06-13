# EKS Autoscaling Tutorial: HPA + Karpenter (the easy way)

A hands-on, copy-paste tutorial that takes you from zero to a working EKS cluster that
scales **pods** with the Horizontal Pod Autoscaler (HPA) and **nodes** with Karpenter.

We use **`eksctl`** throughout because it is the shortest path: it creates the cluster,
sets up OIDC/IAM, installs Karpenter, and tags your subnets and security groups for you.

> **Tested against:** EKS 1.33, Karpenter v1.x (`NodePool` / `EC2NodeClass` API),
> eksctl, `us-east-1`. Karpenter moves fast — always check
> <https://github.com/aws/karpenter/releases> for the latest version and confirm it is
> compatible with your EKS Kubernetes version before pinning it below.

---

## What you'll build

```
                 ┌─────────────────────────────────────────┐
                 │              EKS Cluster                  │
                 │                                           │
  load ───────▶  │   Deployment ──HPA──▶ more pods           │
                 │        │                                  │
                 │        ▼                                  │
                 │   pending pods ──Karpenter──▶ new EC2 nodes│
                 └─────────────────────────────────────────┘
```

- **HPA** watches CPU and adds/removes *pod replicas*.
- **Karpenter** watches for *unschedulable (pending) pods* and adds/removes *nodes* to fit them.
- They work together: HPA scales pods up first, then Karpenter notices the pods can't fit and adds nodes.

---

## 0. Prerequisites

Install these four CLI tools and make sure your AWS credentials are configured.

```bash
# eksctl
curl --silent --location \
  "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" \
  | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# aws cli should already be installed; then:
aws configure          # set access key, secret, region, output
aws sts get-caller-identity   # confirm you're authenticated
```

Set a few variables you'll reuse:

```bash
export CLUSTER_NAME="demo-cluster"
export AWS_REGION="us-east-1"
export K8S_VERSION="1.33"
export KARPENTER_VERSION="1.3.3"   # check the releases page for the latest compatible version
```

---

## 1. Create the cluster (Karpenter installed automatically)

Instead of running many commands, describe the whole cluster in one config file. The
`karpenter:` block tells eksctl to install Karpenter, create its IAM role + service
account, and wire up the Spot interruption queue — all the fiddly parts done for you.

Create `cluster.yaml`:

```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: demo-cluster
  region: us-east-1
  version: "1.33"

iam:
  withOIDC: true            # required for Karpenter

karpenter:
  version: '1.3.3'          # keep in sync with $KARPENTER_VERSION
  createServiceAccount: true
  withSpotInterruptionQueue: true

# A small managed node group to run system pods + Karpenter itself.
# (Karpenter cannot provision the node it runs on, so it needs a home.)
managedNodeGroups:
  - name: core
    instanceType: t3.medium
    desiredCapacity: 2
    minSize: 1
    maxSize: 3
    volumeSize: 20
```

Launch it (takes ~15–20 minutes):

```bash
eksctl create cluster -f cluster.yaml
```

When it finishes, your kubeconfig is updated automatically. Verify:

```bash
kubectl get nodes
kubectl get pods -n kube-system | grep karpenter   # Karpenter controller should be Running
```

> eksctl also tags your subnets and security groups with
> `karpenter.sh/discovery: demo-cluster`, which is how Karpenter finds where to place
> nodes. Doing this by hand is the most common thing people get wrong — eksctl saves you here.

---

## Part A — Scale PODS with the Horizontal Pod Autoscaler (HPA)

### A1. Install metrics-server

HPA needs CPU/memory metrics, which EKS does not ship by default.

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# confirm it becomes available (give it ~30s)
kubectl get deployment metrics-server -n kube-system
kubectl top nodes
```

### A2. Deploy a sample app

A tiny PHP app that burns CPU when hit — perfect for triggering HPA.

```bash
kubectl create deployment php-apache --image=registry.k8s.io/hpa-example

# give it explicit CPU requests/limits (HPA scales on % of the request)
kubectl set resources deployment php-apache \
  --requests=cpu=200m --limits=cpu=500m

kubectl expose deployment php-apache --port=80
```

### A3. Create the HPA

Scale between 1 and 10 replicas, targeting 50% average CPU.

```bash
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
kubectl get hpa
```

### A4. Generate load and watch it scale

Open **two terminals**.

Terminal 1 — watch the HPA and pods react:

```bash
kubectl get hpa php-apache --watch
```

Terminal 2 — hammer the service from a temporary pod:

```bash
kubectl run -it --rm load-generator --image=busybox:1.28 --restart=Never -- \
  /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```

Within a minute or two you'll see CPU climb past 50% and the replica count rise:

```bash
kubectl get pods -l app=php-apache    # watch new pods appear
```

Stop the load (Ctrl-C in terminal 2). After the cooldown window (a few minutes) the HPA
scales the deployment back down. **That's pod-level autoscaling.**

---

## Part B — Scale NODES with Karpenter

Karpenter is already installed (Step 1). Now you give it two things:

- an **EC2NodeClass** = the AWS-specific "how" (AMI, IAM role, which subnets/SGs).
- a **NodePool** = the Kubernetes-facing "what" (allowed instance types, limits, disruption rules).

### B1. Create the EC2NodeClass and NodePool

eksctl created a node IAM role named like `eksctl-KarpenterNodeRole-demo-cluster`.
Confirm the exact name, then plug it in below:

```bash
aws iam list-roles --query "Roles[?contains(RoleName,'Karpenter')].RoleName" --output text
```

Apply the config (replace the role name if yours differs):

```bash
cat <<EOF | kubectl apply -f -
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiFamily: AL2023
  amiSelectorTerms:
    - alias: al2023@latest
  role: "KarpenterNodeRole-demo-cluster"     # <-- match the role from the command above
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: "demo-cluster"
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: "demo-cluster"
---
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]   # prefers cheaper Spot, falls back to On-Demand
        - key: node.kubernetes.io/instance-type
          operator: In
          values: ["t3.medium", "t3.large", "c5.large", "c5.xlarge"]
  # Stop runaway scaling: cap total resources this pool can launch.
  limits:
    cpu: "100"
  # Consolidate (replace/remove underutilized nodes) when they're empty or cheaper options exist.
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 30s
EOF
```

Confirm both are ready:

```bash
kubectl get ec2nodeclass    # READY should be True
kubectl get nodepool        # READY should be True
```

> If `ec2nodeclass` is not Ready, it's almost always a tag mismatch (subnets/SGs not
> tagged with `karpenter.sh/discovery: demo-cluster`) or a wrong IAM role name.

### B2. Force pods to go pending so Karpenter reacts

Deploy something that asks for more CPU than your tiny `core` nodes can give, then scale
it up. The pods will go **Pending**, and Karpenter will launch right-sized nodes for them.

```bash
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: inflate
spec:
  replicas: 0
  selector:
    matchLabels: { app: inflate }
  template:
    metadata:
      labels: { app: inflate }
    spec:
      terminationGracePeriodSeconds: 0
      containers:
        - name: inflate
          image: public.ecr.aws/eks-distro/kubernetes/pause:3.7
          resources:
            requests:
              cpu: "1"      # 1 full core per pod
EOF
```

Watch nodes in one terminal:

```bash
kubectl get nodes -L karpenter.sh/nodepool --watch
```

Scale up in another:

```bash
kubectl scale deployment inflate --replicas=8
```

Within ~30–60 seconds you should see Karpenter create a `NodeClaim`, launch a new EC2
instance, and join it to the cluster:

```bash
kubectl get nodeclaims
kubectl logs -f -n kube-system -l app.kubernetes.io/name=karpenter   # watch the decisions
```

### B3. Watch it scale back down (consolidation)

Scale the workload to zero:

```bash
kubectl scale deployment inflate --replicas=0
```

After `consolidateAfter` (30s) plus a short drain, Karpenter terminates the now-empty
nodes it created. Confirm:

```bash
kubectl get nodes -L karpenter.sh/nodepool   # Karpenter-created nodes disappear
```

**That's node-level autoscaling.**

---

## Putting it together

In a real workload you run **both** at once: HPA adds pods as load rises, and the moment
those extra pods can't fit on existing nodes, Karpenter adds nodes. As load falls, HPA
removes pods and Karpenter consolidates the freed-up nodes. You get application elasticity
and cost-efficient infrastructure without managing node groups by hand.

---

## Cleanup (avoid surprise bills!)

Delete in this order so Karpenter's nodes are gone before the cluster:

```bash
kubectl delete deployment inflate php-apache
kubectl delete nodepool default
kubectl delete ec2nodeclass default

# wait until all karpenter-created nodes are gone
kubectl get nodes

# then tear down everything eksctl made (cluster, node group, IAM, VPC)
eksctl delete cluster --name "$CLUSTER_NAME" --region "$AWS_REGION"
```

---

## Quick troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| HPA shows `<unknown>` for CPU | metrics-server not ready, or no CPU `requests` set | `kubectl get deploy metrics-server -n kube-system`; ensure the deployment has CPU requests |
| Pods stay `Pending`, no new node | EC2NodeClass not Ready | check subnet/SG `karpenter.sh/discovery` tags and the IAM role name |
| Nodes never scale down | workload still has pods, or PDBs block it | scale workload to 0; check `kubectl get pdb -A` |
| `NodePool`/`Provisioner` errors | using old v0.x API | use `NodePool` + `EC2NodeClass` (v1), not `Provisioner`/`AWSNodeTemplate` |
| Karpenter version incompatible | version newer/older than EKS supports | match `KARPENTER_VERSION` to your EKS version per the compatibility matrix |
