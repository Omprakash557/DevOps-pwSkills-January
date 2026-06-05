# Helm Charts on AWS EKS — A Q&A Tutorial

A step-by-step, question-driven guide to deploying applications on Amazon EKS with Helm. We deploy a small app **twice** — first with raw `kubectl`, then with Helm — so the advantages are concrete rather than theoretical.

> **Note on versions:** Helm 4 is the current stable release (v4.1.4 / v4.2.0 as of mid-2026), and Helm 3 is now in bug-fixes-only support mode. Chart syntax and the core commands (`create`, `install`, `upgrade`, `rollback`) are essentially unchanged, so this tutorial works on either. Helm 4's headline improvement is server-side apply, which removes a class of merge conflicts that used to affect Helm 3.

---

## Q1. What exactly are we building?

A simple nginx-based web app with a **configurable replica count and environment setting**, deployed to an EKS cluster.

The plan:

1. Deploy it the "hard way" with raw Kubernetes manifests — to feel the pain.
2. Convert it into a Helm chart.
3. Show off templated reuse, upgrades, rollbacks, and per-environment configuration.

---

## Q2. What do I need installed before starting?

Four CLI tools, plus AWS credentials.

```bash
# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscli.zip
unzip awscli.zip && sudo ./aws/install

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# eksctl (easiest way to create a cluster)
curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz"
tar -xzf eksctl_Linux_amd64.tar.gz && sudo mv eksctl /usr/local/bin

# Helm 4
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version    # confirm v4.x
```

Then run `aws configure` and supply an access key with EKS, EC2, and IAM permissions.

> ⚠️ **Cost warning:** An EKS cluster costs ~$0.10/hour for the control plane plus EC2 node costs. Run the cleanup step (Q12) so you aren't billed for an idle cluster.

---

## Q3. How do I create the EKS cluster?

One `eksctl` command provisions the control plane, a node group, the VPC, and updates your kubeconfig. It takes 15–20 minutes.

```bash
eksctl create cluster \
  --name helm-demo \
  --region us-east-1 \
  --nodes 2 \
  --node-type t3.small \
  --managed
```

Verify connectivity when it finishes:

```bash
kubectl get nodes
# NAME                          STATUS   ROLES    AGE   VERSION
# ip-192-168-x-x.ec2.internal   Ready    <none>   2m    v1.3x
```

---

## Q4. Why deploy without Helm first?

Because the pain is the whole point. Deploying with raw manifests first makes Helm's value obvious. Create a folder and two files:

```bash
mkdir raw-deploy && cd raw-deploy
```

**`deployment.yaml`:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
        - name: webapp
          image: nginx:1.27
          ports:
            - containerPort: 80
          env:
            - name: ENVIRONMENT
              value: "development"
```

**`service.yaml`:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp
spec:
  type: LoadBalancer
  selector:
    app: webapp
  ports:
    - port: 80
      targetPort: 80
```

Deploy it:

```bash
kubectl apply -f deployment.yaml -f service.yaml
kubectl get svc webapp   # wait for EXTERNAL-IP, then open it in a browser
```

---

## Q5. So where's the pain?

Suppose you now want a **staging** copy with 5 replicas and `ENVIRONMENT=staging`. Your only options are:

- Copy-paste both files into a new folder and hand-edit them, or
- Fire off `kubectl set` commands and lose track of what's actually deployed.

Multiply that across dev/staging/prod and a dozen microservices and you get copy-paste sprawl, no versioning, and no clean rollback. **That's the problem Helm solves.**

Clean up before moving on:

```bash
kubectl delete -f .
cd ..
```

---

## Q6. How do I create a Helm chart?

```bash
helm create webapp-chart
```

This scaffolds a full chart. The structure:

```
webapp-chart/
├── Chart.yaml          # chart metadata (name, version)
├── values.yaml         # default configuration values
├── charts/             # sub-chart dependencies
└── templates/          # templated manifests
    ├── deployment.yaml
    ├── service.yaml
    ├── _helpers.tpl    # reusable template snippets
    └── ...
```

The core idea: **`templates/` holds manifests with placeholders, and `values.yaml` fills them in.** One template, many configurations.

---

## Q7. How do I customize the chart?

Replace `webapp-chart/values.yaml` with something minimal and readable:

```yaml
replicaCount: 2

image:
  repository: nginx
  tag: "1.27"
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80

environment: development
```

Then point the template at those values. In `webapp-chart/templates/deployment.yaml`, the container spec references values like this:

```yaml
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: 80
          env:
            - name: ENVIRONMENT
              value: {{ .Values.environment | quote }}
```

Every `{{ .Values.x }}` is pulled from `values.yaml` at install time.

---

## Q8. Can I preview what gets deployed before touching the cluster?

Yes — and this is already an advantage. Render and validate locally:

```bash
helm template webapp-chart        # renders manifests to stdout, no cluster needed
helm lint webapp-chart            # catches syntax/structure errors
```

You see exactly what will hit the cluster before anything happens.

---

## Q9. How do I install the chart?

```bash
helm install dev-webapp ./webapp-chart
```

`dev-webapp` is the **release name** — a named, tracked instance of the chart. Check it:

```bash
helm list
kubectl get pods,svc
```

Same app as before, but now defined by one parameterized chart instead of hand-edited manifests.

---

## Q10. What can Helm do that raw `kubectl` can't?

This is the payoff. Each item below is awkward or impossible with raw manifests.

### Advantage 1 — One chart, many environments

Spin up a staging release from the *same* chart with different values — no file duplication:

```bash
helm install staging-webapp ./webapp-chart \
  --set replicaCount=5 \
  --set environment=staging
```

Or keep environment configs in version-controlled files (`values-staging.yaml`, `values-prod.yaml`):

```bash
helm install prod-webapp ./webapp-chart -f values-prod.yaml
```

### Advantage 2 — Clean upgrades

Change the image tag and roll it out as a tracked revision:

```bash
helm upgrade dev-webapp ./webapp-chart --set image.tag=1.28
helm history dev-webapp        # see every revision
```

### Advantage 3 — One-command rollback

The big one. If an upgrade misbehaves, revert instantly — no scrambling to remember the old config:

```bash
helm rollback dev-webapp 1     # roll back to revision 1
```

Doing this reliably with raw manifests means digging through git history and re-applying by hand.

### Advantage 4 — Atomic, all-or-nothing deploys

If any resource fails, the whole release fails cleanly instead of leaving you half-deployed:

```bash
helm upgrade dev-webapp ./webapp-chart --atomic --timeout 2m
```

### Advantage 5 — Reuse community charts

Install battle-tested charts instead of writing boilerplate:

```bash
helm install my-nginx oci://registry-1.docker.io/bitnamicharts/nginx
```

There are 15,000+ public charts on Artifact Hub (Postgres, Redis, Prometheus, and more), so you rarely write that yourself.

---

## Q11. What's the mental model for all this?

Raw `kubectl` is like editing config files by hand on every machine. Helm is a **package manager** — think `apt` or `npm` for Kubernetes.

| Concept | Meaning |
|---|---|
| **Chart** | A reusable, versioned template for an app |
| **Release** | One installed instance of a chart |
| **`values.yaml`** | How you configure each instance without touching the template |

The three things you genuinely can't replicate easily without Helm: **templated reuse**, **revision history**, and **one-command rollback**.

---

## Q12. How do I clean up so I'm not billed?

```bash
helm uninstall dev-webapp staging-webapp prod-webapp
eksctl delete cluster --name helm-demo --region us-east-1
```

The `eksctl delete` tears down the cluster, node group, and VPC.

---

## Q13. Where do I go next?

Production-shaped extensions to try:

- Build and push your own app image to **Amazon ECR** instead of using public nginx.
- Add an **Ingress** with the AWS Load Balancer Controller.
- Wire up a `values-prod.yaml` with **horizontal pod autoscaling** and health checks (liveness/readiness probes).
- Publish your chart to an **OCI registry** (ECR supports this natively) so others can `helm install` it.

---

*Reference: [helm.sh/docs](https://helm.sh/docs/) · [eksctl.io](https://eksctl.io/) · [Artifact Hub](https://artifacthub.io/)*
