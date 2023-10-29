output "frontend_target_id" {
  value = aws_ecs_service.frontend_service.id
}

output "backend_target_id" {
  value = aws_ecs_service.backend_service.id
}
