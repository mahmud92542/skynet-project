# Networking module
module "networking" {
  source       = "../modules/networking"
  project_id   = var.project_id
  region       = var.region
  network_name = var.network_name
  subnet_name  = var.subnet_name
  subnet_cidr  = var.subnet_cidr
}

# Artifact Registry module
module "artifact_registry" {
  source          = "../modules/artifact_registry"
  project_id      = var.project_id
  region          = var.region
  repository_name = var.repository_name
}

# GKE module
module "gke" {
  source       = "../modules/gke"
  project_id   = var.project_id
  region       = var.region
  cluster_name = var.cluster_name

  network    = module.networking.network_name
  subnetwork = module.networking.subnet_name

  node_count   = var.node_count
  machine_type = var.machine_type
}
