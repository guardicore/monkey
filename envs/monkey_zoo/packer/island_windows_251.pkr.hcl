source "googlecompute" "island-windows-251" {
  image_name     = "island-windows-251"
  project_id     = "${var.project_id}"
  source_image   = "windows-server-2016-dc-v20211216"
  zone           = "${var.zone}"
  disk_size      = 50
  machine_type   = "${var.machine_type}"
  account_file   = "${var.account_file}"
  communicator   = "winrm"
  winrm_username = "${var.packer_username}"
  winrm_password = "${var.packer_user_password}"
  winrm_insecure = true
  winrm_use_ssl  = true
  metadata       = {
    sysprep-specialize-script-cmd = "winrm quickconfig -quiet & net user packer_user Passw0rd /add & net localgroup administrators packer_user /add & winrm set winrm/config/service/auth @{Basic=\"true\"}"
  }
}

build {
  sources = [
    "source.googlecompute.island-windows-251",
  ]
  provisioner "ansible" {
    only             = ["googlecompute.island-windows-251"]
    use_proxy        = false
    user             = "${var.packer_username}"
    playbook_file    = "./packer/setup_island_windows_251.yml"
    ansible_env_vars = ["ANSIBLE_HOST_KEY_CHECKING=False"]
    extra_arguments  = [
      "-e", "ansible_winrm_transport=ntlm ansible_winrm_server_cert_validation=ignore",
      "-e", "ansible_password=${var.packer_user_password}",
      "-vvv"
    ]
  }
}
