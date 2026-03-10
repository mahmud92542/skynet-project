output "network_name" { value = google_compute_network.vpc.name }
output "subnet_name"  { value = google_compute_subnetwork.subnet.name }
output "nat_router"   { value = google_compute_router.nat_router.name }
output "nat"          { value = google_compute_router_nat.nat.name }