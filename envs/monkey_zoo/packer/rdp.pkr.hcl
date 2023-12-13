source "googlecompute" "rdp-64" {
    image_name = "rdp-64"
    project_id = "${var.project_id}"
    source_image = "${var.windows_source_image}"
    zone = "${var.zone}"
    disk_size = 50
    machine_type = "${var.machine_type}"
    account_file = "${var.account_file}"
    communicator = "winrm"
    winrm_username = "${var.packer_username}"
    winrm_password = "${var.packer_user_password}"
    winrm_insecure = true
    winrm_use_ssl = true
    metadata = {
      sysprep-specialize-script-cmd = "winrm quickconfig -quiet & net user packer_user Passw0rd /add & net localgroup administrators packer_user /add & winrm set winrm/config/service/auth @{Basic=\"true\"}"
    }
}

source "googlecompute" "rdp-65" {
    image_name = "rdp-65"
    project_id = "${var.project_id}"
    source_image = "windows-2012-r2"  # We use Windows 2012 R2 because PTH over RDP works only on Windows 8.1 and Windows 2012 R2. We use custom Windows Server 2012 R2 image
    zone = "${var.zone}"
    disk_size = 50
    machine_type = "${var.machine_type}"
    account_file = "${var.account_file}"
    communicator = "winrm"
    winrm_username = "${var.packer_username}"
    winrm_password = "${var.packer_user_password}"
    winrm_insecure = true
    winrm_use_ssl = true
    metadata = {
      sysprep-specialize-script-cmd = "winrm quickconfig -quiet & net user packer_user Passw0rd /add & net localgroup administrators packer_user /add & winrm set winrm/config/service/auth @{Basic=\"true\"}"
    }
}


build {
    sources = [
        "source.googlecompute.rdp-64",
        "source.googlecompute.rdp-65"
    ]
    provisioner "ansible" {
        only = ["googlecompute.rdp-64"]
        use_proxy = false
        user = "${var.packer_username}"
        playbook_file = "${path.root}/setup_rdp_64.yml"
        ansible_env_vars = ["ANSIBLE_HOST_KEY_CHECKING=False"]
        extra_arguments = [
                "-e", "ansible_winrm_transport=ntlm ansible_winrm_server_cert_validation=ignore",
                "-e", "ansible_password=${var.packer_user_password}",
                "-vvv"
        ]
    }
    provisioner "ansible" {
        only = ["googlecompute.rdp-65"]
        use_proxy = false
        user = "${var.packer_username}"
        playbook_file = "${path.root}/setup_rdp_65.yml"
        ansible_env_vars = ["ANSIBLE_HOST_KEY_CHECKING=False"]
        extra_arguments = [
                "-e", "ansible_winrm_transport=ntlm ansible_winrm_server_cert_validation=ignore",
                "-e", "ansible_password=${var.packer_user_password}",
                "-vvv"
        ]
    }
}
