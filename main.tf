terraform {
  backend "gcs" {
    bucket = "weather-api-tfstate"
    prefix = "env/dev"
  }
}

variable "project" {}

resource "google_cloud_run_service" "weather-api" {
  name = "weather-api"
  location = "europe-west1"
  project = "${var.project}"
  template {
    spec {
      containers {
        image = "europe-west1-docker.pkg.dev/${var.project}/cloud-run-containers/weather-api:latest"
      }
    }
  }
}