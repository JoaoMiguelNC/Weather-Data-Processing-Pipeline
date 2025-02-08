terraform {
  backend "gcs" {
    bucket = "weather-api-tfstate"
    prefix = "env/dev"
  }
}

variable "project" {}

resource "google_cloud_run_v2_service" "weather-api" {
  name = "weather-api"
  location = "europe-west1"
  project = "${var.project}"
  deletion_protection=false
  template {
  containers {
    image = "europe-west1-docker.pkg.dev/${var.project}/cloud-run-containers/weather-api:latest"
    env {
        name = "WEATHER_KEY"
        value_source {
            secret_key_ref {
                secret  = "open-weather-map-key"
                version = "latest"
            }
        }
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

# resource "google_cloud_run_service_iam_policy" "noauth" {
#   location    = google_cloud_run_v2_service.weather-api.location
#   project     = google_cloud_run_v2_service.weather-api.project
#   service     = google_cloud_run_v2_service.weather-api.name

#   policy_data = data.google_iam_policy.noauth.policy_data
# }