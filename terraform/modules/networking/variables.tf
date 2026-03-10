variable "project_id" {}
variable "region" {}

variable "network_name" {
  default = "platform-vpc"
}

variable "subnet_name" {
  default = "gke-subnet"
}

variable "subnet_cidr" {
  default = "10.0.0.0/24"
}