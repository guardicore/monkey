variable "ami" {type=string}
variable "ip" {type=string}
variable "name" {type=string}
variable "type" {
  type=string
  default="t2.micro"
}
variable "user_data" {
  type=string
  default=""
}
variable "env_vars" {
  type = object({
    subnet_id = string
    vpc_security_group_ids = string
  })
}

data "aws_subnet" "main" {
  id = "${var.env_vars.subnet_id}"
}

data "aws_security_group" "os_compat_instance" {
  id = "${var.env_vars.vpc_security_group_ids}"
}
