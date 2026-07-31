# ADR-003: API Gateway Selection

## Status
Accepted

## Context
We need an API gateway to handle:
- Request routing to microservices
- Authentication and authorization
- Rate limiting
- SSL termination
- Load balancing

## Decision
Use **Kong API Gateway** (version 3.5) in DB-less mode with declarative configuration.

## Rationale
- Kong is lightweight and fast (built on OpenResty/Nginx)
- DB-less mode simplifies deployment and configuration
- Declarative YAML config is version-controllable and CI/CD friendly
- Supports plugins for rate limiting, CORS, JWT, and request transformations
- Integrates well with Kubernetes and Istio

## Consequences
- All API routes are defined in `kong.yml` at the project root
- Kong runs as a sidecar or standalone service in Docker Compose
- In production, Kong runs as a Kubernetes deployment behind a load balancer
- Istio handles service mesh concerns (mTLS, retries, circuit breaking) at the pod level
- Kong handles external API gateway concerns at the edge
