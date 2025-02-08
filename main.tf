# terraform {
#   backend "gcs" {
#     bucket = "weather-api-tfstate"
#     prefix = "env/dev"
#   }
# }

# This Terraform won't create any Google Cloud resources, so additional 
# permissions are required for the service account
#
terraform {
  backend "gcs" {
    bucket = "weather-api-tfstate"
    prefix = "env/dev"
  }
}

variable "project" {}

# Cloud Run
resource "google_cloud_run_service" "weather-api" {
  name = "weather-api"
  location = "europe-west1"
  template {
    spec {
      containers {
        image = "europe-west1-docker.pkg.dev/${var.project}/cloud-run-containers/weather-api:latest"
      }
    }
  }
}