# ZonoSign Backend

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-FFD43B.svg?logo=python&logoColor=blue)](https://github.com/astral-sh/uv)

Backend service for ZonoSign, a 3D sign language learning platform that helps users learn and practice sign language through interactive lessons and real-time feedback.

## 🚀 Features

- **User Authentication**: JWT-based authentication system
- **Learning Modules**: Structured curriculum with progressive difficulty
- **Sign Language Dictionary**: Comprehensive database of sign language entries
- **Progress Tracking**: Detailed user progress and performance metrics
- **Interactive Learning**: Support for video lessons and interactive exercises
- **3D Sign Visualization**: Integration with 3D sign language visualization

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (Development), PostgreSQL (Production-ready)
- **Authentication**: JWT (JSON Web Tokens)
- **Package Management**: uv
- **API Documentation**: OpenAPI/Swagger UI
- **Testing**: pytest

## 📦 Prerequisites

- Python 3.10+
- uv (Package Manager)
- SQLite (for development)
- (Optional) PostgreSQL (for production)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/zonosign-backend.git
   cd zonosign-backend/backend
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies using uv**
   ```bash
   uv pip install -e .
   ```

4. **Set up environment variables**
   Copy the example environment file and update the values:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize the database**
   ```bash
   python -c "from database import init_db; init_db()"
   python seed_data.py
   ```

## 🏃‍♂️ Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8024`

## 📚 API Documentation

- **Scalar**: `http://localhost:8024/scalar`
- **Swagger UI**: `http://localhost:8024/docs`
- **ReDoc**: `http://localhost:8024/redoc`
- **OpenAPI JSON**: `http://localhost:8024/openapi.json`

## 🧪 Running Tests

```bash
uv run pytest
```

## 🏗️ Project Structure

```
backend/
├── .env.example           # Example environment variables
├── main.py               # Application entry point
├── pyproject.toml        # Project dependencies and metadata
├── uv.lock               # uv lock file
├── database.py           # Database configuration
├── models.py             # SQLAlchemy models
├── schemas.py            # Pydantic models
├── auth_utils.py         # Authentication utilities
├── settings.py           # Application settings
├── seed_data.py          # Sample data generation
└── routers/              # API route handlers
    ├── __init__.py
    ├── auth.py           # Authentication routes
    ├── curriculum.py     # Learning modules and lessons
    ├── dictionary.py     # Sign language dictionary
    ├── progress.py       # User progress tracking
    └── users.py          # User management
```

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Application
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./zonosign.db
# For production:
# DATABASE_URL=postgresql://user:password@localhost/zonosign
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- FastAPI and Sebastian for the amazing web framework
- SQLAlchemy for the ORM
- All contributors who have helped with development

---

<div align="center">
  Made with ❤️ by the ZonoSign Team
</div>
