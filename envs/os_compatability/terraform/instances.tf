resource "aws_instance" "island" {
  ami           = "ami-01cc9554aa0b4c00e"
  instance_type = "t2.micro"
  private_ip = "10.0.0.251"
  subnet_id = "${aws_subnet.main.id}"
  key_name = "os_compat"
  tags = {
    Name = "os_compat_ISLAND"
  }
  security_groups = ["${aws_security_group.os_compat_islad.id}"]
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
    security_group_id = "${aws_security_group.os_compat_instance.id}"
  }
}

module "ubuntu_12" {
  source = "./instance_template"
  name = "ubuntu_12"
  ami = "ami-003d0b1d"
  ip = "10.0.0.6"
  env_vars = "${local.env_vars}"
}

module "ubuntu_14" {
  source = "./instance_template"
  name = "ubuntu_14"
  ami = "ami-067ee10914e74ffee"
  ip = "10.0.0.7"
  env_vars = "${local.env_vars}"
}
