terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

module "ecr" {
  source = "../ecr"
}

# Provider configuration
provider "aws" {
  region = "us-west-2"
}

# VPC creation
resource "aws_vpc" "example_vpc" {
  cidr_block = "10.0.0.0/16"
}

# Subnet creation
resource "aws_subnet" "sl_subnet" {
  vpc_id                  = aws_vpc.example_vpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "us-west-2a"
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

resource "aws_route_table_association" "example_association" {
  subnet_id      = aws_subnet.sl_subnet.id
  route_table_id = aws_route_table.example_route_table.id
}

# Frontend Load Balancer
resource "aws_lb" "frontend_lb" {
  name               = "frontend-lb"
  load_balancer_type = "application"
  subnets            = [aws_subnet.sl_subnet.id]
}

# Backend Load Balancer
resource "aws_lb" "backend_lb" {
  name               = "backend-lb"
  load_balancer_type = "application"
  subnets            = [aws_subnet.sl_subnet.id]
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
  ami           = aws_ecr_repository.e.name + ":" + var.ecr_image_name + ":" + var.ecr_image_tag
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.sl_subnet.id

  # Add any additional configuration for your frontend instance
}


resource "aws_instance" "frontend_instance" {
  ami           = data.aws_ecr_image.frontend_image.image_digest
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.sl_subnet.id

  # Add any additional configuration for your frontend instance
}

resource "aws_instance" "backend_instance" {
  count         = data.aws_ecr_repository_image.latest_image.image_digest != "" ? 1 : 0
  ami           = data.aws_ecr_image.backend_image.image_digest
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.sl_subnet.id

  # Add any additional configuration for your backend instance
}

data "aws_ecr_image" "backend_image" {
  repository_name = ecr..name
  image_tag       = "latest"  # Replace with the desired image tag
}

data "aws_ecr_image" "frontend_image" {
  repository_name = ecr.ecr_repository_name
  image_tag       = "latest"  # Replace with the desired image tag
}
