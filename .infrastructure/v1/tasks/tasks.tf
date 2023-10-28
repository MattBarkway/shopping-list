resource "aws_ecs_task_definition" "frontend" {
  family                   = "frontend-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn        = var.ecs_execution_role_arn
  cpu = "256"
  memory = "512"

  container_definitions = local.frontend_task_definition
}

resource "aws_ecs_task_definition" "backend" {
  family                   = "backend-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn        = var.ecs_execution_role_arn
  cpu = "256"
  memory = "512"

  container_definitions = local.backend_task_definition
}

resource "aws_ecs_service" "frontend_service" {
  name            = "frontend-service"
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.frontend.arn
  launch_type     = "FARGATE"

  network_configuration {
    subnets = var.subnet_ids
    security_groups = var.security_groups
    assign_public_ip = true
  }

  depends_on = [var.ecs_execution_role_arn]
}

resource "aws_ecs_service" "backend_service" {
  name            = "backend-service"
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.backend.arn
  launch_type     = "FARGATE"

  network_configuration {
    subnets = var.subnet_ids
    security_groups = var.security_groups
  }

  depends_on = [var.ecs_execution_role_arn]
}
