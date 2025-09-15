# SnapPost

A FastAPI-based social media backend with PostgreSQL, Alembic migrations, and Docker support.

## Features
- User registration and login
- Create, view, and manage posts
- Async database operations with SQLModel
- Alembic migrations for schema management
- Docker and Docker Compose for easy deployment

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.13 (for local development)

### Run with Docker
```bash
docker compose up -d --build
```

### Local Development
1. Clone the repo:
   ```bash
   git clone https://github.com/Ali-Soleimanian/Snappost
   cd snappost
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the server:
   ```bash
   uvicorn app.main:app --reload  # Or python run.py
   ```


## Environment Variables
Set your database connection in `.env`:
```
DATABASE_URL = "postgresql+asyncpg://username:password@localhost:5432/dbname"
```

## License
MIT
