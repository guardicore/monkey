variable "ami" {type=string}
variable "ip" {type=string}
variable "name" {type=string}
variable "env_vars" {
  type = object({
    subnet_id = string
    security_group_id = string
  })
}

data "aws_subnet" "main" {
  id = "${var.env_vars.subnet_id}"
}

data "aws_security_group" "os_compat_instance" {
  id = "${var.env_vars.security_group_id}"
}
