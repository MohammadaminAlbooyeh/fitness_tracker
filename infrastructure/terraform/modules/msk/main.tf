resource "aws_security_group" "msk" {
  name        = "${var.name}-msk-sg"
  description = "Security group for MSK ${var.name}"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 9092
    to_port         = 9092
    protocol        = "tcp"
    cidr_blocks     = ["10.0.0.0/8"]
  }

  ingress {
    from_port       = 9094
    to_port         = 9094
    protocol        = "tcp"
    cidr_blocks     = ["10.0.0.0/8"]
  }

  ingress {
    from_port       = 2181
    to_port         = 2181
    protocol        = "tcp"
    cidr_blocks     = ["10.0.0.0/8"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name = "${var.name}-msk-sg"
  })
}

resource "aws_msk_configuration" "this" {
  kafka_versions = [var.kafka_version]
  name           = "${var.name}-config"

  config_file_contents = base64encode(<<-EOF
    auto.create.topics.enable = true
    delete.topic.enable = true
    log.retention.hours = 168
    log.segment.bytes = 1073741824
    num.partitions = 3
    num.replica.fetchers = 2
    num.replica.replication.lag.time.max.ms = 30000
    replica.lag.time.max.ms = 30000
    EOF
  )
}

resource "aws_msk_cluster" "this" {
  cluster_name           = var.name
  kafka_version          = var.kafka_version
  enhanced_monitoring    = var.enhanced_monitoring
  kafka_configuration {
    config_file_contents = aws_msk_configuration.this.config_file_contents
    name                 = aws_msk_configuration.this.name
  }

  number_of_broker_nodes = var.number_of_broker_nodes

  broker_node_group_info {
    instance_type   = var.broker_instance_type
    client_subnets  = var.subnet_ids
    security_groups = [aws_security_group.msk.id]
  }

  encryption_info {
    encryption_at_rest_kms_key_arn = aws_kms_key.msk.arn
  }

  logging_info {
    broker_logs {
      cloudwatch_logs {
        enabled   = true
        log_group = "/aws/msk/${var.name}"
      }
      firehose {
        enabled = false
      }
      s3 {
        enabled = false
      }
    }
  }

  tags = var.tags
}

resource "aws_kms_key" "msk" {
  description             = "KMS key for MSK ${var.name}"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  tags = var.tags
}

resource "aws_cloudwatch_log_group" "msk" {
  name              = "/aws/msk/${var.name}"
  retention_in_days = 30

  tags = var.tags
}
