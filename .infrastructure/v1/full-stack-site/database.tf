#resource "aws_security_group" "db_sg" {
#  name        = "${var.name}-rds-db-security-group"
#  description = "Security group for the RDS database"
#
#  vpc_id = var.vpc_id
#
#  ingress {
#    from_port   = 5432
#    to_port     = 5432
#    protocol    = "tcp"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#
#  egress {
#    from_port   = 0
#    to_port     = 0
#    protocol    = "-1"
#    cidr_blocks = ["0.0.0.0/0"]
#  }
#}
#
#resource "aws_db_parameter_group" "db_params" {
#  name        = "${var.name}-db-params"
#  family      = var.db_family
#  description = "Parameter group for ${var.name} DB"
#
#  parameter {
#    name  = "max_connections"
#    value = "20"
#    apply_method = "pending-reboot"
#  }
#}
#
#resource "aws_db_subnet_group" "db_subnet_group" {
#    name       = "${var.name}-db_subnet_group"
#    subnet_ids = var.subnet_ids
#
#    tags = {
#        Name = "${var.name} DB subnet group"
#    }
#}
#
#resource "aws_db_instance" "db_instance" {
#  identifier                = "${var.name}-db"
#  allocated_storage         = var.db_allocated_storage
#  storage_type              = var.db_storage_type
#  engine                    = var.db_engine
#  engine_version            = var.db_engine_version
#  instance_class            = var.db_instance_class
#  username                  = var.db_username
#  password                  = var.db_password
#  parameter_group_name      = aws_db_parameter_group.db_params.name
#  db_subnet_group_name      = aws_db_subnet_group.db_subnet_group.name
#  vpc_security_group_ids    = [aws_security_group.db_sg.id]
#  publicly_accessible       = false
#  backup_retention_period   = 7
#  multi_az                  = false
#  skip_final_snapshot       = true
#
#  tags = {
#    Name = "${var.name}-db"
#  }
#}
