terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
}

resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "subnet_a" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "eu-west-2a"
}

resource "aws_subnet" "subnet_b" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-west-2b"
}

resource "aws_internet_gateway" "gateway" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_instance" "frontend_instance" {
  ami           = "ami-06464c878dbe46da4"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.subnet_a.id

  vpc_security_group_ids = [aws_security_group.frontend_sg.id]
}

resource "aws_instance" "backend_instance" {
  ami           = "ami-06464c878dbe46da4"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.subnet_b.id

  vpc_security_group_ids = [aws_security_group.backend_sg.id]
}

resource "aws_security_group" "frontend_sg" {
  name        = "frontend-security-group"
  description = "Security group for the frontend instance"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "backend_sg" {
  name        = "backend-security-group"
  description = "Security group for the backend instance"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
