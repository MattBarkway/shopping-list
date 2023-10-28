output "public_subnet_ids" {
  value = [aws_subnet.public_subnet.id, aws_subnet.public_subnet2.id]
}

output "private_subnet_id" {
  value = aws_subnet.private_subnet.id
}

output "vpc_id" {
  value = aws_vpc.vpc.id
}
