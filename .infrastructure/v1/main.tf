terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

resource "aws_ecr_repository" "backend" {
  name = local.ecr_backend_repository_name
}

resource "aws_ecr_repository" "frontend" {
  name = local.ecr_frontend_repository_name
}

resource "aws_ecr_lifecycle_policy" "frontend_policy" {
  repository = aws_ecr_repository.frontend.name
  policy     = local.ecr_policy
}

resource "aws_ecr_lifecycle_policy" "backend_policy" {
  repository = aws_ecr_repository.backend.name
  policy     = local.ecr_policy
}


module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  name = "sl-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  private_subnets = local.private_subnets
  public_subnets  = local.public_subnets

  enable_nat_gateway = true
  enable_vpn_gateway = true
}

resource aws_security_group "alb_sg" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
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

#module "alb" {
#  source = "terraform-aws-modules/alb/aws"
#  version = "8.7.0"
#
#  name    = "sl-alb"
#  vpc_id  = module.vpc.vpc_id
#  subnets = module.vpc.public_subnets
#  security_groups = [module.vpc.default_security_group_id]
#
#  # Security Group
##  security_group_ingress_rules = {
##    all_http = {
##      from_port   = 80
##      to_port     = 80
##      ip_protocol = "tcp"
##      description = "HTTP web traffic"
##      cidr_ipv4   = "0.0.0.0/0"
##    }
##  }
##  security_group_egress_rules = {
##    all = {
##      ip_protocol = "-1"
##      cidr_ipv4   = "10.0.0.0/16"
##    }
##  }
#
#  http_tcp_listeners = [
#    {
#      port               = 80
#      protocol           = "HTTP"
#      target_group_index = 0
#    }
#  ]
#
#  target_groups = [
#    {
#      name_prefix      = "pref-"
#      backend_protocol = "HTTP"
#      backend_port     = 80
#      target_type      = "instance"
#      targets = {
#        my_target = {
#          target_id = aws_lb_target_group.tg.id
#          port = 80
#        }
#      }
#    }
#  ]
#
#  tags = {
#    Environment = "Development"
#    Project     = "Example"
#  }
#}
#
#resource "aws_lb_target_group" "tg" {
#  name     = "tf-example-lb-tg"
#  port     = 80
#  protocol = "HTTP"
#  vpc_id   = module.vpc.vpc_id
#}
#


#module "ecs" {
#  source  = "terraform-aws-modules/ecs/aws"
#  version = "5.2.2"
#
#  cluster_name = "ecs-sl"
#  #  create = false
#
#  cluster_configuration = {
#    execute_command_configuration = {
#      logging           = "OVERRIDE"
#      log_configuration = {
#        cloud_watch_log_group_name = "/aws/ecs/sl"
#      }
#    }
#  }
#
#  services = {
#    sl = {
#      cpu    = 512
#      memory = 1024
#
#      container_definitions = {
#        frontend = {
#          cpu           = 256
#          memory        = 512
#          essential     = true
#          image         = "${aws_ecr_repository.frontend.repository_url}:latest"
#          port_mappings = [
#            {
#              containerPort = 3000
#              protocol      = "tcp"
#            }
#          ]
#        }
#
#        backend = {
#          cpu       = 256
#          memory    = 512
#          essential = true
#          image     = "${aws_ecr_repository.backend.repository_url}:latest"
#
#          port_mappings = [
#            {
#              containerPort = 8000
#              protocol      = "tcp"
#            }
#          ]
#        }
#      }
#
#      #      service_connect_configuration = {
#      #        namespace = "example"  # todo this no wrkok
#      #        service   = {
#      #          client_alias = {
#      #            port     = 80
#      #            dns_name = "ecs-sample"
#      #          }
#      #          port_name      = "ecs-sample"
#      #          discovery_name = "ecs-sample"
#      #        }
#      #      }
#
#      load_balancer = {
#        service = {
#          target_group_arn = module.alb.target_group_arns[0]
#          container_name   = "backend"
#          container_port   = 8000
#        }
#      }
#
#      subnet_ids           = module.vpc.public_subnets
#      security_group_rules = {
#        alb_ingress_3000 = {
#          type                     = "ingress"
#          from_port                = 80
#          to_port                  = 80
#          protocol                 = "tcp"
#          description              = "Service port"
#          source_security_group_id = module.vpc.default_security_group_id
#        }
#        egress_all = {
#          type        = "egress"
#          from_port   = 0
#          to_port     = 0
#          protocol    = "-1"
#          cidr_blocks = ["0.0.0.0/0"]
#        }
#      }
#    }
#  }
#
#}

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
  port     = "5432"

  #  iam_database_authentication_enabled = true

  vpc_security_group_ids = [module.vpc.default_security_group_id]
  subnet_ids             = module.vpc.public_subnets
  create_db_subnet_group = true
  # DB subnet group
#  create_db_subnet_group = true

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
  backend_app_port              = 8000
  backend_target_group_arn      = module.alb.backend_target_group_arn
  frontend_app_port             = 3000
  frontend_target_group_arn     = module.alb.frontend_target_group_arn
  backend_listener              = module.alb.backend_listener
  frontend_listener             = module.alb.frontend_listener
}

module "alb" {
  source = "./alb"

  vpc_id = module.vpc.vpc_id
  alb_security_groups = [aws_security_group.alb_sg.id]
  alb_subnets = module.vpc.public_subnets
  frontend_target_id = module.ecs.frontend_target_id
  backend_target_id = module.ecs.backend_target_id
}


# eni???? to talk to ecs???
