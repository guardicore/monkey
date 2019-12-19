resource "aws_instance" "os_test_machine" {
  ami           = "${var.ami}"
  instance_type = "${var.type}"
  private_ip = "${var.ip}"
  subnet_id = "${data.aws_subnet.main.id}"
  key_name = "os_compat"
  tags = {
    Name = "os_compat_${var.name}"
    Purpose = "os_compat_instance"
  }
  vpc_security_group_ids = ["${data.aws_security_group.os_compat_instance.id}"]
  associate_public_ip_address = true
  user_data = "${var.user_data}"
}
