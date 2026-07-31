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
    bucket         = "ecommerce-terraform-state-dev"
    key            = "infrastructure/terraform/dev/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "ecommerce-terraform-locks-dev"
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
  default     = "dev"
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
  default     = "vpc-0123456789abcdef0"
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
  default     = ["subnet-01234567", "subnet-89abcdef"]
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

  node_instance_type = "t3.medium"
  desired_capacity   = 2
  max_size           = 4
  min_size           = 2

  tags = local.common_tags
}

module "rds" {
  source = "../modules/rds"

  name                   = "ecommerce-rds-${var.environment}"
  environment            = var.environment
  vpc_id                 = var.vpc_id
  subnet_ids             = var.subnet_ids
  instance_class         = "db.t3.medium"
  allocated_storage      = 20
  max_allocated_storage  = 100
  database_name          = "ecommerce"
  backup_retention_period = 7
  deletion_protection    = false

  tags = local.common_tags
}

module "elasticache" {
  source = "../modules/elasticache"

  name               = "ecommerce-redis-${var.environment}"
  environment        = var.environment
  vpc_id             = var.vpc_id
  subnet_ids         = var.subnet_ids
  node_type          = "cache.t3.micro"
  num_cache_clusters = 2

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
