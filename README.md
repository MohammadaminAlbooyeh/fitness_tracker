# Fitness Tracker

A full-stack fitness tracking application built with React (frontend) and FastAPI (backend).

## Features

- User authentication and profiles
- Workout planning and tracking
- Exercise library with equipment and muscle groups
- Progress tracking with photos and measurements
- Social features (posts, challenges)
- Gamification (achievements, streaks)
- Smart features and health recovery

## Project Structure

- `client/`: React frontend with Vite
- `server/`: FastAPI backend with SQLAlchemy

## Setup

### Prerequisites

- Node.js (for client)
- Python 3.9+ (for server)
- PostgreSQL

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MohammadaminAlbooyeh/fitness_tracker.git
   cd fitness_tracker
   ```

2. **Set up the database**
   - Install PostgreSQL
   - Create a database named `fitness_db`
   - Update `server/.env` with your database URL

3. **Install server dependencies**
   ```bash
   cd server
   poetry install
   ```

4. **Install client dependencies**
   ```bash
   cd ../client
   npm install
   ```

### Running the Application

1. **Start the server**
   ```bash
   cd server
   poetry run uvicorn app.main:app --reload
   ```
   Server will run on http://localhost:8000

2. **Start the client**
   ```bash
   cd client
   npm run dev
   ```
   Client will run on http://localhost:5173

## API Documentation

Once the server is running, visit http://localhost:8000/docs for the FastAPI interactive documentation.

## Testing

### Client Tests
```bash
cd client
npm test
```

### Server Tests
```bash
cd server
poetry run pytest
```

## Deployment

### Using Docker
```bash
docker-compose up -d
```

See `docs/deployment.md` for detailed deployment instructions.

## CI/CD

The project includes GitHub Actions for continuous integration. Tests run on every push and PR to the main branch.