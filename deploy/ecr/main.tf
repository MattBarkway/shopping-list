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

resource "aws_ecr_repository" "shopping_list_ecr" {
  name = var.ecr_repository_name
}
