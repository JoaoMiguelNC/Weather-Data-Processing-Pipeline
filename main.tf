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

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.default.location
  project     = google_cloud_run_service.default.project
  service     = google_cloud_run_service.default.name

  policy_data = data.google_iam_policy.noauth.policy_data
}