output "cluster_id" {
  description = "ElastiCache cluster ID"
  value       = aws_elasticache_replication_group.this.id
}

output "primary_endpoint" {
  description = "Primary endpoint address"
  value       = aws_elasticache_replication_group.this.primary_endpoint_address
}

output "configuration_endpoint" {
  description = "Configuration endpoint address"
  value       = aws_elasticache_replication_group.this.configuration_endpoint_address
}

output "port" {
  description = "Redis port"
  value       = aws_elasticache_replication_group.this.port
}
