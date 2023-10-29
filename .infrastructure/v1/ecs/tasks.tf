resource "aws_security_group" "frontend_sg" {
  name        = "frontend-sg"
  description = "ECS security group"

  vpc_id = var.vpc_id

  ingress {
    from_port   = 3000
    to_port     = 3000
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
  name        = "backend-sg"
  description = "ECS security group"

  vpc_id = var.vpc_id

  ingress {
    from_port   = var.backend_app_port
    to_port     = var.backend_app_port
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

resource "aws_ecs_service" "frontend_service" {
  name                               = "frontend-service"
  cluster                            = local.cluster_id
  task_definition                    = aws_ecs_task_definition.frontend.arn
  desired_count                      = 1
  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 100

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = [aws_security_group.frontend_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = var.frontend_target_group_arn
    container_name   = "frontend"
    container_port   = 3000
  }

  depends_on = [local.ecs_execution_role_arn, var.frontend_listener]
}

resource "aws_ecs_task_definition" "frontend" {
  family                   = "frontend"
  network_mode             = "awsvpc"
  execution_role_arn       = local.ecs_execution_role_arn
  cpu                      = "256"
  memory                   = "512"

  container_definitions = local.frontend_task_definition
}

resource "aws_ecs_service" "backend_service" {
  name                               = "backend-service"
  cluster                            = local.cluster_id
  task_definition                    = aws_ecs_task_definition.backend.arn
  desired_count                      = 1
  deployment_maximum_percent         = 200
  deployment_minimum_healthy_percent = 100

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = [aws_security_group.backend_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = var.backend_target_group_arn
    container_name   = "backend"
    container_port   = 8000
  }

  depends_on = [local.ecs_execution_role_arn, var.backend_listener]
}

resource "aws_ecs_task_definition" "backend" {
  family                   = "backend"
  network_mode             = "awsvpc"
  execution_role_arn       = local.ecs_execution_role_arn
  cpu                      = "256"
  memory                   = "512"

  container_definitions = local.backend_task_definition
}


resource "aws_cloudwatch_log_group" "sl_logs" {
  name              = "/ecs/sl-logs"
  retention_in_days = 7
}
