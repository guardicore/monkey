variable "project" {
  description = "The GCP project to deploy to"
  type        = string
  default     = "test-000000"
}

variable "region" {
  description = "The GCP region to deploy to"
  type        = string
  default     = "europe-west3"
}

variable "zone" {
  description = "The GCP zone to deploy to"
  type        = string
  default     = "europe-west3-b"
}

variable "service_account_email" {
  description = "The service account to use. Must have permissions to modify instances on the project"
  type        = string
}

variable "credentials_file" {
  description = "The file containing the GCP credentials to use. Must have permissions to use the service account"
}

provider "google" {
  project     = var.project
  region      = var.region
  zone        = var.zone
  credentials = var.credentials_file
}
locals {
  resource_prefix       = ""
  service_account_email = var.service_account_email
  monkeyzoo_project     = "guardicore-22050661"
}
