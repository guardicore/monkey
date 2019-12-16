resource "google_compute_firewall" "islands-in" {
  name    = "${local.resource_prefix}islands-in"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "tcp"
    ports    = ["22", "443", "3389", "5000"]
  }

  direction = "INGRESS"
  priority = "65534"
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
  source_ranges = ["10.2.2.0/24"]
}

resource "google_compute_firewall" "monkeyzoo-out" {
  name    = "${local.resource_prefix}monkeyzoo-out"
  network = google_compute_network.monkeyzoo.name

  allow {
    protocol = "all"
  }

  direction = "EGRESS"
  priority = "65534"
  destination_ranges = ["10.2.2.0/24"]
}

resource "google_compute_firewall" "tunneling-in" {
  name    = "${local.resource_prefix}tunneling-in"
  network = google_compute_network.tunneling.name

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  source_ranges = ["10.2.1.0/24"]
}

resource "google_compute_firewall" "tunneling-out" {
  name    = "${local.resource_prefix}tunneling-out"
  network = google_compute_network.tunneling.name

  allow {
    protocol = "all"
  }

  direction = "EGRESS"
  destination_ranges = ["10.2.1.0/24"]
}

resource "google_compute_firewall" "tunneling2-in" {
  name    = "${local.resource_prefix}tunneling2-in"
  network = google_compute_network.tunneling2.name

  allow {
    protocol = "all"
  }

  direction = "INGRESS"
  source_ranges = ["10.2.0.0/24"]
}

resource "google_compute_firewall" "tunneling2-out" {
  name    = "${local.resource_prefix}tunneling2-out"
  network = google_compute_network.tunneling2.name

  allow {
    protocol = "all"
  }

  direction = "EGRESS"
  destination_ranges = ["10.2.0.0/24"]
}
