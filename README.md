# SnapPost

A FastAPI-based social media backend with PostgreSQL, Alembic migrations, and Docker support.

## Features
- User registration and login
- Create, view, and manage posts
- Async database operations with SQLModel
- Alembic migrations for schema management
- Docker and Docker Compose for easy deployment
 - Media upload/download backed by MinIO (S3-compatible)

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
Create a `.env` file in the project root:
```
DATABASE_URL="postgresql+asyncpg://username:password@localhost:5432/dbname"
POSTGRES_HOST=host
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=bd_name
SECRET_KEY="your_jwt_secretkey"
ACCESS_TOKEN_EXPIRE_MINUTES=token_expire_time(int)
ALGORITHM=hash_algoritm
 
# MinIO / S3
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Upload limits and allowed types
MAX_FILE_SIZE=10485760
ALLOWED_IMAGE_TYPES='["image/gif","image/png","image/jpeg"]'
ALLOWED_VIDEO_TYPES='["video/mp4","video/x-msvideo","video/quicktime","video/x-matroska"]'
```

## API Overview

### Auth
- `POST /user/register`
- `POST /user/login`

### Posts
- `POST /post/create` form fields: `Title`, `Text`, `media` (file)
- `GET /post/view` query: `owner_username`, `target_post_title`
- `GET /post/download/{filename}`

When running locally with Docker, MinIO is expected at `http://localhost:9000`.

## License
MIT
