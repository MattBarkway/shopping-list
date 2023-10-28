variable "cluster_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_groups" {
  type = list(string)
}

variable "ecs_execution_role_arn" {
  type = string
}

variable "backend_task_definition_path" {
  type = string
}

variable "frontend_task_definition_path" {
  type = string
}
