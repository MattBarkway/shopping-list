terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

# Provider configuration
provider "aws" {
  region = "eu-west-2"
}

resource "aws_ecr_repository" "shopping_list_backend_ecr" {
  name = var.ecr_backend_repository_name
}

resource "aws_ecr_repository" "shopping_list_frontend_ecr" {
  name = var.ecr_frontend_repository_name
}