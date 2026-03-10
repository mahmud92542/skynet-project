terraform {
  backend "gcs" {
    bucket = "skynet-terraform-state-mahmud" 
    prefix = "terraform/state"
  }
}
