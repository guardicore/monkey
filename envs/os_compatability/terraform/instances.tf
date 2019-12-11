resource "aws_instance" "island" {
  ami           = "ami-01cc9554aa0b4c00e"
  instance_type = "t2.micro"
  private_ip = "10.0.0.251"
  subnet_id = "${aws_subnet.main.id}"
  key_name = "os_compat"
  tags = {
    Name = "os_compat_ISLAND"
  }
  vpc_security_group_ids = ["${aws_security_group.os_compat_islad.id}"]
  associate_public_ip_address = true
  root_block_device {
    volume_size           = "30"
    volume_type           = "standard"
    delete_on_termination = true
  }
  #associate_public_ip_address = false
}

locals {
  env_vars = {
    subnet_id = "${aws_subnet.main.id}"
    vpc_security_group_ids = "${aws_security_group.os_compat_instance.id}"
  }

  user_data_linux_64 = <<EOF
Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"
#!/bin/bash
wget --no-check-certificate https://10.0.0.251:5000/api/monkey/download/monkey-linux-64 || curl https://10.0.0.251:5000/api/monkey/download/monkey-linux-64 -k -o monkey-linux-64
chmod +x ./monkey-linux-64
./monkey-linux-64 m0nk3y -s 10.0.0.251:5000
--//
EOF

  user_data_windows_64 = <<EOF
<powershell>
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue
Invoke-WebRequest -Uri 'https://10.0.0.251:5000/api/monkey/download/monkey-windows-64.exe' -OutFile 'C:\windows\temp\monkey-windows-64.exe' -UseBasicParsing
C:\windows\temp\monkey-windows-64.exe m0nk3y -s 10.0.0.251:5000
</powershell>
<persist>true</persist>
EOF

  user_data_windows_32 = <<EOF
<powershell>
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@
[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue
Invoke-WebRequest -Uri 'https://10.0.0.251:5000/api/monkey/download/monkey-windows-32.exe' -OutFile 'C:\windows\temp\monkey-windows-32.exe' -UseBasicParsing
C:\windows\temp\monkey-windows-32.exe m0nk3y -s 10.0.0.251:5000
</powershell>
<persist>true</persist>
EOF

user_data_windows_bits_32 = <<EOF
<script>
bitsadmin /transfer Update /download /priority high https://10.0.0.251:5000/api/monkey/download/monkey-windows-32.exe C:\windows\temp\monkey-windows-32.exe
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/guardicore/monkey/releases/download/1.6/monkey-linux-32', 'package.zip')"
C:\windows\temp\monkey-windows-32.exe m0nk3y -s 10.0.0.251:5000
</script>
<persist>true</persist>
EOF
}

module "kali_2019" {
  source = "./instance_template"
  name = "kali_2019"
  ami = "ami-05d64b1d0f967d4bf"
  ip = "10.0.0.99"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "rhel_8" {
  source = "./instance_template"
  name = "rhel_8"
  ami = "ami-0badcc5b522737046"
  ip = "10.0.0.88"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "ubuntu_12" {
  source = "./instance_template"
  name = "ubuntu_12"
  ami = "ami-003d0b1d"
  ip = "10.0.0.22"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "ubuntu_14" {
  source = "./instance_template"
  name = "ubuntu_14"
  ami = "ami-067ee10914e74ffee"
  ip = "10.0.0.24"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "ubuntu_19" {
  source = "./instance_template"
  name = "ubuntu_19"
  ami = "ami-001b87954b72ea3ac"
  ip = "10.0.0.29"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "centos" {
  source = "./instance_template"
  name = "centos_8"
  ami = "ami-0034c84e4e9c557bd"
  ip = "10.0.0.33"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}


module "windows_2003_r2_32" {
  source = "./instance_template"
  name = "windows_2003_r2_32"
  ami = "ami-01e4fa6d"
  ip = "10.0.0.4"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}

module "windows_2008" {
  source = "./instance_template"
  name = "windows_2008"
  ami = "ami-0d8c60e4d3ca36ed6"
  ip = "10.0.0.8"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}

module "windows_2008_r2" {
  source = "./instance_template"
  name = "windows_2008_r2"
  ami = "ami-0252def122d07efd3"
  ip = "10.0.0.7"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}

module "windows_2012" {
  source = "./instance_template"
  name = "windows_2012"
  ami = "ami-0d8c60e4d3ca36ed6"
  ip = "10.0.0.12"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}

module "windows_2012_r2" {
  source = "./instance_template"
  name = "windows_2012_r2"
  ami = "ami-08dcceb529e70f875"
  ip = "10.0.0.11"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}

module "windows_2019" {
  source = "./instance_template"
  name = "windows_2019"
  ami = "ami-09fe2745618d2af42"
  ip = "10.0.0.19"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}
