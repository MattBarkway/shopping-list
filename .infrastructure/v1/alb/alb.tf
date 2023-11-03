resource "aws_alb" "alb" {
  name = "sl-alb"

  internal = false
  subnets = var.alb_subnets
  security_groups = var.alb_security_groups
}

resource "aws_lb_target_group" "frontend_tg" {
  name        = "sl-target"
  port        = 3000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path     = "/"
    protocol = "HTTP"
    interval = 60
  }
}

resource "aws_lb_target_group" "backend_tg" {
  name        = "backend-target"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path     = "/"
    protocol = "HTTP"
    interval = 60
  }
}

# Attach the target groups to the ALB listeners
resource "aws_lb_listener" "frontend_listener" {
  load_balancer_arn = aws_alb.alb.arn
  port             = 80
  protocol         = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend_tg.arn
  }
}

resource "aws_lb_listener" "backend_listener" {
  load_balancer_arn = aws_alb.alb.arn
  port              = 8000
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_tg.arn
  }
}

resource "aws_lb_listener_rule" "backend_listener_rule" {
  listener_arn = aws_lb_listener.backend_listener.arn
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_tg.arn
  }

  condition {
    path_pattern {
      values = ["/api"]
    }
  }
}
