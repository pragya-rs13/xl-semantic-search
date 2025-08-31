# Semantic Search Frontend

A modern, responsive web interface for semantic search functionality built with vanilla HTML, CSS, and JavaScript.

## Features

- Clean, modern UI with floating background orbs
- File attachment support for search queries
- Real-time search results display
- Responsive design for all devices

## Quick Start with Docker

### Prerequisites
- Docker installed on your system

### Running the Frontend

1. **Build the Docker image:**
   ```bash
   docker build -t semantic-search-frontend .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8081:80 semantic-search-frontend
   ```

3. **Access the application:**
   Open your browser and navigate to `http://localhost:8081`

### Docker Commands

- **Stop the container:**
  ```bash
  docker stop $(docker ps -q --filter ancestor=semantic-search-frontend)
  ```

- **View running containers:**
  ```bash
  docker ps
  ```

- **Remove the image:**
  ```bash
  docker rmi semantic-search-frontend
  ```

## Development Setup

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Local Development

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

## Project Structure

frontend/
├── index.html # Main HTML file
├── styles.css # Custom CSS styles
├── script.js # JavaScript functionality
├── package.json # Dependencies and scripts
├── vite.config.js # Vite configuration
└── README.md # This file

## Technologies Used

- **HTML5** - Semantic markup
- **CSS3** - Custom styling with animations
- **Vanilla JavaScript** - ES6+ features
- **Vite** - Build tool and dev server

## API Integration

The frontend connects to the backend API at `http://localhost:8001/api/v1/search` for search functionality.

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)