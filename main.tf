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
    bucket = "PROJECT_ID-tfstate"
    prefix = "env/dev"
  }
}