resource "google_compute_instance_template" "ubuntu16" {
  name        = "${local.resource_prefix}ubuntu16"
  description = "Creates ubuntu 16.04 LTS servers at europe-west3-a."

  tags = ["test-machine", "ubuntu16", "linux"]

  machine_type         = "n1-standard-1"
  can_ip_forward       = false

  disk {
    source_image = "ubuntu-os-cloud/ubuntu-1604-lts"
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    access_config {
      // Cheaper, non-premium routing
      network_tier = "STANDARD"
    }
  }
  service_account {
    email =local.service_account_email
    scopes=["cloud-platform"]
  }
}

resource "google_compute_instance_template" "windows2016" {
  name        = "${local.resource_prefix}windows2016"
  description = "Creates windows 2016 core servers at europe-west3-a."

  tags = ["test-machine", "windowsserver2016", "windows"]

  machine_type         = "n1-standard-1"
  can_ip_forward       = false

  disk {
    source_image = "windows-cloud/windows-2016"
  }
  network_interface {
    subnetwork="monkeyzoo-main"
  }
  service_account {
    email=local.service_account_email
    scopes=["cloud-platform"]
  }
}
