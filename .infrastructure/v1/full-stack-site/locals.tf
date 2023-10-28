locals {
  ecr_backend_repository_name = "${var.name}-backend-ecr"
  ecr_frontend_repository_name = "${var.name}-frontend-ecr"
  db_security_group = aws_security_group.db_sg.id
  ecs_execution_role_arn = aws_iam_role.ecs_execution_role.arn
  cluster_id = aws_ecs_cluster.service_cluster.id
}
