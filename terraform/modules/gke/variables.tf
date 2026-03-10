variable "project_id" {}
variable "region" {}

variable "cluster_name" {
  default = "platform-cluster"
}

variable "network" {}
variable "subnetwork" {}

variable "machine_type" {
  default = "e2-medium"
}

variable "node_count" {
  default = 1
}