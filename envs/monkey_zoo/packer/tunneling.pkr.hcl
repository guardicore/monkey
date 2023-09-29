variable "project_id" {
    type = string
}
variable "zone" {
    type = string
    default = "europe-west3-a"
}
variable "machine_type" {
    type = string
    default = "n1-standard-2"
}
variable "source_image" {
    type = string
    default = "ubuntu-1804-bionic-v20230418"
}
variable "account_file" {
    type = string
}

source "googlecompute" "tunneling-9" {
    image_name = "tunneling-9"
    project_id = "${var.project_id}"
    source_image = "${var.source_image}"
    zone = "${var.zone}"
    disk_size = 10
    machine_type = "${var.machine_type}"
    ssh_username = "root"
    account_file = "${var.account_file}"
}

source "googlecompute" "tunneling-10" {
    image_name = "tunneling-10"
    project_id = "${var.project_id}"
    source_image = "${var.source_image}"
    zone = "${var.zone}"
    disk_size = 10
    machine_type = "${var.machine_type}"
    ssh_username = "root"
    account_file = "${var.account_file}"
}

build {
    sources = [
        "source.googlecompute.tunneling-9",
        "source.googlecompute.tunneling-10"
    ]
    provisioner "ansible" {
        only = ["googlecompute.tunneling-9"]
        playbook_file = "${path.root}/setup_tunneling_9.yml"
    }
    provisioner "ansible" {
        only = ["googlecompute.tunneling-10"]
        playbook_file = "${path.root}/setup_tunneling_10.yml"
    }
}
