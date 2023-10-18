source "googlecompute" "island-linux-250" {
    image_name = "island-linux-250"
    project_id = "${var.project_id}"
    source_image = "ubuntu-2004-focal-v20230907"
    zone = "${var.zone}"
    disk_size = 10
    machine_type = "${var.machine_type}"
    ssh_username = "root"
    account_file = "${var.account_file}"
}

build {
    sources = [
        "source.googlecompute.island-linux-250"
    ]
    provisioner "ansible" {
        only = ["googlecompute.island-linux-250"]
        playbook_file = "${path.root}/setup_island_linux_250.yml"
    }
}
