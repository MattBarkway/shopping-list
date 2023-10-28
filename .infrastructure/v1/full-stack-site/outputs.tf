output "ecr_backend_repository_name" {
  value = local.ecr_backend_repository_name
}

output "ecr_frontend_repository_name" {
  value = local.ecr_frontend_repository_name
}

output "cluster_id" {
  value = local.cluster_id
}

output "ecs_execution_role_arn" {
  value = local.ecs_execution_role_arn
}

output "security_groups" {
  value = local.security_groups
}
