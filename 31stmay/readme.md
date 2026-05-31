
# Kubernetes Basics with Minikube — A Hands-On Tutorial

This tutorial teaches you the core concepts of Kubernetes (k8s) **while you actually deploy nginx**. Each concept is explained in plain language and then immediately put into practice. By the end you'll understand pods, deployments, services, scaling, and the declarative YAML workflow — and you'll have a working nginx site running on your own machine.

**Time:** ~45 minutes · **Cost:** free · **Level:** beginner

---

## What is Kubernetes? (the 2-minute mental model)

Imagine you have an application that needs to run reliably: it should restart if it crashes, scale up when traffic spikes, and survive a machine dying. Doing all that by hand is painful.

**Kubernetes is an orchestrator** — you tell it the *desired state* ("I want 3 copies of nginx running"), and it constantly works to make reality match that. If a copy dies, it starts a new one. If you ask for more, it adds them. You describe the *what*, Kubernetes figures out the *how*.

The key shift in thinking: you stop running commands like "start this server" and instead **declare** what you want to exist. This is called the *declarative* model, and it's the heart of Kubernetes.

A few terms you'll meet, from biggest to smallest:

- **Cluster** — the whole system: a set of machines running your workloads.
- **Node** — a single machine (VM or physical) in the cluster. Minikube gives you one node.
- **Pod** — the smallest unit you deploy. It wraps one (or a few tightly-coupled) containers.
- **Deployment** — manages a set of identical pods, handles updates and self-healing.
- **Service** — a stable network address to reach your pods (pods come and go; services stay).

Don't worry if these are fuzzy now — we'll build each one up with hands-on steps.

---

## Prerequisites

You need three tools. If you already followed a minikube setup, skip ahead.

```bash
# 1. Docker (minikube uses it as the driver) — install from docker.com if needed
docker --version

# 2. kubectl — the command-line tool to talk to Kubernetes
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# 3. minikube — runs a single-node Kubernetes cluster locally
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

> **macOS users:** `brew install kubectl minikube` is the easy path.

---

## Part 1 — Start your cluster

### Concept: the cluster and control plane

When you start Kubernetes, you get a **control plane** (the brain that makes scheduling decisions and stores the desired state) and one or more **nodes** (where your containers actually run). Minikube packs all of this into a single node so you can learn without any cloud.

### Practice

```bash
minikube start
```

This downloads the Kubernetes components and boots your node (takes a few minutes the first time). When it finishes, check it:

```bash
kubectl get nodes
```

You should see one node with status `Ready`:

```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   1m    v1.30.x
```

**What just happened:** `kubectl` is your remote control. It sends your requests to the control plane's API. Every command you run from here is really "please make the cluster look like this."

Peek at what's already running under the hood:

```bash
kubectl get pods -A
```

The `-A` flag means "all namespaces." You'll see system pods (DNS, networking, etc.) that Kubernetes runs to manage itself.

---

## Part 2 — Your first Pod

### Concept: what a Pod is

A **Pod** is the smallest thing Kubernetes runs. It usually holds a single container (here, nginx). Pods are *ephemeral* — they can be killed and replaced at any time, and they get a new IP each time. That impermanence is why we almost never create bare pods in real life — but creating one once is the best way to *see* the concept.

### Practice

```bash
kubectl run my-nginx --image=nginx:latest
```

Check it:

```bash
kubectl get pods
```

```
NAME       READY   STATUS    RESTARTS   AGE
my-nginx   1/1     Running   0          20s
```

Inspect it in detail — this command is your best friend for debugging:

```bash
kubectl describe pod my-nginx
```

See its logs (nginx's startup output):

```bash
kubectl logs my-nginx
```

Prove there's a real nginx inside by jumping into the pod:

```bash
kubectl exec -it my-nginx -- /bin/bash
# inside the pod:
curl localhost
exit
```

You'll see nginx's welcome HTML. Now delete this pod — we're about to do it the right way:

```bash
kubectl delete pod my-nginx
```

**The limitation you just felt:** you had to create the pod manually, and if it crashed, nothing would bring it back. That's the problem Deployments solve.

---

## Part 3 — Deployments (the real way to run things)

### Concept: desired state and self-healing

A **Deployment** says "I always want N copies of this pod running." Kubernetes creates a **ReplicaSet** behind the scenes to enforce that count. If a pod dies, the ReplicaSet notices the gap and creates a replacement — automatically. This *self-healing* is the whole point of Kubernetes.

### Practice

```bash
kubectl create deployment nginx-deploy --image=nginx:latest
```

Look at what got created:

```bash
kubectl get deployments
kubectl get pods
```

Now **watch the magic of self-healing**. Find your pod's name, then delete it:

```bash
kubectl get pods
kubectl delete pod <paste-pod-name-here>
kubectl get pods
```

You'll see a *new* pod appear almost instantly. You declared "I want one nginx pod," so Kubernetes refuses to let that number drop. You never told it to recreate the pod — it just does, because the desired state says one must exist.

---

## Part 4 — Services (reaching your pods)

### Concept: a stable address

Pods get new IP addresses every time they're recreated, so you can never rely on a pod's IP. A **Service** is a stable, never-changing front door that automatically routes traffic to whichever pods are currently alive. It finds its pods using *labels* (tags attached to pods).

Common types:
- **ClusterIP** (default) — reachable only inside the cluster.
- **NodePort** — opens a port on the node so you can reach it from outside.
- **LoadBalancer** — provisions a cloud load balancer (used in EKS/GKE, not local).

### Practice

Expose your deployment with a NodePort service:

```bash
kubectl expose deployment nginx-deploy --type=NodePort --port=80
```

Check it:

```bash
kubectl get services
```

Now open it in your browser — minikube gives you a handy shortcut:

```bash
minikube service nginx-deploy
```

This opens nginx's welcome page in your browser. **You now have a real, network-accessible nginx running in Kubernetes.** Traffic flows: your browser → NodePort service → whichever nginx pod is alive.

---

## Part 5 — Scaling

### Concept: changing the desired count

Scaling is just telling the Deployment a new number. Kubernetes adds or removes pods to match. No restarts of the others, no manual work.

### Practice

```bash
kubectl scale deployment nginx-deploy --replicas=4
kubectl get pods
```

You'll watch four pods come up. Your single Service automatically load-balances across all of them. Scale back down whenever you like:

```bash
kubectl scale deployment nginx-deploy --replicas=2
```

---

## Part 6 — The declarative way (YAML)

### Concept: infrastructure as code

Everything above used *imperative* commands (`kubectl create`, `kubectl scale`) — great for learning, but in real projects you write the desired state in **YAML files** and check them into git. This makes your setup reproducible, reviewable, and version-controlled. This is how teams actually run Kubernetes.

### Practice

First, clean up the imperative resources so we can recreate them declaratively:

```bash
kubectl delete service nginx-deploy
kubectl delete deployment nginx-deploy
```

Create a file called `nginx.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx          # the Deployment manages pods with this label
  template:
    metadata:
      labels:
        app: nginx        # pods get stamped with this label
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: nginx            # routes to pods carrying this label
  ports:
    - port: 80
      targetPort: 80
```

Notice how the Service's `selector` matches the pods' `labels` — that label matching is the invisible thread connecting services to pods.

Apply the whole thing with one command:

```bash
kubectl apply -f nginx.yaml
```

Verify:

```bash
kubectl get all
minikube service nginx-service
```

The beauty: edit the file (say, change `replicas: 3` to `replicas: 5`), run `kubectl apply -f nginx.yaml` again, and Kubernetes reconciles the difference. Same command for create and update — you just describe the goal.

---

## Part 7 — The Dashboard (optional, visual)

Minikube ships a web UI to see everything graphically:

```bash
minikube dashboard
```

This opens a browser view of your pods, deployments, and services — useful for getting an intuition of how the pieces relate.

---

## Cleanup

When you're done practicing, tear it all down so nothing eats resources:

```bash
kubectl delete -f nginx.yaml      # removes what you applied
minikube stop                     # stops the cluster (keeps it for later)
# or, to delete everything entirely:
minikube delete
```

---

## Command cheat sheet

| Task | Command |
|------|---------|
| Start cluster | `minikube start` |
| List nodes | `kubectl get nodes` |
| List pods | `kubectl get pods` |
| List everything | `kubectl get all` |
| Inspect a resource | `kubectl describe pod <name>` |
| View logs | `kubectl logs <pod>` |
| Shell into a pod | `kubectl exec -it <pod> -- /bin/bash` |
| Apply a YAML file | `kubectl apply -f file.yaml` |
| Scale a deployment | `kubectl scale deployment <name> --replicas=N` |
| Delete a resource | `kubectl delete <type> <name>` |
| Open a service | `minikube service <name>` |
| Stop cluster | `minikube stop` |

---

## Concept glossary

- **Cluster** — the entire Kubernetes system (control plane + nodes).
- **Node** — a worker machine where pods run.
- **Pod** — smallest deployable unit; wraps your container(s). Ephemeral.
- **ReplicaSet** — keeps a specified number of identical pods alive.
- **Deployment** — manages ReplicaSets; handles self-healing and rolling updates.
- **Service** — stable network endpoint that routes to pods via labels.
- **Label** — a key/value tag on objects; how services find their pods.
- **Namespace** — a way to partition a cluster into virtual sub-clusters.
- **Manifest** — a YAML file describing desired state.
- **Declarative model** — you describe the goal; Kubernetes makes it happen.

---

## Where to go next

You've learned the foundation that transfers to *any* Kubernetes — including managed clouds like EKS, GKE, and AKS. Natural next topics:

1. **ConfigMaps & Secrets** — inject configuration and credentials into pods.
2. **Persistent Volumes** — give pods storage that survives restarts.
3. **Ingress** — route HTTP traffic by hostname/path (try `minikube addons enable ingress`).
4. **Rolling updates & rollbacks** — `kubectl set image` and `kubectl rollout undo`.
5. **Helm** — package manager for Kubernetes apps.

The same `kubectl` skills you practiced here are exactly what you'll use on a real cloud cluster — only the underlying nodes change.
