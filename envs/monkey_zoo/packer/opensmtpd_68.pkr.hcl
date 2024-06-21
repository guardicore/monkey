source "googlecompute" "opensmtpd-68" {
    image_name = "opensmtpd-68"
    project_id = "${var.project_id}"
    source_image = "debian-10-buster-v20240515"
    zone = "${var.zone}"
    disk_size = 10
    machine_type = "${var.machine_type}"
    ssh_username = "vzilius"
    account_file = "${var.account_file}"
}

build {
    sources = [
        "source.googlecompute.opensmtpd-68"
    ]
    provisioner "ansible" {
        only = ["googlecompute.opensmtpd-68"]
        playbook_file = "${path.root}/setup_opensmtpd_68.yml"
    }
}
