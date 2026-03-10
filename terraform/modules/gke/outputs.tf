output "cluster_name"      { value = google_container_cluster.gke_cluster.name }
output "node_pool_name"    { value = google_container_node_pool.primary_nodes.name }
output "cluster_endpoint"  { value = google_container_cluster.gke_cluster.endpoint }
output "cluster_location"  { value = google_container_cluster.gke_cluster.location }