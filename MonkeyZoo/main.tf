
// Local variables
locals {
  default_ubuntu="${google_compute_instance_template.ubuntu16.self_link}"
  default_windows="${google_compute_instance_template.windows2016.self_link}"
}

variable "region" {
  default="europe-west3"
}

variable "zone" {
  default="europe-west3-b"
}

resource "google_compute_network" "monkeyzoo" {
  name                    = "monkeyzoo"
  auto_create_subnetworks = false
}

resource "google_compute_network" "tunneling" {
  name                    = "tunneling"
  auto_create_subnetworks = false
}

resource "google_compute_firewall" "monkeyzoo-in" {
  name    = "monkeyzoo-in"
  network = "${google_compute_network.monkeyzoo.name}"

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "65534"
  source_ranges = ["10.2.2.0/24"]
}

resource "google_compute_firewall" "monkeyzoo-out" {
  name    = "monkeyzoo-out"
  network = "${google_compute_network.monkeyzoo.name}"

  allow {
    protocol = "all"
  }

  direction = "EGRESS"
  priority = "65534"
  destination_ranges = ["10.2.2.0/24"]
}

resource "google_compute_firewall" "tunneling-in" {
  name    = "tunneling-in"
  network = "${google_compute_network.tunneling.name}"

  allow {
    protocol = "all"
  }

  direction = "INGRESS"

  source_ranges = ["10.2.1.0/28"]
}

resource "google_compute_firewall" "tunneling-out" {
  name    = "tunneling-out"
  network = "${google_compute_network.tunneling.name}"

  allow {
    protocol = "all"
  }

  direction = "EGRESS"

  destination_ranges = ["10.2.1.0/28"]
}

resource "google_compute_subnetwork" "monkeyzoo-main" {
  name            = "monkeyzoo-main"
  ip_cidr_range   = "10.2.2.0/24"
  region          = "europe-west3"
  network         = "${google_compute_network.monkeyzoo.self_link}"
}

resource "google_compute_subnetwork" "tunneling-main" {
  name            = "tunneling-main"
  ip_cidr_range   = "10.2.1.0/28"
  region          = "europe-west3"
  network         = "${google_compute_network.tunneling.self_link}"
}

resource "google_compute_instance_template" "ubuntu16" {
  name        = "ubuntu16"
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
    email ="${local.service_account_email}"
    scopes=["cloud-platform"]
  }
}

resource "google_compute_instance_template" "windows2016" {
  name        = "windows2016"
  description = "Creates windows 2016 core servers at europe-west3-a."

  tags = ["test-machine", "windows2016core", "windows"]

  machine_type         = "n1-standard-1"
  can_ip_forward       = false

  disk {
    source_image = "windows-cloud/windows-2016"
  }
  network_interface {
    subnetwork="monkeyzoo-main"
  }
  service_account {
    email="${local.service_account_email}"
    scopes=["cloud-platform"]
  }
}

resource "google_compute_instance_from_template" "hadoop-2" {
  name         = "hadoop-2"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.hadoop-2.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.2"
  }
}
resource "google_compute_instance_from_template" "hadoop-3" {
  name         = "hadoop-3"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.hadoop-3.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.3"
  }
}
resource "google_compute_instance_from_template" "elastic-4" {
  name         = "elastic-4"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.elastic-4.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.4"
  }
}
resource "google_compute_instance_from_template" "elastic-5" {
  name         = "elastic-5"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.elastic-5.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.5"
  }
}
/*
resource "google_compute_instance_from_template" "sambacry-6" {
  name         = "sambacry-6"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.sambacry-6.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.6"
  }
}
*/
/* WE NEED COSTOM 32-BIT UBUNTU FOR THIS MACHINE
resource "google_compute_instance_from_template" "sambacry-7" {
  name         = "sambacry-7"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk {
    initialize_params {
      // Add custom image to cloud
      image = "ubuntu32"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.7"
  }
}
*/
resource "google_compute_instance_from_template" "shellshock-8" {
  name         = "shellshock-8"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.shellshock-8.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.8"
  }
}
resource "google_compute_instance_from_template" "tunneling-9" {
  name         = "tunneling-9"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.tunneling-9.self_link}"
    }
  }
  network_interface{
    subnetwork="tunneling-main"
    network_ip="10.2.1.9"
    
  }
  network_interface{
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.9"
  }
}

resource "google_compute_instance_from_template" "tunneling-10" {
  name         = "tunneling-10"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.tunneling-10.self_link}"
    }
  }
  network_interface{
    subnetwork="tunneling-main"
    network_ip="10.2.1.10"
  }
}


resource "google_compute_instance_from_template" "sshkeys-11" {
  name         = "sshkeys-11"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.sshkeys-11.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.11"
  }
}

resource "google_compute_instance_from_template" "sshkeys-12" {
  name         = "sshkeys-12"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.sshkeys-12.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.12"
  }
}
/*
resource "google_compute_instance_from_template" "rdpgrinder-13" {
  name         = "rdpgrinder-13"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.rdpgrinder-13.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.13"
  }
}
*/

resource "google_compute_instance_from_template" "mimikatz-14" {
  name         = "mimikatz-14"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.mimikatz-14.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.14"
  }
}

/*
resource "google_compute_instance_from_template" "mimikatz-15" {
  name         = "mimikatz-15"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.mimikatz-15.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.15"
  }
}
*/
resource "google_compute_instance_from_template" "mssql-16" {
  name         = "mssql-16"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.mssql-16.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.16"
  }
}
/*
resource "google_compute_instance_from_template" "upgrader-17" {
  name         = "upgrader-17"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.upgrader-17.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.17"
    access_config {
      // Cheaper, non-premium routing
      network_tier = "STANDARD"
    }
  }
}
*/
resource "google_compute_instance_from_template" "weblogic-18" {
  name         = "weblogic-18"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.weblogic-18.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.18"
  }
}

resource "google_compute_instance_from_template" "weblogic-19" {
  name         = "weblogic-19"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.weblogic-19.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.19"
  }
}

resource "google_compute_instance_from_template" "smb-20" {
  name         = "smb-20"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.smb-20.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.20"
  }
}

resource "google_compute_instance_from_template" "scan-21" {
  name         = "scan-21"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.scan-21.self_link}"
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.21"
  }
}

resource "google_compute_instance_from_template" "scan-22" {
  name         = "scan-22"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.scan-22.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.22"
  }
}
resource "google_compute_instance_from_template" "struts2-23" {
  name         = "struts2-23"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.struts2-23.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.23"
  }
}

resource "google_compute_instance_from_template" "struts2-24" {
  name         = "struts2-24"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.struts2-24.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.24"
  }
}

resource "google_compute_instance_from_template" "island-linux-250" {
  name         = "island-linux-250"
  machine_type         = "n1-standard-2"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.island-linux-250.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.250"
    access_config {
      // Cheaper, non-premium routing
      network_tier = "STANDARD"
    }
  }
}

resource "google_compute_instance_from_template" "island-windows-251" {
  name         = "island-windows-251"
  machine_type         = "n1-standard-2"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.island-windows-251.self_link}"
    }
  }
  network_interface {
    subnetwork="monkeyzoo-main"
    network_ip="10.2.2.251"
    access_config {
      // Cheaper, non-premium routing
      network_tier = "STANDARD"
    }
  }
}