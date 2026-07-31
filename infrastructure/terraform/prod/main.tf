terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.12"
    }
  }

  backend "s3" {
    bucket         = "ecommerce-terraform-state-prod"
    key            = "infrastructure/terraform/prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "ecommerce-terraform-locks-prod"
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "prod"
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
  default     = "vpc-0123456789abcdef0"
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
  default     = ["subnet-01234567", "subnet-89abcdef", "subnet-fedcba98"]
}

locals {
  common_tags = {
    Project     = "ecommerce-platform"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

module "eks" {
  source = "../modules/eks"

  cluster_name    = "ecommerce-eks-${var.environment}"
  cluster_version = "1.31"
  vpc_id          = var.vpc_id
  subnet_ids      = var.subnet_ids

  node_instance_type = "t3.large"
  desired_capacity   = 6
  max_size           = 12
  min_size           = 3

  tags = local.common_tags
}

module "rds" {
  source = "../modules/rds"

  name                   = "ecommerce-rds-${var.environment}"
  environment            = var.environment
  vpc_id                 = var.vpc_id
  subnet_ids             = var.subnet_ids
  instance_class         = "db.t3.large"
  allocated_storage      = 100
  max_allocated_storage  = 500
  database_name          = "ecommerce"
  backup_retention_period = 14
  deletion_protection    = true

  tags = local.common_tags
}

module "elasticache" {
  source = "../modules/elasticache"

  name               = "ecommerce-redis-${var.environment}"
  environment        = var.environment
  vpc_id             = var.vpc_id
  subnet_ids         = var.subnet_ids
  node_type          = "cache.t3.small"
  num_cache_clusters = 3

  tags = local.common_tags
}

module "msk" {
  source = "../modules/msk"

  name                   = "ecommerce-msk-${var.environment}"
  environment            = var.environment
  vpc_id                 = var.vpc_id
  subnet_ids             = var.subnet_ids
  broker_instance_type   = "kafka.m7g.large"
  number_of_broker_nodes = 3

  tags = local.common_tags
}
