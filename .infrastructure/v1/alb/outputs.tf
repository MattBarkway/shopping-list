output "alb_arn" {
  value = aws_alb.alb.arn
}

output "target_group_arn" {
  value = aws_lb_target_group.sl_tg.arn
}

output "listener" {
  value = aws_lb_listener.listener.arn
}
