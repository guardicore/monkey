resource "google_compute_firewall" "islands-in" {
  name    = "${local.resource_prefix}islands-in"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "tcp"
    ports    = ["22", "443", "3389", "5000"]
  }

  direction = "INGRESS"
  priority = "65534"
  source_ranges = ["0.0.0.0/0"]
  target_tags = ["island"]
}

resource "google_compute_firewall" "islands-out" {
  name    = "${local.resource_prefix}islands-out"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "tcp"
  }

  direction = "EGRESS"
  priority = "65534"
  target_tags = ["island"]
}

resource "google_compute_firewall" "monkeyzoo-in" {
  name    = "${local.resource_prefix}monkeyzoo-in"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "65534"
  source_ranges = ["10.2.2.0/24", "10.2.1.0/27", "10.2.3.0/24", "10.2.4.0/24" ]
}

resource "google_compute_firewall" "monkeyzoo-out" {
  name    = "${local.resource_prefix}monkeyzoo-out"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "all"
  }

  direction = "EGRESS"
  priority = "65534"
  destination_ranges = ["10.2.2.0/24", "10.2.1.0/27", "10.2.3.0/24", "10.2.4.0/24" ]
}

resource "google_compute_firewall" "tunneling-in" {
  name    = "${local.resource_prefix}tunneling-in"
  network = google_compute_network.tunneling.name

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  source_ranges = ["10.2.1.0/28"]
}

resource "google_compute_firewall" "tunneling-out" {
  name    = "${local.resource_prefix}tunneling-out"
  network = google_compute_network.tunneling.name

  allow {
    protocol = "all"
  }

  direction = "EGRESS"
  destination_ranges = ["10.2.1.0/28"]
}

resource "google_compute_firewall" "tunneling2-in" {
  name    = "${local.resource_prefix}tunneling2-in"
  network = google_compute_network.tunneling2.name

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  source_ranges = ["10.2.0.0/27"]
}

resource "google_compute_firewall" "tunneling2-out" {
  name    = "${local.resource_prefix}tunneling2-out"
  network = google_compute_network.tunneling2.name

  allow {
    protocol = "all"
  }

  direction = "EGRESS"
  destination_ranges = ["10.2.0.0/27"]
}

resource "google_compute_firewall" "allow-tunneling-only-from-islands" {
  name    = "${local.resource_prefix}allow-tunneling-only-from-islands"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "1000"
  source_tags = ["island"]
  target_tags = ["tunneling-9"]
}


resource "google_compute_firewall" "credentials-reuse-in" {
  name    = "${local.resource_prefix}credentials-reuse-in"
  network = google_compute_network.credential-reuse.name

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "1000"
  source_tags = ["island", "credentials-reuse"]
}

resource "google_compute_firewall" "credentials-reuse2-in" {
  name    = "${local.resource_prefix}credentials-reuse2-in"
  network = google_compute_network.credential-reuse2.name

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "1000"
  source_tags = ["island", "credentials-reuse"]
}


resource "google_compute_firewall" "powershell-48-allow" {
  name    = "${local.resource_prefix}powershell-48-allow"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "all"
  }

  direction = "EGRESS"
  priority = "1000"
  destination_ranges = ["10.2.2.0/24"]
  target_tags = ["powershell-48"]
}


resource "google_compute_firewall" "powershell-48-allow-egress-45" {
  name    = "${local.resource_prefix}powershell-48-allow-egress-45"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "all"
  }

  direction = "EGRESS"
  priority = "5"
  destination_ranges = ["10.2.3.45/32"]
  target_tags = ["powershell-48"]
}

resource "google_compute_firewall" "powershell-48-deny-all-egress" {
  name    = "${local.resource_prefix}powershell-48-deny-all-egress"
  network = google_compute_network.monkeyzoo.name

  deny {
    protocol = "all"
  }

  direction = "EGRESS"
  priority = "10"
  destination_ranges = ["0.0.0.0/0"]
  target_tags = ["powershell-48"]
}


resource "google_compute_firewall" "powershell-45-deny" {
  name    = "${local.resource_prefix}powershell-45-deny"
  network = google_compute_network.monkeyzoo.name
  description = "Denies access to 45 from 46 and 47. 45 machines needs to be exploited only by the island."

  deny {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "1000"
  source_ranges = ["10.2.3.46/32", "10.2.3.47/32"]
  target_tags = ["powershell-45"]
}

resource "google_compute_firewall" "powershell-48-deny" {
  name    = "${local.resource_prefix}powershell-48-deny"
  network = google_compute_network.monkeyzoo.name

  deny {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "1000"
  source_ranges = ["10.2.3.47/32", "10.2.3.46/32", "10.2.2.0/24"]
  target_tags = ["powershell-48"]
}

resource "google_compute_firewall" "powershell-45-allow" {
  name    = "${local.resource_prefix}powershell-45-allow"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "1000"
  source_ranges = ["10.2.2.0/24"]
  target_tags = ["powershell-45"]
}

resource "google_compute_firewall" "powershell-allow" {
  name    = "${local.resource_prefix}powershell-allow"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "1000"
  source_ranges = ["10.2.2.0/24"]
  target_tags = ["powershell"]
}

resource "google_compute_firewall" "monkeyzoo-test-in" {
  name    = "${local.resource_prefix}monkeyzoo-test-in"
  network = google_compute_network.monkeyzoo.name
  description = "Allows access to the instances in the MonkeyZoo. Add your public IP under Source filters if you want to SSH/RDP in the instances."

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "999"
  // Here goes your public IP so you can SSH/RDP in the instances
  source_ranges = ["127.0.0.1/32"]
}

resource "google_compute_firewall" "allow-all-tunneling2" {
  name    = "${local.resource_prefix}allow-all-tunneling2"
  network = google_compute_network.tunneling2.name
  description = "Allows access to the tunneling2 instances  in the MonkeyZoo. Add your public IP under Source filters if you want to SSH/RDP in the instances."

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  priority = "900"
  // Here goes your public IP so you can SSH/RDP in the instances
  source_ranges = ["127.0.0.1/32"]
}

resource "google_compute_firewall" "allow-rdp64-and-island" {
  name    = "allow-rdp64-to-island"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "all"
  }
  priority = "999"
  source_tags = ["island", "rdp-64"]
  target_tags = ["rdp-64", "island"]
}


resource "google_compute_firewall" "allow-rdp65-and-rdp64" {
  name    = "allow-rdp65-to-rdp64"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "all"
  }
  priority = "999"

  source_tags = ["rdp-64", "rdp-65"]
  target_tags = ["rdp-65", "rdp-64"]
}


resource "google_compute_firewall" "deny-rdp-from-others" {
  name    = "deny-rdp65-from-others"
  network = google_compute_network.monkeyzoo.name

  deny {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["rdp-64", "rdp-65"]
}

resource "google_compute_firewall" "deny-rdp64-rdp65-to-others" {
  name    = "deny-rdp64-rdp65-to-others"
  network = google_compute_network.monkeyzoo.name

  deny {
    protocol = "all"
  }

  source_tags = ["rdp-64", "rdp-65"]
}

// We are disabling PowerShell because we want only RDP to run on these machines
// and we can't do it via Packer because it uses WinRM to configure the instances
resource "google_compute_firewall" "deny-powershell-on-rdp" {
 name    = "deny-powershell-on-rdp"
 network = google_compute_network.monkeyzoo.name

 deny {
    protocol = "tcp"
    ports    = ["5985", "5986"]
 }
 direction = "INGRESS"
 priority = "998"

 source_ranges = ["0.0.0.0/0"]
 target_tags   = ["rdp-64", "rdp-65"]
}
