# Architecture

## Overview

A microservices-based e-commerce platform with 14 services implemented in Python (FastAPI) and Java (Spring Boot), orchestrated via Docker Compose for local development and Kubernetes (EKS) for production.

## Architecture Diagram

```
                    ┌─────────────────────────────────────────┐
                    │              Kong API Gateway            │
                    │           (Port 8000/8443)               │
                    └──────────┬──────────────────┬──────────┘
                               │                  │
        ┌──────────────────────┴──┐    ┌──────────┴──────────────┐
        │     Python Services      │    │      Java Services      │
        │     (FastAPI 8001-8008)  │    │     (Spring Boot 8081-8085)│
        └──────────────────────────┘    └──────────────────────────┘
               │         │         │         │         │
        ┌──────┴──────┐  │  ┌──────┴──────┐  │  ┌──────┴──────┐
        │ user-svc    │  │  │ product-svc │  │  │ payment-svc │
        │ cart-svc    │  │  │ order-svc   │  │  │ inventory   │
        │ notif-svc   │  │  │ analytics   │  │  │ search-svc  │
        │ behavior    │  │  │ recommend   │  │  │ review-svc  │
        │             │  │  │             │  │  │ seller-svc  │
        └──────┬──────┘  │  └──────┬──────┘  │  └──────┬──────┘
               │         │         │         │         │
               └─────────┴─────────┴─────────┴─────────┘
                         │
               ┌─────────┴─────────┐
               │  Shared Services   │
               │  PostgreSQL (5432) │
               │  Redis (6379)      │
               │  Kafka (MSK)       │
               └────────────────────┘
```

## Service Catalog

### Python Services (FastAPI + SQLAlchemy + AsyncPG)

| Service | Port | Description |
|---------|------|-------------|
| user-service | 8001 | Authentication, JWT tokens, user profiles |
| product-service | 8002 | Products, categories, inventory references |
| cart-service | 8003 | Shopping cart with items, Redis-backed sessions |
| order-service | 8004 | Order management, order items, status tracking |
| notification-service | 8005 | User notifications (email, SMS, push) |
| analytics-service | 8006 | Sales analytics and reporting |
| behavior-tracking-service | 8007 | User behavior event tracking |
| recommendation-service | 8008 | Product recommendations based on behavior |

### Java Services (Spring Boot + JPA + Hibernate)

| Service | Port | Description |
|---------|------|-------------|
| payment-service | 8081 | Payment processing, transaction management |
| inventory-service | 8082 | Inventory stock levels, reservation system |
| search-service | 8083 | Search query logging and analytics |
| review-service | 8084 | Product reviews and ratings |
| seller-service | 8085 | Seller management, store profiles |

### Infrastructure Components

| Component | Port | Description |
|-----------|------|-------------|
| Kong API Gateway | 8000/8443 | API routing, authentication, rate limiting |
| PostgreSQL | 5432 | Primary database for all services |
| Redis | 6379 | Caching and session storage |
| Kafka (MSK) | 9092 | Event streaming between services |
| Istio | - | Service mesh for traffic management |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Monitoring dashboards |
| Jaeger | 16686 | Distributed tracing |

## Design Decisions

### Language Split
- **Python (FastAPI)**: User-facing CRUD services, analytics, behavior tracking, recommendations — services that benefit from rapid development and data science integration
- **Java (Spring Boot)**: Payment, inventory, search, review, seller — services requiring strong transaction guarantees, type safety, and JVM ecosystem integrations

### Shared Libraries
- `shared/python-common-lib/`: Base SQLAlchemy models, Pydantic schemas, security (JWT, password hashing), database session management, configuration
- `shared/java-common-lib/`: BaseEntity with audit fields, SecurityConfig, common application.yml

### Database Strategy
- Single PostgreSQL instance for development (docker-compose)
- AWS RDS PostgreSQL for production with multi-AZ, encryption, automated backups
- Each service owns its tables; no cross-service table access

### Communication Patterns
- Synchronous: REST APIs through Kong API Gateway
- Asynchronous: Kafka (MSK) for event-driven communication (order → payment, order → inventory, behavior → recommendation)

### Deployment Strategy
- **Development**: Docker Compose with all services
- **Production**: Kubernetes (EKS) with Helm charts, Istio service mesh, Terraform IaC

## Key Patterns

1. **DTO Pattern**: All services use separate request/response DTOs to decouple API contracts from database models
2. **Service Layer**: Business logic encapsulated in service classes, controllers are thin
3. **Dependency Injection**: Spring DI for Java services, FastAPI dependencies for Python
4. **Health Checks**: All services expose `/health` or `/actuator/health` endpoints
5. **Configuration**: Environment variables via configmaps/secrets in Kubernetes
