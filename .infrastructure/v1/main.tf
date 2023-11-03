terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  name = "sl-vpc"
  cidr = "10.0.0.0/16"

  azs             = local.azs
  private_subnets = local.private_subnets
  public_subnets  = local.public_subnets

  enable_nat_gateway = true
  enable_vpn_gateway = true
}

module "ecr" {
  source = "./ecr"

  ecr_backend_repository_name = local.ecr_backend_repository_name
  ecr_frontend_repository_name = local.ecr_frontend_repository_name
  ecr_policy = local.ecr_policy
}

resource aws_security_group "alb_sg" {
  name        = "alb_sg"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = module.vpc.public_subnets_cidr_blocks
    ipv6_cidr_blocks = module.vpc.public_subnets_ipv6_cidr_blocks
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

module "db" {
  source = "terraform-aws-modules/rds/aws"

  identifier = "sl-db"

  engine            = "postgres"
  engine_version    = "15"
  instance_class    = "db.t3.micro"
  allocated_storage = 5

  db_name  = "sl"
  username = var.db_username
  password = var.db_password
  port     = 5432

  vpc_security_group_ids = [module.vpc.default_security_group_id]
  subnet_ids             = module.vpc.public_subnets
  create_db_subnet_group = true

  family = "postgres15"
  major_engine_version = "15.3"
  deletion_protection = false

  parameters = [
    {
      name         = "max_connections"
      value        = "20"
      apply_method = "pending-reboot"
    }
  ]
}

module "ecs" {
  source = "./ecs"

  subnet_ids                    = module.vpc.public_subnets
  backend_task_definition_path  = var.backend_task_definition_path
  frontend_task_definition_path = var.frontend_task_definition_path
  vpc_id                        = module.vpc.vpc_id
  target_group_arn     = module.alb.target_group_arn
  listener              = module.alb.listener
  backend_app_port              = 8000
  frontend_app_port             = 3000
}

module "alb" {
  source = "./alb"

  vpc_id = module.vpc.vpc_id
  alb_security_groups = [aws_security_group.alb_sg.id]
  alb_subnets = module.vpc.public_subnets
  frontend_target_id = module.ecs.frontend_target_id
  backend_target_id = module.ecs.backend_target_id
}


# TODO
# look into security groups, is ecs reachable, what ports and shit
