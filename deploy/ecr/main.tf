resource "aws_ecr_repository" "shopping_list_ecr" {
  name = var.ecr_repository_name
}
