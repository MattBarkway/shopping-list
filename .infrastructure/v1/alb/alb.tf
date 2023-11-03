resource "aws_alb" "alb" {
  name = "sl-alb"

  subnets = var.alb_subnets
  security_groups = var.alb_security_groups
}

resource "aws_lb_target_group" "sl_tg" {
  name        = "sl-target"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path     = "/"
    protocol = "HTTP"
    interval = 60
  }
}

resource "aws_lb_listener" "listener" {
  load_balancer_arn = aws_alb.alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.sl_tg.arn
  }
}
