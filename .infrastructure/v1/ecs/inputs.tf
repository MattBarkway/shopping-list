variable "subnet_ids" {
  type = list(string)
}

variable "vpc_id" {
  type = string
}

variable "backend_task_definition_path" {
  type = string
}

variable "frontend_task_definition_path" {
  type = string
}

variable "backend_app_port" {
  type = string
}

variable "target_group_arn" {
  type = string
}

variable "frontend_app_port" {
  type = string
}

variable "listener" {
  type = string
}
