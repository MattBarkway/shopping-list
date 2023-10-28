resource "aws_ecr_repository" "backend" {
  name = local.ecr_backend_repository_name
}

resource "aws_ecr_repository" "frontend" {
  name = local.ecr_frontend_repository_name
}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_ecs_cluster" "service_cluster" {
  name = "sl-cluster"
}

resource "aws_iam_role" "ecs_execution_role" {
  name = "ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy_attachment" "ecs_execution_role_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  roles       = [aws_iam_role.ecs_execution_role.name]
  name       = "ECSTaskExecutionRole"
}

resource "aws_iam_role_policy_attachment" "ecs_execution_role_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.ecs_execution_role.name
}

resource "aws_security_group" "ecs_sg" {
  name        = "ecs-sg"
  description = "ECS security group"

  vpc_id = var.vpc_id

  # Define your security group rules here
  # Example:
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Adjust for your needs
  }
}

#output "frontend_service_url" {
#  value = aws_ecs_service.frontend_service.endpoint
#}
#
#output "backend_service_url" {
#  value = aws_ecs_service.backend_service.endpoint
#}
