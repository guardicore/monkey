source "googlecompute" "mssql-16-1" {
  image_name     = "mssql-16-1"
  project_id     = "${var.project_id}"
  source_image   = "${var.windows_source_image}"
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
    sysprep-specialize-script-cmd = join(" & ", [
        "winrm quickconfig -quiet",
        "net user packer_user Passw0rd /add",
        "net localgroup administrators packer_user /add",
        "winrm set winrm/config/service @{AllowUnencrypted=\"true\"}",
        "winrm set winrm/config/client @{AllowUnencrypted=\"true\"}",
        "winrm set winrm/config/service/auth @{Basic=\"true\"}",
        "winrm set winrm/config/service/auth @{CredSSP=\"true\"}",
        "powershell -Command \"Set-Item WSMan:\\localhost\\Client\\TrustedHosts -Value * -Force\"",
        "powershell -Command \"Enable-WSManCredSSP -role server -force\"",
        "powershell -Command \"Restart-Service WinRM\""
    ])
  }
}

build {
  sources = [
    "source.googlecompute.mssql-16-1",
  ]
  provisioner "ansible" {
    only             = ["googlecompute.mssql-16-1"]
    use_proxy        = false
    user             = "${var.packer_username}"
    playbook_file    = "${path.root}/setup_mssql_16.yml"
    ansible_env_vars = ["ANSIBLE_HOST_KEY_CHECKING=False"]
    extra_arguments  = [
      "-e", "ansible_winrm_transport=credssp ansible_winrm_server_cert_validation=ignore",
      "-e", "ansible_password=${var.packer_user_password}",
      "-vvv"
    ]
  }
}
