
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

resource "google_compute_subnetwork" "monkeyzoo-main-1" {
  name = "${local.resource_prefix}monkeyzoo-main-1"
  ip_cidr_range   = "10.2.3.0/24"
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

resource "google_compute_instance_from_template" "powershell-3-48" {
  name = "${local.resource_prefix}powershell-3-48"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.powershell-3-48.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main-1"
    network_ip="10.2.3.48"
  }
}

resource "google_compute_instance_from_template" "powershell-3-47" {
  name = "${local.resource_prefix}powershell-3-47"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.powershell-3-47.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main-1"
    network_ip="10.2.3.47"
  }
}

resource "google_compute_instance_from_template" "powershell-3-46" {
  name = "${local.resource_prefix}powershell-3-46"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.powershell-3-46.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main-1"
    network_ip="10.2.3.46"
  }
}

resource "google_compute_instance_from_template" "powershell-3-45" {
  name = "${local.resource_prefix}powershell-3-45"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.powershell-3-45.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.3.45"
  }
}

resource "google_compute_instance_from_template" "powershell-3-45" {
  name = "${local.resource_prefix}powershell-3-45"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.powershell-3-45.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.3.45"
  }
}

resource "google_compute_instance_from_template" "log4j-solr-49" {
  name = "${local.resource_prefix}log4j-solr-49"
  source_instance_template = local.default_linux
  boot_disk{
    initialize_params {
      image = data.google_compute_image.log4j-solr-49.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.3.49"
  }
}

resource "google_compute_instance_from_template" "log4j-solr-50" {
  name = "${local.resource_prefix}log4j-solr-50"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.log4j-solr-50.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.3.50"
  }
}

resource "google_compute_instance_from_template" "log4j-tomcat-51" {
  name = "${local.resource_prefix}log4j-tomcat-51"
  source_instance_template = local.default_linux
  boot_disk{
    initialize_params {
      image = data.google_compute_image.log4j-tomcat-51.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.3.51"
  }
}

resource "google_compute_instance_from_template" "log4j-tomcat-52" {
  name = "${local.resource_prefix}log4j-tomcat-52"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.log4j-tomcat-52.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.3.52"
  }
}

resource "google_compute_instance_from_template" "log4j-logstash-55" {
  name = "${local.resource_prefix}log4j-logstash-55"
  source_instance_template = local.default_linux
  boot_disk{
    initialize_params {
      image = data.google_compute_image.log4j-logstash-55.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.3.55"
  }
}

resource "google_compute_instance_from_template" "log4j-logstash-56" {
  name = "${local.resource_prefix}log4j-logstash-56"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.log4j-logstash-56.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.3.56"
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

resource "google_compute_instance_from_template" "zerologon-25" {
  name = "${local.resource_prefix}zerologon-25"
  source_instance_template = local.default_windows
  boot_disk{
    initialize_params {
      image = data.google_compute_image.zerologon-25.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main"
    network_ip="10.2.2.25"
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
