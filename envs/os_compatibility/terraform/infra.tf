resource "aws_vpc" "os_compat_vpc" {
  cidr_block = "10.0.0.0/24"
  enable_dns_support = true
  tags = {
    Name = "os_compat_vpc"
  }
}

resource "aws_internet_gateway" "os_compat_gateway" {
  vpc_id = "${aws_vpc.os_compat_vpc.id}"

  tags = {
    Name = "os_compat_gateway"
  }
}

// create routing table which points to the internet gateway
resource "aws_route_table" "os_compat_route" {
  vpc_id = "${aws_vpc.os_compat_vpc.id}"

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.os_compat_gateway.id}"
  }

  tags = {
    Name = "os_compat_route"
  }
}

// associate the routing table with the subnet
resource "aws_route_table_association" "subnet-association" {
  subnet_id      = "${aws_subnet.main.id}"
  route_table_id = "${aws_route_table.os_compat_route.id}"
}

resource "aws_subnet" "main" {
  vpc_id     = "${aws_vpc.os_compat_vpc.id}"
  cidr_block = "10.0.0.0/24"

  tags = {
    Name = "Main"
  }
}

resource "aws_security_group" "os_compat_island" {
  name        = "os_compat_island"
  description = "Allow remote access to the island"
  vpc_id      = "${aws_vpc.os_compat_vpc.id}"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.0.0.0/24"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "os_compat_island"
  }
}

resource "aws_security_group" "os_compat_instance" {
  name        = "os_compat_instance"
  description = "Allow remote access to the machines"
  vpc_id      = "${aws_vpc.os_compat_vpc.id}"

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.0.0.0/24"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "os_compat_instance"
  }
}
