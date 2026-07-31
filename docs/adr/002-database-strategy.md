# ADR-002: Database Strategy

## Status
Accepted

## Context
The platform has 14 microservices, each with its own data model. We need to decide on the database architecture:
- Single shared database vs. database-per-service
- SQL vs. NoSQL
- Replication and sharding strategy

## Decision
- **Database**: PostgreSQL 16 as the primary database for all services
- **Development**: Single PostgreSQL instance via Docker Compose
- **Production**: AWS RDS PostgreSQL with multi-AZ deployment, encryption at rest, automated backups
- **Strategy**: Database-per-service with shared PostgreSQL instance (schema separation by table naming)

## Rationale
- PostgreSQL provides strong ACID guarantees needed for financial and inventory operations
- All services use similar data patterns (relational with foreign keys)
- RDS provides managed operations, backups, and scaling
- Single instance reduces operational complexity while table-level separation provides service isolation

## Consequences
- All services share the same PostgreSQL connection pool
- Cross-service queries require API calls, not direct DB access
- Migration to database-per-service is possible in the future by splitting the RDS instance
- Redis is used for caching and session storage (shared across services)
- Kafka (MSK) is used for event-driven communication between services
