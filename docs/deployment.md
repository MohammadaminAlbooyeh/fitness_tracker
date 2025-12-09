# Deployment Guide

This guide covers deploying the Fitness Tracker application to production.

## Prerequisites

- Docker and Docker Compose
- PostgreSQL database (or cloud equivalent like AWS RDS)
- Domain name (optional)

## Local Development

1. Follow the setup instructions in the main README.md
2. Run the application locally for testing

## Production Deployment

### Using Docker Compose

1. **Create docker-compose.yml** in the root directory:
```yaml
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: fitness_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  server:
    build: ./server
    environment:
      - DATABASE_URL=postgresql://postgres:your_password@db:5432/fitness_db
      - SECRET_KEY=your_secret_key
    ports:
      - "8000:8000"
    depends_on:
      - db

  client:
    build: ./client
    ports:
      - "80:80"

volumes:
  postgres_data:
```

2. **Create Dockerfile for server**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. **Create Dockerfile for client**:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .
RUN npm run build

EXPOSE 80

CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "80"]
```

4. **Deploy**:
```bash
docker-compose up -d
```

### Cloud Deployment Options

#### AWS
- **Frontend**: Host on S3 + CloudFront
- **Backend**: Deploy to ECS or Lambda
- **Database**: Use RDS PostgreSQL

#### Heroku
- **Frontend**: Static hosting
- **Backend**: Heroku app with PostgreSQL addon

#### Vercel + Railway
- **Frontend**: Vercel
- **Backend**: Railway (PostgreSQL included)

## Environment Variables

Set these in production:
- `DATABASE_URL`: Production database URL
- `SECRET_KEY`: Strong random key
- `ALGORITHM`: HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 30

## Security Considerations

- Use HTTPS in production
- Store secrets securely (not in code)
- Implement rate limiting
- Regular security updates

## Monitoring

- Set up logging
- Monitor performance with tools like New Relic or DataDog
- Use health check endpoints

## Scaling

- Use load balancers for multiple instances
- Implement caching (Redis)
- Database read replicas for heavy loads