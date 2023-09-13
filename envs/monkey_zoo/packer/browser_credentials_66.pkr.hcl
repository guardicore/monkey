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
    elevated_user = "m0nk3y"
    elevated_password = "P@ssw0rd!"
    inline = [
      "$process = Start-Process \"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" -ArgumentList \"-first-run\" -PassThru",
      "Start-Sleep -Seconds 10",
      "$process",
      "Stop-Process -Id $process.Id",
    ]
  }

  provisioner "file" {
    only   = ["googlecompute.browser-credentials-66"]
    source = "./packer/files/chrome-creds.ps1"
    destination = "C:\\Users\\m0nk3y\\Desktop\\chrome-creds.ps1"
  }

  provisioner "file" {
    only   = ["googlecompute.browser-credentials-66"]
    source = "./packer/files/System.Data.SQLite.dll"
    destination = "C:\\Users\\m0nk3y\\Desktop\\System.Data.SQLite.dll"
  }

  provisioner "powershell" {
    only   = ["googlecompute.browser-credentials-66"]
    elevated_user = "m0nk3y"
    elevated_password = "P@ssw0rd!"
    inline = [
      "Set-Location C:\\Users\\m0nk3y\\Desktop",
      "pwsh -Command {",
      <<EOF
      ./chrome-creds.ps1 -Command Import `
        -origin_url forBBtests.com `
        -action_url forBBtests.com `
        -username_element username `
        -username_value forBBtests `
        -password_element password `
        -password_value supersecret `
        -submit_element "" `
        -signon_realm forBBtests.com `
        -blacklisted_by_user 0 `
        -scheme 0 `
        -password_type 0 `
        -times_used 1 `
        -form_data 3401000007000000050000006C006F00670069006E0000002300000068747470733A2F2F64656D6F2E74657374666972652E6E65742F6C6F67696E2E6A7370002100000068747470733A2F2F64656D6F2E74657374666972652E6E65742F646F4C6F67696E00000002000000090000000000000003000000750069006400000000000000040000007465787400000000FFFFFF7F00000000000000000000000001000000010000000100000002000000000000000000000000000000200000000000000000000000090000000000000005000000700061007300730077000000000000000800000070617373776F726400000000FFFFFF7F0000000000000000000000000100000001000000010000000200000000000000000000000000000020000000000000000000000001000000040000006E756C6C `
        -display_name "" `
        -icon_url "" `
        -federation_url "" `
        -skip_zero_click 0 `
        -generation_upload_status 0 `
        -possible_username_pairs 00000000 `
        -moving_blocked_for 00000000
      EOF
      ,
      <<EOF
      ./chrome-creds.ps1 -Command Import `
        -origin_url https://www.w3schools.com/howto/howto_css_login_form.asp `
        -action_url https://www.w3schools.com/howto/howto_css_login_form.asp `
        -username_element username `
        -username_value usernameFromForm `
        -password_element password `
        -password_value passwordFromForm `
        -submit_element "" `
        -signon_realm https://www.w3schools.com `
        -blacklisted_by_user 0 `
        -scheme 0 `
        -password_type 0 `
        -times_used 2 `
        -form_data 3401000007000000050000006C006F00670069006E0000002300000068747470733A2F2F64656D6F2E74657374666972652E6E65742F6C6F67696E2E6A7370002100000068747470733A2F2F64656D6F2E74657374666972652E6E65742F646F4C6F67696E00000002000000090000000000000003000000750069006400000000000000040000007465787400000000FFFFFF7F00000000000000000000000001000000010000000100000002000000000000000000000000000000200000000000000000000000090000000000000005000000700061007300730077000000000000000800000070617373776F726400000000FFFFFF7F0000000000000000000000000100000001000000010000000200000000000000000000000000000020000000000000000000000001000000040000006E756C6C `
        -display_name "" `
        -icon_url "" `
        -federation_url "" `
        -skip_zero_click 0 `
        -generation_upload_status 0 `
        -possible_username_pairs 00000000 `
        -moving_blocked_for 00000000
      EOF
      ,
      "}",
    ]
  }

}
