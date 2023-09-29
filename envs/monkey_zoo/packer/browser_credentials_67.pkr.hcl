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

source "googlecompute" "browser-credentials-67" {
    image_name = "browser-credentials-67"
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
        "source.googlecompute.browser-credentials-67"
    ]
    provisioner "ansible" {
        only = ["googlecompute.browser-credentials-67"]
        playbook_file = "${path.root}/setup_browser_credentials_67.yml"
    }
}
