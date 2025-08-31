# Semantic Search System

A comprehensive semantic search solution that processes Excel files and provides AI-powered search capabilities for business formulas and concepts.

## Documentation

- **[Frontend Documentation](frontend/README.md)** - Frontend setup, Docker deployment, and development guide
- **[Backend Documentation](backend/README.md)** - Backend API, FastAPI setup, and deployment instructions  
- **[Technical Design Document](design-docs/technical-design.md)** - Comprehensive technical architecture and implementation details

## Quick Start

### Frontend
```bash
cd frontend

```
1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```
Access at: http://localhost:8080

### Backend
```bash
cd backend
docker build -t semantic-search-backend .
docker run -p 8001:8000 semantic-search-backend
```
API at: http://localhost:8001

## Architecture Overview

The system consists of:
- **Frontend**: Vanilla HTML/CSS/JS with modern UI
- **Backend**: FastAPI Python service with Google Gemini AI integration
- **AI Pipeline (In Backend)**: Multi-step LLM processing for semantic understanding

## Project Structure
```
xl-semantic-search/
├── frontend/ # Frontend application
├── backend/ # Backend API service
├── design-docs/ # Technical documentation
└── README.md # This file
```

## 🔗 Links

- **Live Demo**: [Frontend](http://localhost:8080) | [API Docs](http://localhost:8001/docs)
- **Source Code**: [Frontend](frontend/) | [Backend](backend/)
- **Technical Details**: [Design Document](design-docs/technical-design.md)