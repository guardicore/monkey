provider "google" {
  project = "test-000000"
  region  = "europe-west3"
  zone    = "europe-west3-b"
  credentials = file("../gcp_keys/gcp_key.json")
}
locals {
  resource_prefix = ""
  service_account_email="tester-monkeyZoo-user@testproject-000000.iam.gserviceaccount.com"
  monkeyzoo_project="guardicore-22050661"
}
