project_id = "skynet-2026-code-test-mahmud"
region = "us-central1"

# Networking
network_name = "platform-vpc"
subnet_name = "gke-subnet"
subnet_cidr = "10.0.0.0/24"

# GKE
cluster_name = "platform-cluster"
node_count = 1
machine_type = "e2-medium"

# Artifact Registry
repository_name = "app-repo"