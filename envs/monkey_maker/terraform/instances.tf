resource "aws_instance" "island_windows" {
  ami           = "ami-09fe2745618d2af42"
  instance_type = "t2.micro"
  private_ip = "10.0.0.251"
  subnet_id = "${aws_subnet.main.id}"
  key_name = "monkey_maker"
  tags = {
    Name = "monkey_maker_windows"
  }
  vpc_security_group_ids = ["${aws_security_group.monkey_maker_sg.id}"]
  associate_public_ip_address = true
}

resource "aws_instance" "island_linux_64" {
  ami           = "ami-050a22b7e0cf85dd0"
  instance_type = "t2.micro"
  private_ip = "10.0.0.252"
  subnet_id = "${aws_subnet.main.id}"
  key_name = "monkey_maker"
  tags = {
    Name = "monkey_maker_linux_64"
  }
  vpc_security_group_ids = ["${aws_security_group.monkey_maker_sg.id}"]
  associate_public_ip_address = true
}
