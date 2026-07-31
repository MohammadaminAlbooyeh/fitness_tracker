# Infrastructure

This directory contains infrastructure-as-code and deployment configuration for the e-commerce platform.

## Directory Structure

```
infrastructure/
├── docker-compose/          # Docker Compose override files
│   ├── docker-compose.yml   # Base infra (Postgres, Redis, Kong)
│   ├── docker-compose.services.yml  # All 14 microservices
│   ├── docker-compose.infra.yml     # Observability (Prometheus, Grafana, Jaeger)
│   └── prometheus.yml       # Prometheus scrape config
├── kubernetes/              # Kubernetes manifests and Helm charts
│   ├── base/                # Base Kustomize manifests
│   ├── helm-charts/         # Reusable Helm chart for microservices
│   └── overlays/            # Dev and prod overlays
├── terraform/               # AWS infrastructure (EKS, RDS, ElastiCache, MSK)
│   ├── modules/             # Reusable Terraform modules
│   ├── dev/                 # Dev environment
│   └── prod/                # Prod environment
└── istio/                   # Istio service mesh configuration
```

## Local Development

```bash
# Start all services
docker-compose -f docker-compose/docker-compose.yml \
               -f docker-compose/docker-compose.services.yml up --build

# Start with observability stack
docker-compose -f docker-compose/docker-compose.yml \
               -f docker-compose/docker-compose.services.yml \
               -f docker-compose/docker-compose.infra.yml up --build

# Stop
docker-compose down
```

## Production Deployment

```bash
# 1. Provision AWS infrastructure
cd infrastructure/terraform/prod
terraform init
terraform apply

# 2. Deploy to EKS
kubectl apply -k infrastructure/kubernetes/overlays/prod

# 3. Apply Istio service mesh
kubectl apply -f infrastructure/istio/
```

## Terraform Modules

| Module | Description |
|--------|-------------|
| `eks` | EKS cluster with managed node groups |
| `rds` | PostgreSQL RDS with encryption and backups |
| `elasticache` | Redis ElastiCache with encryption |
| `msk` | Managed Streaming for Kafka (Apache Kafka) |
