# React UI Guide

## Overview

The UI has been upgraded from plain HTML/CSS to a modern React application with fancy animations and glassmorphism effects.

## Features

### Modern Design
- **Glassmorphism Effects**: Beautiful translucent cards with backdrop blur
- **Animated Gradients**: Dynamic background gradients that shift and pulse
- **Smooth Animations**: Framer Motion animations for all interactions
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile

### Components

1. **Header** - Sticky header with animated icon
2. **ConfigInfo** - Displays API configuration with gradient styling
3. **TestCaseUploader** - Drag & drop file upload with image preview
4. **TestCasesList** - Animated list of test cases with hover effects
5. **TestResults** - Charts (Doughnut & Bar) and detailed results table

### Technology Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Framer Motion** - Smooth animations and transitions
- **React Dropzone** - Drag & drop file uploads
- **Chart.js + React-Chartjs-2** - Beautiful charts
- **Lucide React** - Modern icon library

## Development

### Start Development Server

```bash
cd frontend
npm run dev
```

This will start the Vite dev server at `http://localhost:5173` with hot module replacement.

### Build for Production

```bash
cd frontend
npm run build
```

This builds the React app and outputs to `../static/` directory which Flask serves.

## Running the Application

### Option 1: Production Mode (React + Flask)

```bash
# Build React app
cd frontend
npm run build
cd ..

# Start Flask server
python app.py
```

Visit `http://localhost:5000` to see the React UI served by Flask.

### Option 2: Development Mode (React Dev Server + Flask API)

Terminal 1 (Flask API):
```bash
python app.py
```

Terminal 2 (React Dev Server):
```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173` - Vite proxy will forward API calls to Flask.

## UI Features

### Animated Background
- Gradient animation that shifts colors
- Floating radial patterns
- Custom scrollbar with gradient

### Interactive Elements
- Hover effects on all cards
- Scale animations on buttons
- Smooth transitions everywhere
- Loading spinners with gradient

### Drag & Drop Upload
- Click or drag files to upload
- Image preview before submission
- Visual feedback on drag hover
- Support for PNG, JPG, GIF, WEBP

### Charts & Visualizations
- Doughnut chart for pass/fail overview
- Bar chart for similarity scores
- Animated stat cards
- Color-coded results table

### Responsive Design
- Mobile-friendly layout
- Stacked components on small screens
- Touch-friendly buttons
- Optimized chart sizes

## Customization

### Colors
Edit CSS variables in [App.css](frontend/src/App.css):

```css
:root {
  --primary: #667eea;
  --secondary: #764ba2;
  --success: #38ef7d;
  --danger: #f45c43;
  /* ... more colors */
}
```

### Animations
Adjust Framer Motion settings in component files:

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
```

## File Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx & Header.css
│   │   ├── ConfigInfo.jsx & ConfigInfo.css
│   │   ├── TestCaseUploader.jsx & TestCaseUploader.css
│   │   ├── TestCasesList.jsx & TestCasesList.css
│   │   └── TestResults.jsx & TestResults.css
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── package.json
└── vite.config.js
```

## Notes

- The old HTML template is still in `templates/index.html` (not used)
- React build outputs to `static/` which Flask serves
- All API endpoints remain the same
- CORS is enabled for development mode
