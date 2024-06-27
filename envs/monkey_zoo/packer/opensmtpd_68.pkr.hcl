source "googlecompute" "opensmtpd-68" {
    image_name = "opensmtpd-68"
    project_id = "${var.project_id}"
    source_image = "ubuntu-pro-1804-bionic-v20240618"
    zone = "${var.zone}"
    disk_size = 10
    machine_type = "${var.machine_type}"
    ssh_username = "root"
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
