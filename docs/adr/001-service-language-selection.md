# ADR-001: Service Language Selection (Python vs Java)

## Status
Accepted

## Context
The e-commerce platform consists of 14 microservices. We need to decide which services should be implemented in Python (FastAPI) and which in Java (Spring Boot), considering factors such as:
- Development speed
- Type safety requirements
- Transaction guarantees
- Team expertise
- Ecosystem integrations
- Performance characteristics

## Decision
We split services as follows:

**Python (FastAPI)** — 8 services:
- user-service: Authentication and user profiles (rapid development, JWT)
- product-service: Product catalog (data-centric, frequent schema changes)
- cart-service: Shopping cart (Redis integration, async operations)
- order-service: Order management (relatively simple business logic)
- notification-service: Notifications (async I/O for email/SMS)
- analytics-service: Sales analytics (data science friendly)
- behavior-tracking-service: User behavior tracking (high write throughput)
- recommendation-service: Recommendations (ML/data processing)

**Java (Spring Boot)** — 5 services:
- payment-service: Payment processing (strong transaction guarantees, financial data)
- inventory-service: Inventory management (critical stock accuracy, reservation logic)
- search-service: Search query logging (type safety for query models)
- review-service: Product reviews (moderation, rating calculations)
- seller-service: Seller management (store profiles, business relationships)

## Rationale
- Python services benefit from FastAPI's rapid development cycle and are well-suited for CRUD-heavy, data-science-adjacent use cases
- Java services handle financial/transactional data where type safety and ACID guarantees are critical
- Spring Boot provides robust ecosystem integrations (payment gateways, messaging) that are well-established in Java
- All services share common infrastructure (PostgreSQL, Redis, Kafka) via shared libraries

## Consequences
- Two technology stacks to maintain
- Cross-service communication via REST APIs (language agnostic)
- Shared libraries in both Python and Java to enforce consistency
- CI/CD pipeline must handle both Python (Poetry) and Java (Maven) builds
