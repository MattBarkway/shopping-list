variable "ecr_image_name" {
  description = "Name of the ECR image to use for EC2 instances"
  type        = string
  default     = "my-container-image"
}

variable "ecr_image_tag" {
  description = "Tag of the ECR image to use for EC2 instances"
  type        = string
  default     = "latest"
}