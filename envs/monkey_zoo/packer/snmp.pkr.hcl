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
    default = "ubuntu-2004-focal-v20230302"
}
variable "account_file" {
    type = string
}

source "googlecompute" "snmp-manager" {
    image_name = "snmp-manager"
    project_id = "${var.project_id}"
    source_image = "${var.source_image}"
    zone = "${var.zone}"
    disk_size = 5
    machine_type = "${var.machine_type}"
    ssh_username = "root"
    account_file = "${var.account_file}"
}

source "googlecompute" "snmp-agent" {
    image_name = "snmp-agent"
    project_id = "${var.project_id}"
    source_image = "${var.source_image}"
    zone = "${var.zone}"
    disk_size = 5
    machine_type = "${var.machine_type}"
    ssh_username = "root"
    account_file = "${var.account_file}"
}

build {
    sources = [
        "source.googlecompute.snmp-manager",
        "source.googlecompute.snmp-agent"
    ]
    provisioner "ansible" {
        only = ["googlecompute.snmp-manager"]
        playbook_file = "./packer/setup_snmp_manager.yml"
    }
    provisioner "ansible" {
        only = ["googlecompute.snmp-agent"]
        playbook_file = "./packer/setup_snmp_agent.yml"
    }
}
