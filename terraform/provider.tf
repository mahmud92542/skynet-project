provider "google-beta" {
  project = var.project_id
  region  = var.region
  default_labels = ({
    environment = "dev"
    owner       = "mahmud-sre-interviewee"
  })
}