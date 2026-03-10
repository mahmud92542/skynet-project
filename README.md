# SRE Platform Deployment – GKE Observability Stack

This repository contains infrastructure and application code to deploy a small production-style platform on Google Cloud using Terraform and Kubernetes.

The platform includes:

- Infrastructure provisioning with Terraform
- A containerized HTTP service
- Deployment to Google Kubernetes Engine (GKE)
- Observability stack with Prometheus, Grafana, and Loki
- Logging, metrics, and dashboards

The goal of this project is to demonstrate infrastructure automation, container deployment, and observability practices.

---

# Repository Structure

.
├── terraform/ # Infrastructure as Code (Terraform modules)
├── app/ # HTTP application source code + Dockerfile
├── k8s/ # Kubernetes manifests
├── observability/ # Monitoring stack (Prometheus, Grafana, Loki)
└── README.md


### terraform/

Contains all infrastructure code written with **Terraform**.

Modules include:

- networking (VPC, subnet, NAT)
- gke (GKE cluster + node pool)
- artifact_registry (Docker image registry)

Files:

```
terraform/
├── modules/
│   ├── networking/
│   ├── gke/
│   └── artifact_registry/
├── main.tf
├── variables.tf
├── outputs.tf
├── backend.tf
└── terraform.tfvars.example
```

Remote state is stored in a **Google Cloud Storage (GCS)** backend.

---

### app/

Contains the application source code and Dockerfile.

The application is a simple HTTP service that:

- exposes `/hello`
- exposes `/metrics`
- logs request metadata including `trace_id`
- supports Prometheus scraping

Example endpoints:

```
GET /hello
GET /metrics
```

---

### k8s/

Contains Kubernetes manifests used to deploy the application.

Resources include:

- Deployment
- Service
- ServiceAccount
- RBAC

---

### observability/

Contains configuration for the observability stack:

- Prometheus (metrics collection)
- Grafana (dashboards)
- Loki (log aggregation)
- Promtail (log shipping)

---

# Prerequisites

Install the following tools:

- Terraform
- gcloud CLI
- kubectl
- Docker
- Helm

You must also have a Google Cloud project with billing enabled.

---

# Infrastructure Setup

Initialize Terraform:

```bash
cd terraform
terraform init
```

Create a variables file:

```bash
cp terraform.tfvars.example terraform.tfvars
```

Update values in `terraform.tfvars`:

```
project_id = "your-gcp-project-id"
region     = "us-central1"
```

Apply infrastructure:

```bash
terraform apply
```

This will create:

- VPC
- Subnet
- Cloud NAT
- GKE cluster
- Artifact Registry repository

---

# Connect to the Cluster

After Terraform finishes:

```bash
gcloud container clusters get-credentials platform-cluster \
  --region us-central1 \
  --project <your-project-id>
```

Verify cluster access:

```bash
kubectl get nodes
```

---

# Build and Push the Application Image

Navigate to the app directory:

```bash
cd app
```

Build the Docker image:

```bash
docker build -t us-central1-docker.pkg.dev/<PROJECT_ID>/app-repo/hello-service:latest .
```

Authenticate Docker:

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

Push the image:

```bash
docker push us-central1-docker.pkg.dev/<PROJECT_ID>/app-repo/hello-service:latest
```

---

# Deploy Application to Kubernetes

Apply manifests:

```bash
kubectl apply -f k8s/
```

Verify deployment:

```bash
kubectl get pods
```

Test service:

```bash
kubectl port-forward svc/hello-service 8080:80
```

Open:

```
http://localhost:8080/hello
```

---

# Deploy Observability Stack

Install monitoring components with Helm.

Add Helm repositories:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

Install Loki:

```bash
helm upgrade --install loki grafana/loki \
  --namespace monitoring \
  --create-namespace \
  --set deploymentMode=SingleBinary \
  --set loki.auth_enabled=false \
  --set loki.storage.type=filesystem
```

Install Promtail:

```bash
helm upgrade --install promtail grafana/promtail \
  --namespace monitoring \
  --set "config.clients[0].url=http://loki.monitoring.svc.cluster.local:3100/loki/api/v1/push"
```

Install Prometheus + Grafana:

```bash
helm upgrade --install prometheus grafana/k8s-monitoring \
  --namespace monitoring
```

---

# Verify Observability Stack

Check pods:

```bash
kubectl get pods -n monitoring
```

Access Grafana:

```bash
kubectl port-forward svc/grafana -n monitoring 3000:80
```

Open:

```
http://localhost:3000
```

Default credentials:

```
admin / admin
```

Verify:

- Metrics visible from Prometheus
- Logs visible in Loki
- Application dashboard in Grafana

---

# Architecture Decisions

### 1. Terraform Modules

Infrastructure components were separated into modules (networking, gke, artifact registry) to improve reusability and maintainability.

### 2. GCS Backend for Terraform State

Terraform remote state is stored in a GCS bucket to enable safe state management and prevent local state conflicts.

### 3. Loki for Log Aggregation

Loki was chosen instead of Elasticsearch because it integrates natively with Grafana and has significantly lower resource overhead.

### 4. Helm for Observability Stack

Helm was used to install monitoring components to simplify deployment and configuration management.

---

# Estimated GCP Cost (24 hours)

Approximate cost for running this stack for 24 hours in `us-central1`.

| Resource | Estimated Cost |
|--------|--------|
| GKE control plane | $0.10/hour |
| 1 × e2-medium node | ~$0.033/hour |
| Persistent storage | ~$0.02 |
| Networking/NAT | ~$0.02 |

Estimated total:

**~$1.20 – $1.50 per day**

Costs may vary depending on usage and region.

---

# Cleanup

Destroy infrastructure:

```bash
terraform destroy
```

---

# Summary

This project demonstrates:

- Infrastructure automation with Terraform
- Containerized application deployment
- Kubernetes workload management
- Monitoring with Prometheus and Grafana
- Centralized logging with Loki

The platform provides a reproducible environment for deploying and monitoring containerized applications in Google Cloud.
