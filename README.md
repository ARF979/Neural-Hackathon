# 🚀 AI Social Media Content Generator

**Professional full-stack application for generating AI-powered social media content with multi-agent workflow and compliance checking.**

Built for the Neural Hackathon | November 2025

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Deployment](#deployment)
- [Team](#team)

---

## ✨ Features

### 🤖 AI-Powered Content Generation
- **Multi-Agent Workflow** using LangGraph
- **Specialized AI Models**:
  - Zephyr-7B for content writing
  - Phi-2 for reviewing and coordination
- **Iterative Refinement** with up to 3 revision cycles
- **Compliance Checking** for brand safety

### 🎨 Beautiful Frontend
- Modern glassmorphism design
- Responsive layout (mobile-first)
- Real-time loading states
- Copy & download functionality
- Professional animations

### 🔧 Robust Backend
- FastAPI with automatic documentation
- Proper error handling
- CORS configuration
- Health check endpoints
- Structured logging

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │
│   (React)       │
└────────┬────────┘
         │ HTTP
         │
┌────────▼────────┐
│   Backend API   │
│   (FastAPI)     │
└────────┬────────┘
         │
┌────────▼────────────────────────────────┐
│         AI Agent Workflow               │
│  ┌──────────────────────────────────┐  │
│  │ 1. Coordinator (Phi-2)           │  │
│  │    ↓                             │  │
│  │ 2. Text Generator (Zephyr-7B)   │  │
│  │    ↓                             │  │
│  │ 3. Reviewer (Phi-2)             │  │
│  │    ↓                             │  │
│  │ 4. Image Prompt (Zephyr-7B)     │  │
│  │    ↓                             │  │
│  │ 5. Compliance (Zephyr-7B)       │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PyTorch** - Deep learning framework
- **Transformers** - Hugging Face models
- **LangChain** - LLM orchestration
- **LangGraph** - Agent workflow management
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI library
- **TailwindCSS** - Utility-first CSS
- **Axios** - HTTP client
- **Lucide React** - Icon library

### AI Models
- **HuggingFaceH4/zephyr-7b-beta** - Writing & compliance
- **microsoft/phi-2** - Reviewing & coordination
- **4-bit quantization** - Memory optimization

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- 10GB+ free disk space (for models)
- GPU recommended (optional)

### 1. Clone the Repository

```bash
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon
```

### 2. Start the Backend

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start the API server
python main.py
```

The backend will start on `http://localhost:8000`

**Note:** First run will download AI models (~10GB). This takes 5-10 minutes.

### 3. Start the Frontend

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will open at `http://localhost:3000`

### 4. Use the Application

1. Fill in the product/campaign description
2. Select tone and style
3. Click "Generate Content"
4. Wait 2-4 minutes for AI generation
5. View results, copy, or download

---

## 📁 Project Structure

```
Neural-Hackathon/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── workflow.py       # AI agent system
│   ├── main.py               # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── index.js
│   │   └── index.css        # Tailwind styles
│   ├── package.json
│   ├── tailwind.config.js
│   └── README.md
├── Neural.ipynb             # Original prototype
└── README.md               # This file
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Generate Content
```http
POST /api/generate
Content-Type: application/json

{
  "user_instruction": "Create an Instagram post promoting EcoWave reusable water bottles.",
  "tone": "Fun and Playful",
  "style": "Short caption with 3-4 hashtags"
}
```

**Response:**
```json
{
  "success": true,
  "reviewed_text": "Generated caption...",
  "image_prompt": "Generated image description...",
  "compliance_status": "approved",
  "compliance_feedback": "Content approved",
  "iteration": 1,
  "elapsed_time": 145.2,
  "generated_at": "2025-11-15T10:30:00"
}
```

#### Health Check
```http
GET /health
```

#### API Documentation
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

---

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Test health endpoint
curl http://localhost:8000/health

# Test content generation
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_instruction": "Create an Instagram post promoting EcoWave reusable water bottles.",
    "tone": "Fun and Playful",
    "style": "Short caption with 3-4 hashtags"
  }'
```

### Frontend Testing

1. Open `http://localhost:3000`
2. Fill in the form
3. Click "Generate Content"
4. Verify results display correctly

---

## 🚢 Deployment

### Backend Deployment

**Option 1: Render**
```bash
# Create render.yaml in backend/
service: web
env: python
buildCommand: pip install -r requirements.txt
startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Option 2: Railway**
```bash
railway init
railway up
```

**Option 3: AWS EC2**
```bash
# SSH into EC2 instance
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
python3 main.py
```

### Frontend Deployment

**Option 1: Vercel (Recommended)**
```bash
cd frontend
npm install -g vercel
vercel
```

**Option 2: Netlify**
```bash
cd frontend
npm run build
# Drag & drop build/ folder to Netlify
```

**Option 3: GitHub Pages**
```bash
cd frontend
npm run build
# Deploy build/ folder
```

---

## 📊 Performance

- **First Generation**: 2-4 minutes (model loading)
- **Subsequent Generations**: 1-2 minutes
- **Model Size**: ~10GB (cached)
- **Memory Usage**: 8-12GB RAM
- **GPU Acceleration**: Supported (optional)

---

## 🔐 Environment Variables

### Backend (.env)
```env
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
MODEL_CACHE_DIR=./model_cache
LOG_LEVEL=INFO
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 🐛 Troubleshooting

### Backend Issues

**Models not loading:**
```bash
# Clear cache and retry
rm -rf model_cache/
python main.py
```

**CUDA errors:**
```bash
# Force CPU mode
export CUDA_VISIBLE_DEVICES=""
python main.py
```

### Frontend Issues

**API connection errors:**
- Ensure backend is running on port 8000
- Check REACT_APP_API_URL in .env
- Verify CORS settings in backend

**Build errors:**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## 📝 License

MIT License - Built for Neural Hackathon 2025

---

## 👥 Team

- **Abdul Farooqui** - Frontend Developer & Integration

---

## 🙏 Acknowledgments

- Hugging Face for AI models
- FastAPI & React communities
- Neural Hackathon organizers

---

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Check API docs at `/docs`
- Review logs in terminal

---

**Built with ❤️ for the Neural Hackathon**
