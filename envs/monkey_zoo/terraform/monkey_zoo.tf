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
}

resource "google_compute_subnetwork" "credential-reuse2" {
  name          = "${local.resource_prefix}credential-reuse2"
  ip_cidr_range = "10.2.5.0/24"
  network       = google_compute_network.credential-reuse2.self_link
}

resource "google_compute_instance" "hadoop-2" {
  name              = "${local.resource_prefix}hadoop-2"
  machine_type      = "n1-standard-1"
  tags              = ["test-machine", "ubuntu16", "linux"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "hadoop-3" {
  name              = "${local.resource_prefix}hadoop-3"
  machine_type      = "e2-standard-2"
  tags              = ["test-machine", "windowsserver2016", "windows"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.hadoop-3.self_link
      type  = "pd-ssd"
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
  name              = "${local.resource_prefix}tunneling-9"
  machine_type      = "n1-standard-1"
  zone              = var.tunneling_zone
  tags              = ["tunneling-9"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.tunneling-9.self_link
    }
    auto_delete = true
  }
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
  name              = "${local.resource_prefix}tunneling-10"
  machine_type      = "n1-standard-1"
  zone              = var.tunneling_zone
  tags              = ["tunneling-10"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "tunneling-11" {
  name              = "${local.resource_prefix}tunneling-11"
  machine_type      = "n1-standard-1"
  zone              = var.tunneling_zone
  tags              = ["test-machine", "ubuntu16", "linux"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.tunneling-11.self_link
      type  = "pd-ssd"
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
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance" "tunneling-12" {
  name              = "${local.resource_prefix}tunneling-12"
  machine_type      = "e2-standard-2"
  zone              = var.tunneling_zone
  tags              = ["test-machine", "windowsserver2016", "windows"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.tunneling-12.self_link
      type  = "pd-ssd"
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

resource "google_compute_instance" "tunneling-13" {
  name              = "${local.resource_prefix}tunneling-13"
  machine_type      = "n1-standard-1"
  zone              = var.tunneling_zone
  tags              = ["test-machine", "ubuntu16", "linux"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.tunneling-13.self_link
      type  = "pd-ssd"
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

resource "google_compute_instance" "sshkeys-11" {
  name              = "${local.resource_prefix}sshkeys-11"
  machine_type      = "e2-medium"
  tags              = ["test-machine", "ubuntu16", "linux"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "sshkeys-12" {
  name              = "${local.resource_prefix}sshkeys-12"
  machine_type      = "e2-medium"
  tags              = ["test-machine", "ubuntu16", "linux"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "rdp-64" {
  name              = "${local.resource_prefix}rdp-64"
  machine_type      = "e2-standard-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2016", "windows", "rdp-64"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.rdp-64.self_link
      type  = "pd-ssd"
    }
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.64"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance" "rdp-65" {
  name              = "${local.resource_prefix}rdp-65"
  machine_type      = "e2-standard-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2012", "windows", "rdp-65"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.rdp-65.self_link
      type  = "pd-ssd"
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.65"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}


resource "google_compute_instance" "mimikatz-14" {
  name              = "${local.resource_prefix}mimikatz-14"
  machine_type      = "n1-standard-1"
  tags              = ["test-machine", "windowsserver2016", "windows"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.mimikatz-14.self_link
      type  = "pd-ssd"
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

resource "google_compute_instance" "mimikatz-15" {
  name              = "${local.resource_prefix}mimikatz-15"
  machine_type      = "n1-standard-1"
  tags              = ["test-machine", "windowsserver2016", "windows"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.mimikatz-15.self_link
      type  = "pd-ssd"
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

resource "google_compute_instance" "mssql-16" {
  name              = "${local.resource_prefix}mssql-16"
  machine_type      = "e2-standard-2"
  tags              = ["test-machine", "windowsserver2016", "windows"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.mssql-16.self_link
      type  = "pd-ssd"
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
  name              = "${local.resource_prefix}snmp-20"
  machine_type      = "n1-standard-1"
  zone              = var.main1_zone
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "powershell-3-48" {
  name              = "${local.resource_prefix}powershell-3-48"
  machine_type      = "e2-standard-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2016", "windows", "powershell", "powershell-48"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.powershell-3-48.self_link
      type  = "pd-ssd"
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.48"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance" "powershell-3-47" {
  name              = "${local.resource_prefix}powershell-3-47"
  machine_type      = "e2-standard-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2016", "windows", "powershell", "powershell-47"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.powershell-3-47.self_link
      type  = "pd-ssd"
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.47"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance" "powershell-3-46" {
  name              = "${local.resource_prefix}powershell-3-46"
  machine_type      = "e2-standard-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2016", "windows", "powershell", "powershell-46"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.powershell-3-46.self_link
      type  = "pd-ssd"
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.46"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance" "powershell-3-44" {
  name              = "${local.resource_prefix}powershell-3-44"
  machine_type      = "e2-standard-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2016", "windows", "powershell", "powershell-44"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.powershell-3-44.self_link
      type  = "pd-ssd"
    }
    auto_delete = true
  }
  network_interface {
    subnetwork = "${local.resource_prefix}monkeyzoo-main-1"
    network_ip = "10.2.3.44"
    access_config {
      // Allows Ephemeral IPs
    }
  }
}

resource "google_compute_instance" "powershell-3-45" {
  name              = "${local.resource_prefix}powershell-3-45"
  machine_type      = "e2-standard-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2016", "windows", "powershell", "powershell-45"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.powershell-3-45.self_link
      type  = "pd-ssd"
    }
    auto_delete = true
  }
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

resource "google_compute_instance" "credentials-reuse-14" {
  name              = "${local.resource_prefix}credentials-reuse-14"
  machine_type      = "e2-small"
  zone              = var.credentials_reuse_zone
  tags              = ["test-machine", "ubuntu16", "linux", "credentials-reuse"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "credentials-reuse-15" {
  name              = "${local.resource_prefix}credentials-reuse-15"
  machine_type      = "e2-small"
  zone              = var.credentials_reuse_zone
  tags              = ["test-machine", "ubuntu16", "linux", "credentials-reuse"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "credentials-reuse-16" {
  name              = "${local.resource_prefix}credentials-reuse-16"
  machine_type      = "e2-small"
  zone              = var.credentials_reuse_zone
  tags              = ["test-machine", "ubuntu16", "linux", "credentials-reuse"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "log4j-solr-49" {
  name              = "${local.resource_prefix}log4j-solr-49"
  machine_type      = "e2-highcpu-4"
  zone              = var.main1_zone
  tags              = ["test-machine", "ubuntu16", "linux"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "log4j-solr-50" {
  name              = "${local.resource_prefix}log4j-solr-50"
  machine_type      = "e2-standard-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2016", "windows"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.log4j-solr-50.self_link
      type  = "pd-ssd"
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

resource "google_compute_instance" "log4j-tomcat-51" {
  name              = "${local.resource_prefix}log4j-tomcat-51"
  machine_type      = "e2-highcpu-4"
  zone              = var.main1_zone
  tags              = ["test-machine", "ubuntu16", "linux"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "log4j-tomcat-52" {
  name              = "${local.resource_prefix}log4j-tomcat-52"
  machine_type      = "e2-standard-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2016", "windows"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.log4j-tomcat-52.self_link
      type  = "pd-ssd"
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

resource "google_compute_instance" "log4j-logstash-55" {
  name              = "${local.resource_prefix}log4j-logstash-55"
  machine_type      = "e2-highcpu-4"
  zone              = var.main1_zone
  tags              = ["test-machine", "ubuntu16", "linux"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "log4j-logstash-56" {
  name              = "${local.resource_prefix}log4j-logstash-56"
  machine_type      = "e2-standard-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2016", "windows"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.log4j-logstash-56.self_link
      type  = "pd-ssd"
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

resource "google_compute_instance" "browser-credentials-66" {
  name              = "${local.resource_prefix}browser-credentials-66"
  machine_type      = "e2-highcpu-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "windowsserver2016", "windows"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.browser-credentials-66.self_link
      type  = "pd-ssd"
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

resource "google_compute_instance" "browser-credentials-67" {
  name              = "${local.resource_prefix}browser-credentials-67"
  machine_type      = "e2-highcpu-2"
  zone              = var.main1_zone
  tags              = ["test-machine", "ubuntu16", "linux"]
  resource_policies = var.resource_policies
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

resource "google_compute_instance" "zerologon-25" {
  name              = "${local.resource_prefix}zerologon-25"
  machine_type      = "e2-standard-2"
  tags              = ["test-machine", "windowsserver2016", "windows"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.zerologon-25.self_link
      type  = "pd-ssd"
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

resource "google_compute_instance" "island-linux-250" {
  name              = "${local.resource_prefix}island-linux-250"
  machine_type      = "n2-custom-2-4096"
  tags              = ["island", "linux", "ubuntu16"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.island-linux-250.self_link
      size  = 20
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

resource "google_compute_instance" "island-windows-251" {
  name              = "${local.resource_prefix}island-windows-251"
  machine_type      = "e2-custom-4-8192"
  tags              = ["test-machine", "windowsserver2016", "windows", "island"]
  resource_policies = var.resource_policies
  boot_disk {
    initialize_params {
      image = data.google_compute_image.island-windows-251.self_link
      type  = "pd-ssd"
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
