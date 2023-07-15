terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

# Provider configuration
provider "aws" {
  region = "eu-west-2"
}

# VPC creation
resource "aws_vpc" "example_vpc" {
  cidr_block = "10.0.0.0/16"
}

# Subnet creation
resource "aws_subnet" "subnet_a" {
  vpc_id                  = aws_vpc.example_vpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "eu-west-2a"
}

resource "aws_subnet" "subnet_b" {
  vpc_id                  = aws_vpc.example_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-west-2b"
}

# Internet Gateway creation
resource "aws_internet_gateway" "example_gateway" {
  vpc_id = aws_vpc.example_vpc.id
}

# Route Table creation and association with Internet Gateway
resource "aws_route_table" "example_route_table" {
  vpc_id = aws_vpc.example_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.example_gateway.id
  }
}

resource "aws_route_table_association" "example_association_a" {
  subnet_id      = aws_subnet.subnet_a.id
  route_table_id = aws_route_table.example_route_table.id
}

resource "aws_route_table_association" "example_association_b" {
  subnet_id      = aws_subnet.subnet_b.id
  route_table_id = aws_route_table.example_route_table.id
}

# Frontend Load Balancer
resource "aws_lb" "frontend_lb" {
  name               = "frontend-lb"
  load_balancer_type = "application"
  subnets            = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]
}

# Backend Load Balancer
resource "aws_lb" "backend_lb" {
  name               = "backend-lb"
  load_balancer_type = "application"
  subnets            = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]
}

# Frontend Target Group
resource "aws_lb_target_group" "frontend_target_group" {
  name     = "frontend-target-group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.example_vpc.id
}

# Backend Target Group
resource "aws_lb_target_group" "backend_target_group" {
  name     = "backend-target-group"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.example_vpc.id
}

# Frontend Listener
resource "aws_lb_listener" "frontend_listener" {
  load_balancer_arn = aws_lb.frontend_lb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_lb_target_group.frontend_target_group.arn
    type             = "forward"
  }
}

# Backend Listener
resource "aws_lb_listener" "backend_listener" {
  load_balancer_arn = aws_lb.backend_lb.arn
  port              = 8080
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_lb_target_group.backend_target_group.arn
    type             = "forward"
  }
}

resource "aws_instance" "frontend_instance" {
  ami           = "ami-06464c878dbe46da4"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.subnet_a.id

  # Add any additional configuration for your frontend instance
}

resource "aws_instance" "backend_instance" {
  ami           = "ami-06464c878dbe46da4"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.subnet_b.id

  # Add any additional configuration for your backend instance
}
