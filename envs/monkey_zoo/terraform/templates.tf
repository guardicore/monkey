
resource "google_compute_instance_template" "windows2012" {
  name        = "${local.resource_prefix}windows2012"
  description = "Creates windows 2012 core servers at europe-west3-a."

  tags = ["test-machine", "windowsserver2012", "windows"]

  machine_type   = "n1-standard-1"
  can_ip_forward = false

  disk {
    source_image = "windows-cloud/windows-2012-r2"
  }
  network_interface {
    subnetwork = "monkeyzoo-main"
    access_config {

    }
  }
  service_account = local.service_account
}

resource "google_compute_instance_template" "windows2016" {
  name        = "${local.resource_prefix}windows2016"
  description = "Creates windows 2016 core servers at europe-west3-a."

  tags = ["test-machine", "windowsserver2016", "windows"]

  machine_type   = "n1-standard-1"
  can_ip_forward = false

  disk {
    source_image = "windows-cloud/windows-2016"
  }
  network_interface {
    subnetwork = "monkeyzoo-main"
    access_config {

    }
  }
  service_account = local.service_account
}
