# alb with target_group
resource "aws_alb" "alb" {
  name = "sl-alb"

  subnets = var.alb_subnets
  security_groups = var.alb_security_groups
}

## target group with type IP
#resource "aws_alb_target_group" "tg" {
#  name        = "tf-example-lb-tg"
#  port        = 80
#  protocol    = "HTTP"
#  target_type = "IP"
#  vpc_id      = var.vpc_id
#}
#
#
#resource "aws_alb_listener" "http_listener" {
#  load_balancer_arn = aws_alb.alb.arn
#}

# maybe add alb to service/container/task

# https://repost.aws/knowledge-center/create-alb-auto-register

# spurge
resource "aws_lb_target_group" "backend_tg" {
  name        = "backend"
  port        = "80"
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    path     = "/"
    protocol = "HTTP"
    interval = 60
  }
}

resource "aws_lb_target_group" "frontend_tg" {
  name        = "backend"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    path     = "/"
    protocol = "HTTP"
    interval = 60
  }
}

resource "aws_lb_target_group_attachment" "frontend_group_att" {
  target_group_arn = aws_lb_target_group.frontend_tg.arn
  target_id        = "10.0.101.15"
  port             = 80
}

resource "aws_lb_listener_rule" "frontend_listener_rule" {
  action {
    target_group_arn = aws_lb_target_group.frontend_tg.arn
    type             = "forward"
  }
  condition {
    path_pattern {
      values = ["/apitest*"]
    }
  }

  listener_arn = aws_lb_listener.frontend_listener.arn
  priority     = "3"
}

#resource "aws_acm_certificate" "cert" {
#  domain_name       = "example.com"
#  validation_method = "DNS"
#
#  tags = {
#    Environment = "test"
#  }
#
#  lifecycle {
#    create_before_destroy = true
#  }
#}

resource "aws_lb_listener" "frontend_listener" {
  load_balancer_arn = aws_alb.alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend_tg.arn
  }
}

resource "aws_lb_target_group_attachment" "backend_group_att" {
  target_group_arn = aws_lb_target_group.backend_tg.arn
  target_id        = "10.0.101.14"
  port             = 80
}

#resource "aws_network_interface" "eni_sl_backend" {
#  subnet_id       = var.alb_subnets[0]
#  private_ips     = ["10.0.101.14"]
#  security_groups = var.alb_security_groups
#
#  attachment {
#    instance     = var.backend_target_id
#    device_index = 1
#  }
#}

#resource "aws_network_interface" "eni_sl_frontend" {
#  subnet_id       = var.alb_subnets[0]
#  private_ips     = ["10.0.101.15"]
#  security_groups = var.alb_security_groups
#
#  attachment {
#    instance     = var.frontend_target_id
#    device_index = 1
#  }
#}

#resource "aws_lb_listener_rule" "backend_listener_rule" {
#  action {
#    target_group_arn = aws_lb_target_group.backend_tg.arn
#    type             = "forward"
#  }
#
#  listener_arn = aws_lb_listener.backend_listener.arn
#  priority     = "3"
#}

resource "aws_lb_listener" "backend_listener" {
  load_balancer_arn = aws_alb.alb.arn
  port              = "80"
  protocol          = "HTTP"
#  ssl_policy        = "ELBSecurityPolicy-2016-08"
#  certificate_arn   = aws_acm_certificate.cert.arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend_tg.arn
  }
}

#resource "aws_ecs_service" "service" {
#  name            = "apigatewaytest"
#  cluster         = var.cluster_id
#  task_definition = aws_ecs_task_definition.service.arn
#  desired_count   = var.task_count
#  launch_type     = "FARGATE"
#  network_configuration {
#    security_groups = [aws_security_group.ecs_task.id]
#    subnets         = module.vpc.private_subnets
#  }
#
#  load_balancer {
#    target_group_arn = aws_lb_target_group.apitest.arn
#    container_name   = "apigatewaytest"
#    container_port   = var.app_port
#  }
#}
##
