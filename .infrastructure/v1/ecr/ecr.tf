resource "aws_ecr_repository" "backend" {
  name = var.ecr_backend_repository_name
}

resource "aws_ecr_repository" "frontend" {
  name = var.ecr_frontend_repository_name
}

resource "aws_ecr_lifecycle_policy" "frontend_policy" {
  repository = aws_ecr_repository.frontend.name
  policy     = var.ecr_policy
}

resource "aws_ecr_lifecycle_policy" "backend_policy" {
  repository = aws_ecr_repository.backend.name
  policy     = var.ecr_policy
}
