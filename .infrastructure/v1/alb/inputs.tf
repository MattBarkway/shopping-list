variable "vpc_id" {
  type = string
}

variable "alb_subnets" {
  type = list(string)
}

variable "alb_security_groups" {
  type = list(string)
}

variable "frontend_target_id" {
  type = string
}

variable "backend_target_id" {
  type = string
}
