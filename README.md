# SRE Platform Deployment – GKE Observability Stack

This repository contains infrastructure and application code to deploy a small production-style platform on Google Cloud using Terraform and Kubernetes.

The platform includes:

- Infrastructure provisioning with Terraform
- A containerized HTTP service
- Deployment to Google Kubernetes Engine (GKE)
- Observability stack with Prometheus, Grafana, Loki, Promtail, and Kubecost
- Logging, metrics, dashboards, and cost monitoring

The goal of this project is to demonstrate infrastructure automation, container deployment, and observability practices.

---

# Repository Structure

```

.
├── terraform/
│   ├── modules/
│   │   ├── networking/
│   │   ├── gke/
│   │   └── artifact_registry/
│   │
│   └── env/
│       └── dev/
│           ├── main.tf
│           ├── variables.tf
│           ├── outputs.tf
│           ├── backend.tf
│           └── terraform.tfvars.example
│
├── app/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── k8s/
│   └── app-deployment.yaml
│
├── observability/
│   ├── grafana.yml
|   ├── prometheus-rbac.yml
|   ├── prometheus.yml
│   ├── loki/
│   ├── promtail/
│   └── cost-analyzer/
│
└── README.md

```

---

# Application

The application is a simple HTTP service exposing three endpoints:

| Endpoint | Description |
|--------|--------|
| `/hello` | returns HTTP 200 includes the Pod name, current timestamp, trace_id, etc |
| `/health` | returns HTTP 200 with a JSON body { "status": "ok" } |
| `/metrics` | Prometheus metrics endpoint |

The `/metrics` endpoint allows Prometheus to scrape application metrics.

---

# Prerequisites

Install the following tools:

- Terraform
- gcloud CLI
- kubectl
- Docker
- Helm

---

# Infrastructure Setup

Terraform is organized by environment.

Navigate to the development environment:

```

cd terraform/env/dev

```

Initialize Terraform:

```

terraform init

```

Preview infrastructure changes:

```

terraform plan

```

Apply infrastructure:

```

terraform apply

```

This will provision:

- VPC network
- Subnet
- Cloud NAT
- GKE cluster
- Artifact Registry repository

---

# Connect to the Cluster

After Terraform completes:

```

gcloud container clusters get-credentials platform-cluster 
--region us-central1 
--project <PROJECT_ID>

```

Verify cluster access:

```

kubectl get nodes

```

---

# Build and Push Application Image

Navigate to the application directory:

```

cd app

```

Authenticate Docker with Artifact Registry:

```

gcloud auth configure-docker us-central1-docker.pkg.dev

```

Build and push the multi-architecture image:

```

docker buildx build 
--platform linux/amd64,linux/arm64 
-t us-central1-docker.pkg.dev/<PROJECT_ID>/app-repo/hello-service:1.7 
--push .

```

---

# Deploy Application to Kubernetes

Apply Kubernetes manifests:

```

kubectl apply -f k8s/

```

Verify deployment:

```

kubectl get pods

```

Test the service:

```

kubectl port-forward svc/hello-service 8080:80

```

Test endpoints:

```

http://localhost:8080/hello
http://localhost:8080/health
http://localhost:8080/metrics

```

---

# Deploy Observability Stack

The observability stack is installed using Helm with custom values files located inside the `observability/` & their perspective directory.

---

# Install Loki

```
cd observability/
helm upgrade --install loki grafana/loki 
--namespace monitoring 
-f observability/loki/loki-values.yaml

```

---

# Install Promtail

```

helm upgrade --install promtail grafana/promtail 
--namespace monitoring 
-f observability/promtail/promtail-values.yaml

```

---

# Install Prometheus

```

kubectl apply -f prometheus.yaml
kubectl apply -f prometheus-rbac.yaml

```

---

# Install Grafana

```

kubectl apply -f grafana.yml

```

---

# Install Kubecost

```

helm upgrade --install kubecost kubecost/cost-analyzer 
--namespace kubecost 
--create-namespace 
-f observability/kubecost/kubecost-values.yaml

```

---

# Access Observability Tools

Most services can be accessed using port forwarding.

General command:

```

kubectl port-forward -n <namespace> svc/<service-name> <local-port>:<service-port>

```

Example for Grafana:

```

kubectl port-forward -n monitoring svc/grafana 3000:80

```

Open in browser:

```

http://localhost:3000

```

---

# Access Kubecost

Kubecost uses a deployment instead of a service:

```

kubectl port-forward -n kubecost deployment/kubecost-cost-analyzer 9091:9090

```

Open:

```

http://localhost:9091

```

Kubecost provides cost insights and resource utilization for the Kubernetes cluster.

---

# Cost Monitoring

Cluster costs can be monitored directly inside Kubecost.

Kubecost analyzes:

- Node usage
- Pod resource consumption
- Namespace costs
- Estimated monthly cloud cost

This provides a more accurate estimate than static cost calculations.

---

# Architecture Decisions

### 1. Terraform Modules

Infrastructure components are organized into reusable Terraform modules:

- networking
- gke
- artifact_registry

This improves maintainability and scalability.

### 2. GCS Backend for Terraform State

Terraform state is stored remotely in Google Cloud Storage to prevent state conflicts and enable team collaboration.

### 3. Loki for Log Aggregation

Loki was selected instead of Elasticsearch because it integrates natively with Grafana and has significantly lower operational overhead.

### 4. Helm for Observability Stack

Helm simplifies installation and configuration of monitoring tools in Kubernetes.

### 5. Kubecost for Cost Visibility

Kubecost provides real-time insights into Kubernetes infrastructure costs and resource utilization.

---

# Estimated GCP Cost (24 hours)

Approximate cost for running this stack in `us-central1`.

| Resource | Estimated Cost |
|--------|--------|
| GKE control plane | ~$2.40 |
| e2-medium node | ~$0.80 |
| Networking / NAT | ~$0.20 |

Estimated total:

**~$3 – $4 per day**

Kubecost provides more accurate real-time cost tracking.

---

# Cleanup

To remove all infrastructure:

```

cd terraform/env/dev
terraform destroy

```

---

# Summary

This project demonstrates:

- Infrastructure automation using Terraform
- Containerized application deployment
- Kubernetes workload management
- Metrics monitoring with Prometheus
- Log aggregation with Loki
- Visualization with Grafana
- Kubernetes cost monitoring using Kubecost

The platform provides a reproducible environment for deploying and monitoring containerized applications on Google Cloud.
