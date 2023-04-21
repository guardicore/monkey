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

build {
    sources = [
        "source.googlecompute.tunneling-9"
    ]
    provisioner "ansible" {
        only = ["googlecompute.tunneling-9"]
        playbook_file = "./packer/setup_tunneling_9.yml"
    }
}
