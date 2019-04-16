provider "google" {
  project = "test-000000"
  region  = "europe-west3"
  zone    = "europe-west3-b"
  credentials = "${file("testproject-000000-0c0b000b00c0.json")}"
}
locals {
  service_account_email="tester-monkeyZoo-user@testproject-000000.iam.gserviceaccount.com"
  monkeyzoo_project="guardicore-22050661"
}