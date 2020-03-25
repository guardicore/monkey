resource "aws_vpc" "monkey_maker" {
  cidr_block = "10.0.0.0/24"
  enable_dns_support = true
  tags = {
    Name = "monkey_maker_vpc"
  }
}

resource "aws_internet_gateway" "monkey_maker_gateway" {
  vpc_id = "${aws_vpc.monkey_maker.id}"

  tags = {
    Name = "monkey_maker_gateway"
  }
}

// create routing table which points to the internet gateway
resource "aws_route_table" "monkey_maker_route" {
  vpc_id = "${aws_vpc.monkey_maker.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.monkey_maker_gateway.id}"
  }

  tags = {
    Name = "monkey_maker_route"
  }
}

// associate the routing table with the subnet
resource "aws_route_table_association" "subnet-association" {
  subnet_id      = "${aws_subnet.main.id}"
  route_table_id = "${aws_route_table.monkey_maker_route.id}"
}

resource "aws_subnet" "main" {
  vpc_id     = "${aws_vpc.monkey_maker.id}"
  cidr_block = "10.0.0.0/24"

  tags = {
    Name = "Main"
  }
}

resource "aws_security_group" "monkey_maker_sg" {
  name        = "monkey_maker_sg"
  description = "Allow remote access to the island"
  vpc_id      = "${aws_vpc.monkey_maker.id}"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "monkey_maker_sg"
  }
}
