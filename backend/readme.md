# Semantic Search Backend

A FastAPI-based backend service for semantic search functionality, built with Python and designed to handle Excel file processing and AI-powered search queries.

## Features

- FastAPI REST API with automatic OpenAPI documentation
- File upload and processing support
- Integration with Google Gemini AI for semantic search
- Excel file parsing and analysis
- Structured response formatting

## Quick Start with Docker

### Prerequisites
- Docker installed on your system

### Running the Backend

1. **Build the Docker image:**
   ```bash
   docker build -t semantic-search-backend .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8001:8000 semantic-search-backend
   ```

3. **Access the API:**
   - API Base URL: `http://localhost:8001`
   - API Documentation: `http://localhost:8001/docs`
   - Health Check: `http://localhost:8001/api/v1/health`

### Docker Commands

- **Stop the container:**
  ```bash
  docker stop $(docker ps -q --filter ancestor=semantic-search-backend)
  ```

- **View running containers:**
  ```bash
  docker ps
  ```

- **Remove the image:**
  ```bash
  docker rmi semantic-search-backend
  ```

## Development Setup

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Local Development

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env-example .env
   # Edit .env file with your API keys
   ```

4. **Run the development server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application:**
   - API: `http://localhost:8000`
   - Documentation: `http://localhost:8000/docs`

## Environment Variables

Create a `.env` file in the backend directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

## Project Structure
```
backend/
├── main.py # FastAPI application entry point
├── requirements.txt # Python dependencies
├── logger.py # Logging configuration
├── .env-example # Environment variables template
├── Dockerfile # Docker configuration
├── routes/ # API route definitions
│ ├── healthcheck.py # Health check endpoint
│ └── search.py # Search API endpoints
├── usecases/ # Business logic
│ ├── search.py # Search functionality
│ ├── uploads.py # File upload handling
│ └── rank_response.py # Response ranking
├── schemas/ # Pydantic data models
│ └── llm_schema.py # LLM response schemas
├── clients/ # External service clients
│ └── gemini_client.py # Google Gemini client
└── utils/ # Utility functions
├── chunk_util.py # Text chunking utilities
├── load_csv.py # CSV file loading
├── load_workbook.py # Excel file loading
└── validate_schema.py # Schema validation
```

## API Endpoints

### Health Check
- **GET** `/api/v1/health` - Service health status

### Search
- **POST** `/api/v1/search` - Perform semantic search with file upload

## Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.11** - Programming language
- **Uvicorn** - ASGI server for running FastAPI
- **Google Gemini AI** - AI-powered semantic search
- **Pydantic** - Data validation and settings management
- **Pandas** - Data manipulation and analysis
- **OpenPyXL** - Excel file processing

## Dependencies

Key dependencies include:
- `fastapi==0.116.1` - Web framework
- `uvicorn==0.35.0` - ASGI server
- `google-generativeai==0.8.3` - Google Gemini AI
- `pandas==2.3.2` - Data analysis
- `openpyxl==3.1.5` - Excel file handling

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests (if implemented)
pytest

# Format code (if black is added)
black .

# Lint code (if flake8 is added)
flake8 .
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide interactive API documentation and testing capabilities.