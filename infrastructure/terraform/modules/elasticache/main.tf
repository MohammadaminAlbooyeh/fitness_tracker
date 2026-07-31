resource "aws_elasticache_subnet_group" "this" {
  name       = "${var.name}-subnet-group"
  subnet_ids = var.subnet_ids

  tags = var.tags
}

resource "aws_elasticache_security_group" "this" {
  name        = "${var.name}-cache-sg"
  description = "Security group for ElastiCache ${var.name}"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.name}-cache-sg"
  })
}

resource "aws_elasticache_replication_group" "this" {
  replication_group_id          = var.name
  replication_group_description = "Redis replication group for ${var.name}"
  engine                        = "redis"
  engine_version                = var.engine_version
  parameter_group_name          = var.parameter_group_name
  node_type                     = var.node_type
  number_cache_clusters         = var.num_cache_clusters
  port                          = 6379

  subnet_group_name    = aws_elasticache_subnet_group.this.name
  security_group_ids   = [aws_elasticache_security_group.this.id]

  automatic_failover_enabled = true
  multi_az_enabled           = true
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = random_password.redis_auth.result

  snapshot_retention_limit = 5
  snapshot_window          = "05:00-06:00"
  maintenance_window       = "sun:06:00-sun:07:00"

  tags = var.tags
}

resource "random_password" "redis_auth" {
  length  = 32
  special = true
}

resource "aws_secretsmanager_secret" "redis_auth" {
  name        = "${var.name}-redis-auth-token"
  description = "Redis auth token for ${var.name}"

  tags = var.tags
}

resource "aws_secretsmanager_secret_version" "redis_auth" {
  secret_id = aws_secretsmanager_secret.redis_auth.id

  secret_string = random_password.redis_auth.result
}
