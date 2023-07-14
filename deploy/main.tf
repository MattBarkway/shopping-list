# Define the AWS provider
provider "aws" {
  region = "us-west-2"  # Replace with your desired AWS region
}

# Declare the module blocks for the ECR module and service module
module "ecr" {
  source = "./ecr"

  ecr_repository_name = "ecr_repository_name"
}

module "service" {
  source = "./service"

  # Pass any required variables to the service module
  # (e.g., ecr_repository_name, other module dependencies, etc.)
}


# Create EC2 instances only if image digests are available





