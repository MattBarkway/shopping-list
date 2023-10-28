locals {
    frontend_task_definition = file(var.frontend_task_definition_path)
    backend_task_definition = file(var.backend_task_definition_path)
}
