# Scalable E-Commerce Platform

A microservices-based e-commerce platform with 14 services implemented in Python (FastAPI) and Java (Spring Boot).

## Architecture

### Python Services (FastAPI + SQLAlchemy)
- user-service - Authentication and user profiles
- product-service - Products and categories
- cart-service - Shopping cart
- order-service - Order management
- notification-service - User notifications
- analytics-service - Sales analytics
- behavior-tracking-service - User behavior tracking
- recommendation-service - Product recommendations

### Java Services (Spring Boot)
- payment-service - Payment processing
- inventory-service - Inventory management
- search-service - Product search
- review-service - Product reviews
- seller-service - Seller management

### Infrastructure
- Kong API Gateway
- PostgreSQL
- Redis

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Java 17 (for local development of Java services)
- Maven (for local development of Java services)
- Poetry (for local development of Python services)

## Quick Start

```bash
# Start all services
docker-compose up --build

# Stop all services
docker-compose down
```

## Service Ports

| Service | Port |
|---------|------|
| Kong Gateway | 8000 |
| PostgreSQL | 5432 |
| Redis | 6379 |
| user-service | 8001 |
| product-service | 8002 |
| cart-service | 8003 |
| order-service | 8004 |
| notification-service | 8005 |
| analytics-service | 8006 |
| behavior-tracking-service | 8007 |
| recommendation-service | 8008 |
| payment-service | 8081 |
| inventory-service | 8082 |
| search-service | 8083 |
| review-service | 8084 |
| seller-service | 8085 |

## Development

### Python Services
```bash
cd services/[service-name]
poetry install
uvicorn app.main:app --reload
```

### Java Services
```bash
cd services/[service-name]
mvn spring-boot:run
```
