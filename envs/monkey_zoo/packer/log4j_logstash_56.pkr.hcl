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
    type = string
    default = "europe-west1-b"
}
variable "machine_type" {
    type = string
    default = "e2-standard-4"
}
variable "source_image" {
    type = string
    default = "windows-server-2016-dc-v20211216"
}
variable "account_file" {
    type = string
}
variable "packer_username" {
    type = string
    default = "packer_user"
}
variable "packer_user_password" {
    type = string
    default = "Passw0rd"
}

source "googlecompute" "log4j-logstash-56-test" {
  image_name     = "log4j-logstash-56-test"
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
    "source.googlecompute.log4j-logstash-56-test",
  ]
  provisioner "ansible" {
    only             = ["googlecompute.log4j-logstash-56-test"]
    use_proxy        = false
    user             = "${var.packer_username}"
    playbook_file    = "${path.root}/setup_log4j_logstash_56.yml"
    ansible_env_vars = ["ANSIBLE_HOST_KEY_CHECKING=False"]
    extra_arguments  = [
      "-e", "ansible_winrm_transport=ntlm ansible_winrm_server_cert_validation=ignore",
      "-e", "ansible_password=${var.packer_user_password}",
      "-vvv"
    ]
  }
}
