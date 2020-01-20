resource "aws_instance" "island_windows" {
  ami           = "ami-033b3ef27f8d1881d"
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

resource "aws_instance" "island_linux" {
  ami           = "ami-0495203541087740a"
  instance_type = "t2.micro"
  private_ip = "10.0.0.252"
  subnet_id = "${aws_subnet.main.id}"
  key_name = "monkey_maker"
  tags = {
    Name = "monkey_maker_linux"
  }
  vpc_security_group_ids = ["${aws_security_group.monkey_maker_sg.id}"]
  associate_public_ip_address = true
}
