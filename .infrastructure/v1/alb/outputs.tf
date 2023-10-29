output "alb_arn" {
  value = aws_alb.alb.arn
}

output "backend_target_group_arn" {
  value = aws_lb_target_group.backend_tg.arn
}

output "frontend_target_group_arn" {
  value = aws_lb_target_group.frontend_tg.arn
}

output "backend_listener" {
  value = aws_lb_listener.backend_listener.arn
}

output "frontend_listener" {
  value = aws_lb_listener.frontend_listener.arn
}
