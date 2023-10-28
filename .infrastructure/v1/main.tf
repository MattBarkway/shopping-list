terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

module "networking" {
  source = "./networking"
}

module "shopping-list" {
  source = "./full-stack-site"

  name                 = var.service_name
  db_password          = var.db_password
  db_username          = var.db_username
  db_family            = "postgres15"
  subnet_ids           = module.networking.public_subnet_ids
  vpc_id               = module.networking.vpc_id
  db_allocated_storage = 10
  db_storage_type      = "gp2"
  db_engine            = "postgres"
  db_engine_version    = "15.3"
  db_instance_class    = "db.t3.micro"
}

module "cluster-tasks" {
  source = "./tasks"

  cluster_id                    = module.shopping-list.cluster_id
  security_groups               = module.shopping-list.security_groups
  ecs_execution_role_arn        = module.shopping-list.ecs_execution_role_arn
  subnet_ids                    = module.networking.public_subnet_ids
  backend_task_definition_path  = var.backend_task_definition_path
  frontend_task_definition_path = var.frontend_task_definition_path
}
