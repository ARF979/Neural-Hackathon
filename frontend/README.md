# AI Social Media Content Generator - Frontend

## 🚀 Beautiful React Frontend with TailwindCSS

### Features

- ✨ Modern, glassmorphism design
- 🎨 Beautiful gradients and animations
- 📱 Fully responsive layout
- 🚀 Real-time content generation
- 📋 Copy and download functionality
- ⚡ Loading states and error handling
- 🎯 Professional UI/UX

### Quick Start

1. **Install dependencies**
```bash
npm install
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Update API_URL if needed
```

3. **Start the development server**
```bash
npm start
```

The app will open at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

### Tech Stack

- **React** - UI framework
- **TailwindCSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icon library

### Project Structure

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── App.js          # Main component
│   ├── index.js        # Entry point
│   └── index.css       # Global styles + Tailwind
├── package.json
├── tailwind.config.js
└── .env
```

### Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:8000)

### Development

The frontend is configured to proxy requests to the backend API. Make sure the backend is running on port 8000.

### Deployment

Deploy to:
- **Vercel** (recommended)
- **Netlify**
- **GitHub Pages**
- **AWS S3 + CloudFront**

Example Vercel deployment:
```bash
npm install -g vercel
vercel
```
