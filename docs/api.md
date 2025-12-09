# API Documentation

This document outlines the API endpoints for the Fitness Tracker application.

## Base URL
```
http://localhost:8000/api
```

## Authentication
Most endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

### Authentication Endpoints

#### POST /register
Register a new user.
- **Body**: `{"email": "string", "username": "string", "password": "string"}`
- **Response**: User object

#### POST /token
Login and get access token.
- **Body**: `{"username": "string", "password": "string"}` (OAuth2 form)
- **Response**: `{"access_token": "string", "token_type": "bearer"}`

## Workout Endpoints

#### GET /workouts
Get all workouts.
- **Response**: Array of workout objects

#### POST /workouts
Create a new workout.
- **Body**: Workout creation data
- **Response**: Created workout object

#### GET /workouts/templates
Get workout templates.
- **Query Params**: `category`, `difficulty`, `include_public`
- **Response**: Array of templates

#### POST /workouts/templates
Create a workout template.
- **Body**: Template data
- **Response**: Created template

## Exercise Endpoints

#### GET /exercises
Get exercises with filtering.
- **Query Params**: `category`, `difficulty`, `equipment`, `muscle`, `query`
- **Response**: Array of exercises

#### GET /equipment
Get available equipment.
- **Response**: Array of equipment

#### GET /muscles
Get muscle groups.
- **Response**: Array of muscles

## Progress Tracking

#### GET /progress/photos
Get progress photos.
- **Response**: Array of photos

#### POST /progress/photos
Upload a progress photo.
- **Body**: Multipart form data with image file

## Gamification

#### GET /achievements
Get user achievements.
- **Response**: Array of achievements

#### GET /streak
Get current streak.
- **Response**: Streak data

## Social Features

#### GET /social/posts
Get social posts.
- **Response**: Array of posts

#### POST /social/posts
Create a new post.
- **Body**: Post data

## Smart Features

#### GET /smart/recommendations
Get workout recommendations.
- **Response**: Recommendations

## Health and Recovery

#### GET /health/recovery
Get recovery suggestions.
- **Response**: Recovery data

For detailed schemas and interactive documentation, visit `http://localhost:8000/docs` when the server is running.

## Testing with Postman

Import the following collection into Postman for testing API endpoints:

```json
{
  "info": {
    "name": "Fitness Tracker API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Register",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"email\": \"test@example.com\", \"username\": \"testuser\", \"password\": \"testpass\"}"
        },
        "url": {
          "raw": "{{base_url}}/register",
          "host": ["{{base_url}}"],
          "path": ["register"]
        }
      }
    },
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "header": [],
        "body": {
          "mode": "urlencoded",
          "urlencoded": [
            {
              "key": "username",
              "value": "test@example.com"
            },
            {
              "key": "password",
              "value": "testpass"
            }
          ]
        },
        "url": {
          "raw": "{{base_url}}/token",
          "host": ["{{base_url}}"],
          "path": ["token"]
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000/api"
    }
  ]
}
```

Set the `base_url` variable to your API URL.