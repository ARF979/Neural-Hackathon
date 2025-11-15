#!/bin/bash

# Quick Start Script for Cloud Version
# Perfect for MacBooks with limited RAM/storage!

echo "════════════════════════════════════════════════════════════"
echo "   ☁️ CLOUD-BASED AI CONTENT GENERATOR"
echo "   No local models needed! Runs on Hugging Face servers"
echo "════════════════════════════════════════════════════════════"
echo ""

# Check if HF token is set
if [ -f "backend/.env" ]; then
    if grep -q "HUGGINGFACE_API_TOKEN" backend/.env; then
        echo "✅ Hugging Face API token found"
    else
        echo "❌ No Hugging Face API token found in backend/.env"
        echo ""
        echo "📝 Quick setup:"
        echo "1. Get free token: https://huggingface.co/settings/tokens"
        echo "2. Add to backend/.env:"
        echo "   HUGGINGFACE_API_TOKEN=hf_your_token_here"
        echo ""
        exit 1
    fi
else
    echo "❌ No .env file found"
    echo ""
    echo "📝 Creating .env file..."
    echo "Please add your Hugging Face API token:"
    echo ""
    echo "1. Get free token: https://huggingface.co/settings/tokens"
    echo "2. Run: echo 'HUGGINGFACE_API_TOKEN=hf_your_token' > backend/.env"
    echo ""
    exit 1
fi

echo ""
echo "🚀 Starting services..."
echo ""

# Start backend in background
echo "📡 Starting cloud-based backend API..."
cd backend
source venv/bin/activate
python main_cloud.py > ../backend_cloud.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "   Backend PID: $BACKEND_PID"
echo "   Logs: backend_cloud.log"

# Wait for backend to start
echo "   Waiting for backend to start..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "   ✅ Backend is running!"
else
    echo "   ⚠️ Backend may still be starting..."
fi

echo ""
echo "🎨 Starting frontend..."
cd frontend

# Check if postcss is configured
if ! grep -q "@tailwindcss/postcss" postcss.config.js 2>/dev/null; then
    echo "   📦 Fixing Tailwind CSS configuration..."
    cat > postcss.config.js << 'EOF'
module.exports = {
  plugins: {
    '@tailwindcss/postcss': {},
  },
};
EOF
fi

npm start > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "   Frontend PID: $FRONTEND_PID"
echo "   Logs: frontend.log"

echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ Setup Complete!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "🌐 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Running in CLOUD MODE:"
echo "   ✅ No local model downloads needed"
echo "   ✅ Minimal RAM usage"
echo "   ✅ Perfect for your MacBook!"
echo ""
echo "📊 Monitor:"
echo "   Backend logs: tail -f backend_cloud.log"
echo "   Frontend logs: tail -f frontend.log"
echo ""
echo "🛑 To stop both servers:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "════════════════════════════════════════════════════════════"
echo "🎉 Happy Hacking! Your cloud-based AI is ready!"
echo "════════════════════════════════════════════════════════════"
