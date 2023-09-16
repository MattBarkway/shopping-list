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
  enable_dns_hostnames = true
}

resource "aws_subnet" "subnet_a" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.0.0.0/24"
  availability_zone       = "eu-west-2a"
}

resource "aws_route_table_association" "subnet_a_association" {
  subnet_id      = aws_subnet.subnet_a.id
  route_table_id = aws_route_table.route_table.id
}

resource "aws_subnet" "subnet_b" {
  vpc_id                  = aws_vpc.vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-west-2b"
}

resource "aws_route_table_association" "subnet_b_association" {
  subnet_id      = aws_subnet.subnet_b.id
  route_table_id = aws_route_table.route_table.id
}

resource "aws_internet_gateway" "gateway" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table" "route_table" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gateway.id
  }
}

resource "aws_instance" "frontend_instance" {
  ami           = "ami-06464c878dbe46da4"
  instance_type = "t2.micro"
  associate_public_ip_address = true
  subnet_id     = aws_subnet.subnet_a.id
  key_name = "shopping-list"
  depends_on = [aws_internet_gateway.gateway]

  vpc_security_group_ids = [aws_security_group.frontend_sg.id]
  tags = {
    Name = "frontend-sl"
  }
}

resource "aws_instance" "backend_instance" {
  ami           = "ami-06464c878dbe46da4"
  instance_type = "t2.micro"
  associate_public_ip_address = true
  subnet_id     = aws_subnet.subnet_b.id
  key_name = "shopping-list"
  depends_on = [aws_internet_gateway.gateway]

  vpc_security_group_ids = [aws_security_group.backend_sg.id]
  tags = {
    Name = "backend-sl"
  }
}

resource "aws_security_group" "frontend_sg" {
  name        = "frontend-security-group"
  description = "Security group for the frontend instance"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
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
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
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

resource "aws_security_group" "db_sg" {
  name        = "rds-db-security-group"
  description = "Security group for the RDS database"

  vpc_id = aws_vpc.vpc.id

  ingress {
    from_port   = 5432
    to_port     = 5432
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

variable "db_password" {
  description = "The password for the RDS instance"
}

variable "db_username" {
  description = "The username for the RDS instance"
}

resource "aws_db_parameter_group" "db_params" {
  name        = "db-params"
  family      = "postgres15"
  description = "Parameter group for PostgreSQL"

  parameter {
    name  = "max_connections"
    value = "20"
    apply_method = "pending-reboot"
  }
}

resource "aws_db_subnet_group" "db_subnet_group" {
    name       = "postgresubgroup"
    subnet_ids = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]

    tags = {
        Name = "PostgreSQL subnet group"
    }
}

resource "aws_db_instance" "sl_db_instance" {
  identifier                = "sl-db"
  allocated_storage         = 10
  storage_type              = "gp2"
  engine                    = "postgres"
  engine_version            = "15.3"
  instance_class            = "db.t3.micro"
  username                  = var.db_username
  password                  = var.db_password
  parameter_group_name      = aws_db_parameter_group.db_params.name
  db_subnet_group_name      = aws_db_subnet_group.db_subnet_group.name
  vpc_security_group_ids    = [aws_security_group.db_sg.id]
  publicly_accessible       = false  // TODO change - figure out how to access
  backup_retention_period   = 7
  multi_az                  = false
  skip_final_snapshot       = true

  tags = {
    Name = "SLDB"
  }
}

