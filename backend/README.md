# AI Social Media Content Generator - Backend

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
cp .env.example .env
# Edit .env as needed
```

### 3. Run the API

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

- **GET /** - API info
- **GET /health** - Health check
- **POST /api/generate** - Generate content
- **GET /api/models/status** - Check model status
- **GET /docs** - Interactive API documentation
- **GET /redoc** - Alternative API documentation

## 🧪 Testing

Test the API using curl:

```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "user_instruction": "Create an Instagram post promoting EcoWave reusable water bottles.",
    "tone": "fun, friendly, eco-conscious",
    "style": "short caption with 3-4 hashtags"
  }'
```

## 📦 Project Structure

```
backend/
├── main.py              # FastAPI application
├── agents/
│   └── workflow.py      # AI agent workflow
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## 🔧 Tech Stack

- **FastAPI** - Modern web framework
- **PyTorch** - ML framework
- **Transformers** - Hugging Face models
- **LangChain** - LLM orchestration
- **LangGraph** - Agent workflow management

## 📝 Notes

- First run will download models (~10GB)
- Models are cached for subsequent runs
- GPU recommended but not required
- Supports 4-bit quantization for efficiency
