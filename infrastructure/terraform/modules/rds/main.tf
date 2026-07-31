resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-subnet-group"
  subnet_ids = var.subnet_ids

  tags = merge(var.tags, {
    Name = "${var.name}-subnet-group"
  })
}

resource "aws_db_parameter_group" "this" {
  family = "postgres-16"
  name   = "${var.name}-parameter-group"

  parameter {
    name  = "shared_preload_libraries"
    value = "pg_stat_statements"
  }

  tags = var.tags
}

resource "aws_secretsmanager_secret" "db_credentials" {
  name        = "${var.name}-credentials"
  description = "RDS credentials for ${var.name}"

  tags = var.tags
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id

  secret_string = jsonencode({
    username = var.username
    password = random_password.db_password.result
  })
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

resource "aws_db_instance" "this" {
  identifier               = var.name
  engine                   = "postgres"
  engine_version           = "16"
  engine_family          = "postgres-16"
  engine_parameter_group = aws_db_parameter_group.this.name

  instance_class          = var.instance_class
  allocated_storage       = var.allocated_storage
  max_allocated_storage   = var.max_allocated_storage
  username                = var.username
  password                = random_password.db_password.result
  db_name                 = var.database_name

  db_subnet_group_name    = aws_db_subnet_group.this.name
  vpc_security_group_ids  = [aws_security_group.rds.id]

  backup_retention_period = var.backup_retention_period
  backup_window           = "03:00-04:00"
  maintenance_window      = "sun:05:00-sun:06:00"

  deletion_protection     = var.deletion_protection
  skip_final_snapshot     = !var.deletion_protection
  publicly_accessible     = false
  apply_immediately       = false
  storage_encrypted       = true

  tags = var.tags
}

resource "aws_security_group" "rds" {
  name        = "${var.name}-rds-sg"
  description = "Security group for RDS ${var.name}"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = []
    cidr_blocks     = []
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.name}-rds-sg"
  })
}
