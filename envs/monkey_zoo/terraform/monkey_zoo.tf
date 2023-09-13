
// Local variables
locals {
  default_ubuntu  = google_compute_instance_template.ubuntu16.self_link
  windows_2012 = google_compute_instance_template.windows2012.self_link
  windows_2016 = google_compute_instance_template.windows2016.self_link
}

// Network
resource "google_compute_network" "monkeyzoo" {
  name                    = "${local.resource_prefix}monkeyzoo"
  auto_create_subnetworks = false
}

resource "google_compute_network" "tunneling" {
  name                    = "${local.resource_prefix}tunneling"
  auto_create_subnetworks = false
}

resource "google_compute_network" "tunneling2" {
  name                    = "${local.resource_prefix}tunneling2"
  auto_create_subnetworks = false
}

resource "google_compute_network" "credential-reuse" {
  name                    = "${local.resource_prefix}credential-reuse"
  auto_create_subnetworks = false
}

resource "google_compute_network" "credential-reuse2" {
  name                    = "${local.resource_prefix}credential-reuse2"
  auto_create_subnetworks = false
}

resource "google_compute_network" "powershell" {
  name                    = "${local.resource_prefix}powershell"
  auto_create_subnetworks = false
}

// Subnetwork for the above networks
resource "google_compute_subnetwork" "monkeyzoo-main" {
  name          = "${local.resource_prefix}monkeyzoo-main"
  ip_cidr_range = "10.2.2.0/24"
  network       = google_compute_network.monkeyzoo.self_link
}

resource "google_compute_subnetwork" "monkeyzoo-main-1" {
  name          = "${local.resource_prefix}monkeyzoo-main-1"
  ip_cidr_range = "10.2.3.0/24"
  network       = google_compute_network.monkeyzoo.self_link
  region        = "europe-west1"
}

resource "google_compute_subnetwork" "tunneling-main" {
  name          = "${local.resource_prefix}tunneling-main"
  ip_cidr_range = "10.2.1.0/28"
  network       = google_compute_network.tunneling.self_link
}

resource "google_compute_subnetwork" "powershell-main" {
  name          = "${local.resource_prefix}powershell-main"
  ip_cidr_range = "10.2.4.0/24"
  network       = google_compute_network.powershell.self_link
  region        = "europe-west1"
}

resource "google_compute_subnetwork" "tunneling2-main" {
  name          = "${local.resource_prefix}tunneling2-main"
  ip_cidr_range = "10.2.0.0/27"
  network       = google_compute_network.tunneling2.self_link
}

resource "google_compute_subnetwork" "credential-reuse" {
  name          = "${local.resource_prefix}credential-reuse"
  ip_cidr_range = "10.2.4.0/24"
  network       = google_compute_network.credential-reuse.self_link
  region        = "europe-west1"
}

resource "google_compute_subnetwork" "credential-reuse2" {
  name          = "${local.resource_prefix}credential-reuse2"
  ip_cidr_range = "10.2.5.0/24"
  network       = google_compute_network.credential-reuse2.self_link
  region        = "europe-west1"
}

resource "google_compute_instance_from_template" "hadoop-2" {
  name                     = "${local.resource_prefix}hadoop-2"
  source_instance_template = local.default_ubuntu
  zone                     = "europe-west3-a"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.hadoop-2.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.2"
    access_config {
      // Allows Ephemeral IPs
    }
  }
  // Add required ssh keys for hadoop service and restart it
  metadata_startup_script = "[ ! -f /home/vakaris_zilius/.ssh/authorized_keys ] && sudo cat /home/vakaris_zilius/.ssh/id_rsa.pub >> /home/vakaris_zilius/.ssh/authorized_keys && sudo reboot"
}

resource "google_compute_instance_from_template" "hadoop-3" {
  name                     = "${local.resource_prefix}hadoop-3"
  source_instance_template = local.windows_2016
  machine_type             = "e2-custom-4-8192"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.hadoop-3.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.3"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance" "tunneling-9" {
  name         = "${local.resource_prefix}tunneling-9"
  machine_type = "n1-standard-2"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.tunneling-9.self_link
    }
    auto_delete = true
  }
  tags = ["tunneling-9"]
  network_interface {
    subnetwork = "${local.resource_prefix}tunneling-main"
    network_ip = "10.2.1.9"
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.9"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance" "tunneling-10" {
  name         = "${local.resource_prefix}tunneling-10"
  machine_type = "n1-standard-2"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.tunneling-10.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}tunneling-main"
    network_ip = "10.2.1.10"
    access_config {
      // Allows Ephemeral IPs
    }
  }
  network_interface {
    subnetwork = "${local.resource_prefix}tunneling2-main"
    network_ip = "10.2.0.10"
  }
}

resource "google_compute_instance_from_template" "tunneling-11" {
  name                     = "${local.resource_prefix}tunneling-11"
  source_instance_template = local.default_ubuntu
  machine_type             = "e2-small"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.tunneling-11.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}tunneling2-main"
    network_ip = "10.2.0.11"
  }
  network_interface {
    subnetwork = "${local.resource_prefix}tunneling-main"
    network_ip = "10.2.1.11"
  }
}

resource "google_compute_instance_from_template" "tunneling-12" {
  name                     = "${local.resource_prefix}tunneling-12"
  source_instance_template = local.windows_2016
  machine_type             = "e2-highcpu-4"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.tunneling-12.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}tunneling2-main"
    network_ip = "10.2.0.12"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "tunneling-13" {
  name                     = "${local.resource_prefix}tunneling-13"
  source_instance_template = local.default_ubuntu
  machine_type             = "e2-small"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.tunneling-13.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}tunneling2-main"
    network_ip = "10.2.0.13"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "sshkeys-11" {
  name                     = "${local.resource_prefix}sshkeys-11"
  source_instance_template = local.default_ubuntu
  machine_type             = "custom-2-3840"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.sshkeys-11.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.11"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "sshkeys-12" {
  name                     = "${local.resource_prefix}sshkeys-12"
  source_instance_template = local.default_ubuntu
  machine_type             = "custom-2-3840"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.sshkeys-12.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.12"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "rdp-64" {
  name                     = "${local.resource_prefix}rdp-64"
  source_instance_template = local.windows_2016
  machine_type             = "e2-highcpu-4"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.rdp-64.self_link}"
    }
  }
  tags = ["rdp-64"]
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main-1"
    network_ip="10.2.3.64"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "rdp-65" {
  name                     = "${local.resource_prefix}rdp-65"
  source_instance_template = local.windows_2012
  machine_type             = "e2-highcpu-4"
  boot_disk{
    initialize_params {
      image = "${data.google_compute_image.rdp-65.self_link}"
    }
    auto_delete = true
  }
  tags = ["rdp-65"]
  network_interface {
    subnetwork="${local.resource_prefix}monkeyzoo-main-1"
    network_ip="10.2.3.65"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}


resource "google_compute_instance_from_template" "mimikatz-14" {
  name                     = "${local.resource_prefix}mimikatz-14"
  source_instance_template = local.windows_2016
  boot_disk {
    initialize_params {
      image = data.google_compute_image.mimikatz-14.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.14"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "mimikatz-15" {
  name                     = "${local.resource_prefix}mimikatz-15"
  source_instance_template = local.windows_2016
  boot_disk {
    initialize_params {
      image = data.google_compute_image.mimikatz-15.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.15"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "mssql-16" {
  name                     = "${local.resource_prefix}mssql-16"
  source_instance_template = local.windows_2016
  machine_type             = "e2-highcpu-4"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.mssql-16.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.16"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance" "snmp-20" {
  name           = "${local.resource_prefix}snmp-20"
  machine_type   = "n1-standard-1"
  zone           = "europe-west1-b"
  can_ip_forward = false
  service_account {
    email  = local.service_account_email
    scopes = ["cloud-platform"]
  }
  boot_disk {
    initialize_params {
      image = data.google_compute_image.snmp-20.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.20"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "powershell-3-48" {
  name                     = "${local.resource_prefix}powershell-3-48"
  source_instance_template = local.windows_2016
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.powershell-3-48.self_link
    }
    auto_delete = true
  }
  tags = ["powershell", "powershell-48"]
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.48"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "powershell-3-47" {
  name                     = "${local.resource_prefix}powershell-3-47"
  source_instance_template = local.windows_2016
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.powershell-3-47.self_link
    }
    auto_delete = true
  }
  tags = ["powershell", "powershell-47"]
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.47"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "powershell-3-46" {
  name                     = "${local.resource_prefix}powershell-3-46"
  source_instance_template = local.windows_2016
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.powershell-3-46.self_link
    }
    auto_delete = true
  }
  tags = ["powershell", "powershell-46"]
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.46"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "powershell-3-44" {
  name                     = "${local.resource_prefix}powershell-3-44"
  source_instance_template = local.windows_2016
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.powershell-3-44.self_link
    }
    auto_delete = true
  }
  tags = ["powershell", "powershell-44"]
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.44"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "powershell-3-45" {
  name                     = "${local.resource_prefix}powershell-3-45"
  source_instance_template = local.windows_2016
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.powershell-3-45.self_link
    }
    auto_delete = true
  }
  tags = ["powershell", "powershell-45"]
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.45"
    access_config {
      // Allows Ephemeral IPs
    }
  }
  network_interface {
    subnetwork = "${local.resource_prefix}powershell-main"
    network_ip = "10.2.4.45"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "credentials-reuse-14" {
  name                     = "${local.resource_prefix}credentials-reuse-14"
  tags                     = ["credentials-reuse"]
  source_instance_template = local.default_ubuntu
  machine_type             = "e2-small"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.credentials-reuse-14.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.14"
    access_config {
      // Allows Ephemeral IPs
    }
  }
  network_interface {
    subnetwork = "${local.resource_prefix}credential-reuse"
    network_ip = "10.2.4.14"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "credentials-reuse-15" {
  name                     = "${local.resource_prefix}credentials-reuse-15"
  tags                     = ["credentials-reuse"]
  source_instance_template = local.default_ubuntu
  machine_type             = "e2-small"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.credentials-reuse-15.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}credential-reuse"
    network_ip = "10.2.4.15"
    access_config {
      // Allows Ephemeral IPs
    }
  }
  network_interface {
    subnetwork = "${local.resource_prefix}credential-reuse2"
    network_ip = "10.2.5.15"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "credentials-reuse-16" {
  name                     = "${local.resource_prefix}credentials-reuse-16"
  tags                     = ["credentials-reuse"]
  source_instance_template = local.default_ubuntu
  machine_type             = "e2-small"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.credentials-reuse-16.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}credential-reuse2"
    network_ip = "10.2.5.16"
    access_config {
      // Allows Ephemeral IPs
    }
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.16"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "log4j-solr-49" {
  name                     = "${local.resource_prefix}log4j-solr-49"
  source_instance_template = local.default_ubuntu
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.log4j-solr-49.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.49"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "log4j-solr-50" {
  name                     = "${local.resource_prefix}log4j-solr-50"
  source_instance_template = local.windows_2016
  machine_type             = "e2-standard-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.log4j-solr-50.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.50"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "log4j-tomcat-51" {
  name                     = "${local.resource_prefix}log4j-tomcat-51"
  source_instance_template = local.default_ubuntu
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.log4j-tomcat-51.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.51"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "log4j-tomcat-52" {
  name                     = "${local.resource_prefix}log4j-tomcat-52"
  source_instance_template = local.windows_2016
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.log4j-tomcat-52.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.52"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "log4j-logstash-55" {
  name                     = "${local.resource_prefix}log4j-logstash-55"
  source_instance_template = local.default_ubuntu
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.log4j-logstash-55.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.55"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "log4j-logstash-56" {
  name                     = "${local.resource_prefix}log4j-logstash-56"
  source_instance_template = local.windows_2016
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.log4j-logstash-56.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.56"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "browser-credentials-66" {
  name                     = "${local.resource_prefix}browser-credentials-66"
  source_instance_template = local.default_ubuntu
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.browser-credentials-66.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.66"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "browser-credentials-67" {
  name                     = "${local.resource_prefix}browser-credentials-67"
  source_instance_template = local.default_ubuntu
  machine_type             = "e2-highcpu-4"
  zone                     = "europe-west1-b"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.browser-credentials-67.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.67"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "zerologon-25" {
  name                     = "${local.resource_prefix}zerologon-25"
  source_instance_template = local.windows_2016
  machine_type             = "e2-custom-4-8192"
  boot_disk {
    initialize_params {
      image = data.google_compute_image.zerologon-25.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.25"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance_from_template" "island-linux-250" {
  name                     = "${local.resource_prefix}island-linux-250"
  machine_type             = "n2-custom-2-4096"
  tags                     = ["island", "linux", "ubuntu16"]
  source_instance_template = local.default_ubuntu
  boot_disk {
    initialize_params {
      image = data.google_compute_image.island-linux-250.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.250"
    access_config {
      // Cheaper, non-premium routing (not available in some regions)
      // network_tier = "STANDARD"
    }
  }
}

resource "google_compute_instance_from_template" "island-windows-251" {
  name                     = "${local.resource_prefix}island-windows-251"
  machine_type             = "e2-highcpu-4"
  tags                     = ["island", "windows", "windowsserver2016"]
  source_instance_template = local.windows_2016
  boot_disk {
    initialize_params {
      image = data.google_compute_image.island-windows-251.self_link
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main"
    network_ip = "10.2.2.251"
    access_config {
      // Cheaper, non-premium routing (not available in some regions)
      // network_tier = "STANDARD"
    }
  }
}
