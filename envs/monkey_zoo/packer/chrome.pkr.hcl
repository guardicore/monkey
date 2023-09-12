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
    default = "ubuntu-2004-focal-v20230907"
}
variable "account_file" {
    type = string
}

source "googlecompute" "chrome-70" {
    image_name = "chrome-70"
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
        "source.googlecompute.chrome-70"
    ]
    provisioner "ansible" {
        only = ["googlecompute.chrome-70"]
        playbook_file = "./packer/setup_chrome_linux.yml"
    }
}
