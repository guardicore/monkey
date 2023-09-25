variable "project" {
  description = "The GCP project to deploy to"
  type        = string
  default     = "test-000000"
}

variable "region" {
  description = "The GCP region to deploy to"
  type        = string
  default     = "europe-west1"
}

variable "main_zone" {
  description = "The GCP zone for machines on the .2 subnet"
  type        = string
  default     = "europe-west1-a"
}

variable "main1_zone" {
  description = "The GCP zone for machines on the .3 subnet"
  type        = string
  default     = "europe-west1-b"
}

variable "tunneling_zone" {
  description = "The GCP zone for tunneling machines"
  type        = string
  default     = "europe-west1-a"
}

variable "credentials_reuse_zone" {
  description = "The GCP zone for credentials reuse machines"
  type        = string
  default     = "europe-west1-b"
}

variable "service_account_email" {
  description = "The service account to impersonate. The account must have permissions to modify instances on the project, and the account associated with the `credentials_file` must have permissions to impersonate this account"
  type        = string
  default     = ""
}

variable "credentials_file" {
  description = "The file containing the GCP credentials to use. Must have permissions to use the service account"
}

provider "google" {
  project                     = var.project
  region                      = var.region
  zone                        = var.main_zone
  credentials                 = var.credentials_file
  impersonate_service_account = var.service_account_email == "" ? null : var.service_account_email
}
locals {
  resource_prefix        = ""
  monkeyzoo_project      = "guardicore-22050661"
  main_zone              = var.main_zone
  main1_zone             = var.main1_zone
  tunneling_zone         = var.tunneling_zone
  credentials_reuse_zone = var.credentials_reuse_zone
}
