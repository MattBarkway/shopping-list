locals {
    frontend_task_definition = file(var.frontend_task_definition_path)
    backend_task_definition = file(var.backend_task_definition_path)
    ecs_execution_role_arn = aws_iam_role.ecs_execution_role.arn
    cluster_id = aws_ecs_cluster.service_cluster.id
}
