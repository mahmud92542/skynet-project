# Networking outputs
output "network_name" {
  description = "VPC network name"
  value       = module.networking.network_name
}

output "subnet_name" {
  description = "Subnet name used by GKE"
  value       = module.networking.subnet_name
}

output "nat_router" {
  description = "Cloud NAT router name"
  value       = module.networking.nat_router
}

output "nat" {
  description = "Cloud NAT name"
  value       = module.networking.nat
}

# GKE outputs
output "cluster_name" {
  description = "GKE cluster name"
  value       = module.gke.cluster_name
}

output "node_pool_name" {
  description = "Node pool name"
  value       = module.gke.node_pool_name
}

output "cluster_endpoint" {
  description = "GKE API server endpoint"
  value       = module.gke.cluster_endpoint
}

output "cluster_location" {
  description = "GKE cluster location"
  value       = module.gke.cluster_location
}

# Artifact Registry
output "artifact_registry_url" {
  description = "Artifact Registry repository URL"
  value       = module.artifact_registry.repository_url
}