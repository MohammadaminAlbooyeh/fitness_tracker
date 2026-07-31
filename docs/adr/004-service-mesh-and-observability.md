# ADR-004: Service Mesh and Observability

## Status
Accepted

## Context
The platform needs:
- Service-to-service traffic management
- Observability (metrics, logs, traces)
- Security (mTLS, authorization policies)

## Decision
- **Service Mesh**: Istio 1.23 for service-to-service communication
- **Metrics**: Prometheus for metric collection
- **Visualization**: Grafana for dashboards
- **Tracing**: Jaeger for distributed tracing
- **Logging**: stdout/stderr to container logs (aggregated by Kubernetes)

## Rationale
- Istio provides advanced traffic management (canaries, blue-green, retries)
- Prometheus + Grafana is the standard CNCF observability stack
- Jaeger provides distributed tracing for debugging microservices
- All tools are available as Docker images for local development

## Consequences
- Istio adds complexity to the Kubernetes deployment
- Sidecar injection required for all services in production
- Local development uses Docker Compose without Istio (simplified)
- Observability stack runs as separate containers in Docker Compose
