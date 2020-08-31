
// Local variables
locals {
  default_ubuntu=google_compute_instance_template.ubuntu16.self_link
  default_windows=google_compute_instance_template.windows2016.self_link
}

resource "google_compute_network" "monkeyzoo" {
  name = "${local.resource_prefix}monkeyzoo"
  auto_create_subnetworks = false
}

resource "google_compute_network" "tunneling" {
  name = "${local.resource_prefix}tunneling"
  auto_create_subnetworks = false
}

resource "google_compute_network" "tunneling2" {
  name = "${local.resource_prefix}tunneling2"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "monkeyzoo-main" {
  name = "${local.resource_prefix}monkeyzoo-main"
  ip_cidr_range   = "10.2.2.0/24"
  network         = google_compute_network.monkeyzoo.self_link
}

resource "google_compute_subnetwork" "tunneling-main" {
  name = "${local.resource_prefix}tunneling-main"
  ip_cidr_range   = "10.2.1.0/28"
  network         = google_compute_network.tunneling.self_link
}

resource "google_compute_subnetwork" "tunneling2-main" {
  name = "${local.resource_prefix}tunneling2-main"
  ip_cidr_range   = "10.2.0.0/27"
  network         = google_compute_network.tunneling2.self_link
}

resource "google_compute_instance_from_template" "hadoop-2" {
  name = "${local.resource_prefix}hadoop-2"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.hadoop-2.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.2"
  }
  // Add required ssh keys for hadoop service and restart it
  metadata_startup_script = "[ ! -f /home/vakaris_zilius/.ssh/authorized_keys ] && sudo cat /home/vakaris_zilius/.ssh/id_rsa.pub >> /home/vakaris_zilius/.ssh/authorized_keys && sudo reboot"
}

resource "google_compute_instance_from_template" "hadoop-3" {
  name = "${local.resource_prefix}hadoop-3"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.hadoop-3.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.3"
  }
}

resource "google_compute_instance_from_template" "elastic-4" {
  name = "${local.resource_prefix}elastic-4"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.elastic-4.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.4"
  }
}

resource "google_compute_instance_from_template" "elastic-5" {
  name = "${local.resource_prefix}elastic-5"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.elastic-5.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.5"
  }
}

/* Couldn't find ubuntu packages for required samba version (too old).
resource "google_compute_instance_from_template" "sambacry-6" {
  name = "${local.resource_prefix}sambacry-6"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.sambacry-6.self_link}"
    }
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.6"
  }
}
*/

/* We need custom 32 bit Ubuntu machine for this (there are no 32 bit ubuntu machines in GCP).
resource "google_compute_instance_from_template" "sambacry-7" {
  name = "${local.resource_prefix}sambacry-7"
  source_instance_template = "${local.default_ubuntu}"
  boot_disk {
    initialize_params {
      // Add custom image to cloud
      image = "ubuntu32"
    }
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.7"
  }
}
*/

resource "google_compute_instance_from_template" "shellshock-8" {
  name = "${local.resource_prefix}shellshock-8"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.shellshock-8.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.8"
  }
}

resource "google_compute_instance_from_template" "tunneling-9" {
  name = "${local.resource_prefix}tunneling-9"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.tunneling-9.self_link
    }
    auto_delete = true
  }
  network_interface{
    subnetwork="${local.resource_prefix}tunneling-main"
    network_ip="10.2.1.9"
  }
  network_interface{
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.9"
  }
}

resource "google_compute_instance_from_template" "tunneling-10" {
  name = "${local.resource_prefix}tunneling-10"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.tunneling-10.self_link
    }
    auto_delete = true
  }
  network_interface{
    subnetwork="${local.resource_prefix}tunneling-main"
    network_ip="10.2.1.10"
  }
  network_interface{
    subnetwork="${local.resource_prefix}tunneling2-main"
    network_ip="10.2.0.10"
  }
}

resource "google_compute_instance_from_template" "tunneling-11" {
  name = "${local.resource_prefix}tunneling-11"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.tunneling-11.self_link
    }
    auto_delete = true
  }
  network_interface{
    subnetwork="${local.resource_prefix}tunneling2-main"
    network_ip="10.2.0.11"
  }
}

resource "google_compute_instance_from_template" "tunneling-12" {
  name = "${local.resource_prefix}tunneling-12"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.tunneling-12.self_link
    }
    auto_delete = true
  }
  network_interface{
    subnetwork="${local.resource_prefix}tunneling2-main"
    network_ip="10.2.0.12"
  }
}

resource "google_compute_instance_from_template" "sshkeys-11" {
  name = "${local.resource_prefix}sshkeys-11"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.sshkeys-11.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.11"
  }
}

resource "google_compute_instance_from_template" "sshkeys-12" {
  name = "${local.resource_prefix}sshkeys-12"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.sshkeys-12.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.12"
  }
}

/*
resource "google_compute_instance_from_template" "rdpgrinder-13" {
  name = "${local.resource_prefix}rdpgrinder-13"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.rdpgrinder-13.self_link}"
    }
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.13"
  }
}
*/

resource "google_compute_instance_from_template" "mimikatz-14" {
  name = "${local.resource_prefix}mimikatz-14"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.mimikatz-14.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.14"
  }
}

resource "google_compute_instance_from_template" "mimikatz-15" {
  name = "${local.resource_prefix}mimikatz-15"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.mimikatz-15.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.15"
  }
}

resource "google_compute_instance_from_template" "mssql-16" {
  name = "${local.resource_prefix}mssql-16"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.mssql-16.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.16"
  }
}

/* We need to alter monkey's behavior for this to upload 32-bit monkey instead of 64-bit (not yet developed)
resource "google_compute_instance_from_template" "upgrader-17" {
  name = "${local.resource_prefix}upgrader-17"
  source_instance_template = "${local.default_windows}"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.upgrader-17.self_link}"
    }
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.17"
    access_config {
      // Cheaper, non-premium routing
      network_tier = "STANDARD"
    }
  }
}
*/

resource "google_compute_instance_from_template" "weblogic-18" {
  name = "${local.resource_prefix}weblogic-18"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.weblogic-18.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.18"
  }
}

resource "google_compute_instance_from_template" "weblogic-19" {
  name = "${local.resource_prefix}weblogic-19"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.weblogic-19.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.19"
  }
}

resource "google_compute_instance_from_template" "smb-20" {
  name = "${local.resource_prefix}smb-20"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.smb-20.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.20"
  }
}

resource "google_compute_instance_from_template" "scan-21" {
  name = "${local.resource_prefix}scan-21"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.scan-21.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.21"
  }
}

resource "google_compute_instance_from_template" "scan-22" {
  name = "${local.resource_prefix}scan-22"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.scan-22.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.22"
  }
}

resource "google_compute_instance_from_template" "struts2-23" {
  name = "${local.resource_prefix}struts2-23"
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.struts2-23.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.23"
  }
}

resource "google_compute_instance_from_template" "struts2-24" {
  name = "${local.resource_prefix}struts2-24"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.struts2-24.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.24"
  }
}

resource "google_compute_instance_from_template" "island-linux-250" {
  name = "${local.resource_prefix}island-linux-250"
  machine_type         = "n1-standard-2"
  tags = ["island", "linux", "ubuntu16"]
  source_instance_template = local.default_ubuntu
  boot_disk{
    initialize_params {
      image = data.google_compute_image.island-linux-250.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.250"
    access_config {
      // Cheaper, non-premium routing (not available in some regions)
      // network_tier = "STANDARD"
    }
  }
}

resource "google_compute_instance_from_template" "island-windows-251" {
  name = "${local.resource_prefix}island-windows-251"
  machine_type         = "n1-standard-2"
  tags = ["island", "windows", "windowsserver2016"]
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.island-windows-251.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.251"
    access_config {
      // Cheaper, non-premium routing (not available in some regions)
      // network_tier = "STANDARD"
    }
  }
}
