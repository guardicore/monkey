// Instances of machines in os_compat environment
// !!! Don't forget to add machines to test_compatibility.py if you add here !!!


resource "aws_instance" "island" {
  ami           = "ami-004f0217ce761fc9a"
  instance_type = "t2.micro"
  private_ip = "10.0.0.251"
  subnet_id = "${aws_subnet.main.id}"
  key_name = "os_compat"
  tags = {
    Name = "os_compat_ISLAND"
  }
  vpc_security_group_ids = ["${aws_security_group.os_compat_island.id}"]
  associate_public_ip_address = true
  root_block_device {
    volume_size           = "30"
    volume_type           = "standard"
    delete_on_termination = true
  }
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
rm ./monkey-linux-64
wget --no-check-certificate -q https://10.0.0.251:5000/api/monkey/download/monkey-linux-64 -O ./monkey-linux-64 || curl https://10.0.0.251:5000/api/monkey/download/monkey-linux-64 -k -o monkey-linux-64
chmod +x ./monkey-linux-64
./monkey-linux-64 m0nk3y -s 10.0.0.251:5000
--//
EOF

  user_data_linux_32 = <<EOF
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
rm ./monkey-linux-32
wget --no-check-certificate -q https://10.0.0.251:5000/api/monkey/download/monkey-linux-32 -O ./monkey-linux-32 || curl https://10.0.0.251:5000/api/monkey/download/monkey-linux-32 -k -o monkey-linux-32
chmod +x ./monkey-linux-32
./monkey-linux-32 m0nk3y -s 10.0.0.251:5000
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
}

module "centos_6" {
  source = "./instance_template"
  name = "centos_6"
  ami = "ami-07fa74e425f2abf29"
  ip = "10.0.0.36"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "centos_7" {
  source = "./instance_template"
  name = "centos_7"
  ami = "ami-0034b52a39b9fb0e8"
  ip = "10.0.0.37"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "centos_8" {
  source = "./instance_template"
  name = "centos_8"
  ami = "ami-0034c84e4e9c557bd"
  ip = "10.0.0.38"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "suse_12" {
  source = "./instance_template"
  name = "suse_12"
  ami = "ami-07b12b913a7e36b08"
  ip = "10.0.0.42"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "suse_11" {
  source = "./instance_template"
  name = "suse_11"
  ami = "ami-0083986c"
  ip = "10.0.0.41"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "kali_2019" {
  source = "./instance_template"
  name = "kali_2019"
  ami = "ami-05d64b1d0f967d4bf"
  ip = "10.0.0.99"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

// Requires m3.medium which usually isn't available
//module "rhel_5" {
//  source = "./instance_template"
//  name = "rhel_5"
//  ami = "ami-a48cbfb9"
//  type = "m3.medium"
//  ip = "10.0.0.85"
//  env_vars = "${local.env_vars}"
//  user_data = "${local.user_data_linux_64}"
//}

module "rhel_6" {
  source = "./instance_template"
  name = "rhel_6"
  ami = "ami-0af3f0e0918f47bcf"
  ip = "10.0.0.86"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "rhel_7" {
  source = "./instance_template"
  name = "rhel_7"
  ami = "ami-0b5edb134b768706c"
  ip = "10.0.0.87"
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

module "debian_7" {
  source = "./instance_template"
  name = "debian_7"
  ami = "ami-0badcc5b522737046"
  ip = "10.0.0.77"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "debian_8" {
  source = "./instance_template"
  name = "debian_8"
  ami = "ami-0badcc5b522737046"
  ip = "10.0.0.78"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "debian_9" {
  source = "./instance_template"
  name = "debian_9"
  ami = "ami-0badcc5b522737046"
  ip = "10.0.0.79"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "oracle_6" {
  source = "./instance_template"
  name = "oracle_6"
  ami = "ami-0f9b69f34108a3770"
  ip = "10.0.0.66"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_linux_64}"
}

module "oracle_7" {
  source = "./instance_template"
  name = "oracle_7"
  ami = "ami-001e494dc0f3372bc"
  ip = "10.0.0.67"
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

// Requires m3.medium instance which usually isn't available
// module "ubuntu_12_32" {
//   source = "./instance_template"
//   name = "ubuntu_12_32"
//   ami = "ami-06003c1b"
//   ip = "10.0.0.23"
//   env_vars = "${local.env_vars}"
//   user_data = "${local.user_data_linux_32}"
// }

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

module "windows_2003_r2_32" {
  source = "./instance_template"
  name = "windows_2003_r2_32"
  ami = "ami-01e4fa6d"
  ip = "10.0.0.4"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}

module "windows_2003" {
  source = "./instance_template"
  name = "windows_2003"
  ami = "ami-9e023183"
  ip = "10.0.0.5"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}

module "windows_2008_r2" {
  source = "./instance_template"
  name = "windows_2008_r2"
  ami = "ami-05af5509c2c73e36e"
  ip = "10.0.0.8"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}


module "windows_2008_32" {
  source = "./instance_template"
  name = "windows_2008_32"
  ami = "ami-3606352b"
  ip = "10.0.0.6"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_32}"
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

module "windows_2016" {
  source = "./instance_template"
  name = "windows_2016"
  ami = "ami-02a6791b44938cfcd"
  ip = "10.0.0.116"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}

module "windows_2019" {
  source = "./instance_template"
  name = "windows_2019"
  ami = "ami-09fe2745618d2af42"
  ip = "10.0.0.119"
  env_vars = "${local.env_vars}"
  user_data = "${local.user_data_windows_64}"
}
