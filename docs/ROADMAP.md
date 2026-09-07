# ROADMAP

## Milestone 0 — Foundation (Completed)

- [x] Project scaffolding: 14 microservices (8 Python, 5 Java, 1 API Gateway)
- [x] Shared libraries: `python-common-lib`, `java-common-lib`
- [x] CI/CD pipeline with lint, test, and Docker build stages
- [x] Docker Compose for local development
- [x] Event catalog documentation (`docs/event-catalog.md`)

## Milestone 1 — Core Services & Event-Driven Flights (Completed)

- [x] User, Product, Cart, Order, Payment, Inventory, Review, Search, Seller services
- [x] Notification, Analytics, Behavior-tracking, Recommendation services
- [x] Kafka event producers for Payment, Inventory, Order, Review services
- [x] Kafka event consumers for Order and Notification services
- [x] Retry with exponential backoff for Kafka consumers
- [x] Integration tests for Kafka publish/consume paths (embedded broker / testcontainers)

## Milestone 2 — Testing & Quality (In Progress)

- [x] Unit tests for all services
- [x] API integration tests for all services
- [x] Kafka integration tests with embedded broker
- [ ] E2E tests covering full user journeys
- [ ] Performance / load testing baseline
- [ ] Security scanning in CI (SAST / dependency check)
- [ ] 80%+ test coverage target enforced in CI

## Milestone 3 — Observability & Reliability (Planned)

- [ ] Distributed tracing (OpenTelemetry / Jaeger)
- [ ] Centralized logging (ELK / Loki)
- [ ] Metrics & dashboards (Prometheus + Grafana)
- [ ] Health checks and readiness probes for all services
- [ ] Circuit breakers and rate limiting (Resilience4j / aioredis)
- [ ] Canary deployments and feature flags

## Milestone 4 — Infrastructure & Deployment (Planned)

- [ ] Terraform modules validated in AWS dev account
- [ ] EKS cluster with auto-scaling
- [ ] RDS PostgreSQL with read replicas
- [ ] ElastiCache Redis cluster
- [ ] MSK Kafka cluster
- [ ] Istio service mesh with mTLS
- [ ] Sealed Secrets / AWS Secrets Manager for K8s secrets
- [ ] Helm charts for all services
- [ ] ArgoCD GitOps deployment pipeline

## Milestone 5 — Advanced Features (Backlog)

- [ ] GraphQL API gateway
- [ ] CQRS and event sourcing for critical domains
- [ ] ML-based recommendation engine
- [ ] Real-time analytics pipeline (Flink / Spark Streaming)
- [ ] Mobile API optimization
- [ ] Multi-tenancy support
