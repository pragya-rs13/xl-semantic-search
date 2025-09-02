# Semantic Search Frontend

A modern, responsive web interface for semantic search functionality built with vanilla HTML, CSS, and JavaScript.

## Features

- Clean, modern UI with floating background orbs
- File attachment support for search queries
- Real-time search results display
- Responsive design for all devices

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
```
frontend/
├── index.html # Main HTML file
├── styles.css # Custom CSS styles
├── script.js # JavaScript functionality
├── package.json # Dependencies and scripts
├── vite.config.js # Vite configuration
└── README.md # This file
```

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