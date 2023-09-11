packer {
  required_plugins {
    googlecompute = {
      source  = "github.com/hashicorp/googlecompute"
      version = "~> 1"
    }
    ansible = {
      source  = "github.com/hashicorp/ansible"
      version = "~> 1"
    }
  }
}

variable "project_id" {
  type = string
}
variable "zone" {
  type    = string
  default = "europe-west1-b"
}
variable "machine_type" {
  type    = string
  default = "e2-standard-4"
}
variable "source_image" {
  type    = string
  default = "windows-server-2016-dc-v20211216"
}
variable "account_file" {
  type = string
}
variable "packer_username" {
  type    = string
  default = "packer_user"
}
variable "packer_user_password" {
  type    = string
  default = "Passw0rd"
}


source "googlecompute" "browser-credentials-66" {
  image_name     = "browser-credentials-66"
  project_id     = "${var.project_id}"
  source_image   = "${var.source_image}"
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
    "source.googlecompute.browser-credentials-66",
  ]
  provisioner "ansible" {
    only             = ["googlecompute.browser-credentials-66"]
    use_proxy        = false
    user             = "${var.packer_username}"
    playbook_file    = "./packer/setup_browser_credentials_66.yml"
    ansible_env_vars = ["ANSIBLE_HOST_KEY_CHECKING=False"]
    extra_arguments  = [
      "-e", "ansible_winrm_transport=ntlm ansible_winrm_server_cert_validation=ignore",
      "-e", "ansible_password=${var.packer_user_password}",
      "-vvv"
    ]
  }

  provisioner "powershell" {
    only   = ["googlecompute.browser-credentials-66"]
    inline = [
      "$LocalTempDir = $env:TEMP",
      "$ChromeInstaller = \"ChromeInstaller.exe\"",
      "(new-object System.Net.WebClient).DownloadFile(\"http://dl.google.com/chrome/install/latest/chrome_installer.exe\", \"$LocalTempDir\\$ChromeInstaller\")",
      "& \"$LocalTempDir\\$ChromeInstaller\" /silent /install",
    ]
  }

  provisioner "powershell" {
    only   = ["googlecompute.browser-credentials-66"]
    inline = [
      "$username = \"m0nk3y\"",
      "$password = \"P@ssw0rd!\"",
      "$securePassword = ConvertTo-SecureString $password -AsPlainText -Force",
      "$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword",
      "Start-Process \"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" -Credential $credential"
    ]
  }
  provisioner "file" {
    only   = ["googlecompute.browser-credentials-66"]
    source = "./packer/files/Login Data"
    destination = "C:\\Users\\m0nk3y\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
  }
  provisioner "file" {
    only   = ["googlecompute.browser-credentials-66"]
    source = "./packer/files/Local State"
    destination = "C:\\Users\\m0nk3y\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"
  }
}
