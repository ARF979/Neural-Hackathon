# 🎯 Command Reference Guide

Quick reference for all commands you'll need.

---

## 🚀 Quick Start Commands

### Start Everything (Easiest)
```bash
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon
./start.sh
```

### Check If Servers Are Running
```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
open http://localhost:3000
```

---

## 🐍 Backend Commands

### Setup
```bash
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon/backend

# Create virtual environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run
```bash
# Start server
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Test
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test generation (full example)
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "user_instruction": "Create an Instagram post promoting EcoWave reusable water bottles.",
    "tone": "Fun and Playful",
    "style": "Short caption with 3-4 hashtags"
  }'

# Check models status
curl http://localhost:8000/api/models/status
```

### Maintenance
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Clear model cache
rm -rf model_cache/

# View logs
tail -f backend.log

# Deactivate virtual environment
deactivate
```

---

## ⚛️ Frontend Commands

### Setup
```bash
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon/frontend

# Install dependencies
npm install

# Or use yarn
yarn install
```

### Run
```bash
# Start development server
npm start

# Or with yarn
yarn start

# Build for production
npm run build

# Serve production build locally
npx serve -s build
```

### Test
```bash
# Run tests
npm test

# Check for issues
npm run lint

# Fix auto-fixable issues
npm run lint --fix
```

### Maintenance
```bash
# Update dependencies
npm update

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check for outdated packages
npm outdated

# Update specific package
npm install axios@latest
```

---

## 🔧 Development Commands

### Git Commands
```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Social Media Generator"

# Create .gitignore
cat > .gitignore << EOF
# Backend
backend/__pycache__/
backend/venv/
backend/model_cache/
backend/*.log
backend/.env

# Frontend  
frontend/node_modules/
frontend/build/
frontend/.env.local

# OS
.DS_Store
*.swp
EOF
```

### Environment Management
```bash
# Backend - Copy example env
cd backend
cp .env.example .env
# Edit as needed
nano .env

# Frontend - Create env
cd frontend
echo "REACT_APP_API_URL=http://localhost:8000" > .env
```

---

## 🐛 Troubleshooting Commands

### Check Ports
```bash
# See what's using port 8000
lsof -i :8000

# See what's using port 3000  
lsof -i :3000

# Kill process on port
kill -9 $(lsof -t -i:8000)
kill -9 $(lsof -t -i:3000)
```

### Process Management
```bash
# Find running Python processes
ps aux | grep python

# Find running Node processes
ps aux | grep node

# Kill by name
pkill -f "python main.py"
pkill -f "react-scripts"

# Kill all Python
pkill python

# Kill all Node
pkill node
```

### System Resources
```bash
# Check disk space
df -h

# Check memory usage
free -h  # Linux
vm_stat  # macOS

# Check CPU usage
top

# Check GPU (if NVIDIA)
nvidia-smi
```

### Network
```bash
# Test localhost connection
curl localhost:8000

# Test with verbose output
curl -v localhost:8000/health

# Test POST request
curl -X POST localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"user_instruction":"test","tone":"fun","style":"short"}'

# Check open ports
netstat -an | grep LISTEN
```

---

## 📦 Package Management

### Python (pip)
```bash
# Install specific version
pip install fastapi==0.104.1

# Install from requirements
pip install -r requirements.txt

# Freeze current packages
pip freeze > requirements.txt

# Uninstall package
pip uninstall package-name

# List installed
pip list

# Show package info
pip show fastapi
```

### Node (npm)
```bash
# Install specific version
npm install react@19.0.0

# Install dev dependency
npm install --save-dev package-name

# Install globally
npm install -g package-name

# Uninstall
npm uninstall package-name

# List installed
npm list --depth=0

# Show package info
npm info react
```

---

## 🧪 Testing Commands

### Backend Testing
```bash
cd backend

# Test with Python
python -m pytest

# Test specific file
python -m pytest tests/test_api.py

# Test with coverage
python -m pytest --cov=.

# Run single endpoint test
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d @test_data.json
```

### Frontend Testing
```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test
npm test -- App.test.js

# Run in CI mode
CI=true npm test
```

---

## 🚢 Deployment Commands

### Backend Deployment
```bash
# Install production dependencies only
pip install -r requirements.txt --no-dev

# Run with production server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Docker build (if using)
docker build -t ai-content-generator-backend .
docker run -p 8000:8000 ai-content-generator-backend

# Heroku deployment
heroku create
git push heroku main
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Deploy to Vercel
vercel

# Deploy to Netlify
netlify deploy --prod

# Deploy to GitHub Pages
npm run build
npm run deploy
```

---

## 📊 Monitoring Commands

### Logs
```bash
# Backend logs
tail -f backend/backend.log

# Follow multiple logs
tail -f backend/*.log

# Search in logs
grep "ERROR" backend/backend.log

# Last 100 lines
tail -n 100 backend/backend.log
```

### Performance
```bash
# Monitor CPU/Memory
htop  # If installed
top

# Check disk I/O
iostat

# Network monitoring
iftop  # If installed

# Process tree
pstree -p $(pgrep python)
```

---

## 🔐 Security Commands

### Environment
```bash
# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Check environment variables
printenv | grep REACT_APP

# Unset environment variable
unset VARIABLE_NAME
```

### Permissions
```bash
# Make script executable
chmod +x start.sh

# Secure env files
chmod 600 .env

# Check file permissions
ls -la .env
```

---

## 📚 Documentation Commands

### API Documentation
```bash
# Open API docs in browser
open http://localhost:8000/docs

# Or alternative docs
open http://localhost:8000/redoc

# Generate OpenAPI schema
curl http://localhost:8000/openapi.json > openapi.json
```

### Code Documentation
```bash
# Generate Python docs
cd backend
pdoc --html --output-dir docs .

# Generate JS docs
cd frontend
npx jsdoc src -r -d docs
```

---

## 🎨 Style/Format Commands

### Python
```bash
# Format with black
black backend/

# Check with flake8
flake8 backend/

# Type checking with mypy
mypy backend/
```

### JavaScript
```bash
# Format with prettier
npx prettier --write "src/**/*.{js,jsx,json,css}"

# Check formatting
npx prettier --check "src/**/*.{js,jsx,json,css}"

# ESLint
npx eslint src/
```

---

## 🧹 Cleanup Commands

### Backend
```bash
cd backend

# Remove cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Remove virtual environment
rm -rf venv/

# Remove model cache
rm -rf model_cache/
```

### Frontend
```bash
cd frontend

# Remove dependencies
rm -rf node_modules/

# Remove build files
rm -rf build/

# Clean cache
npm cache clean --force
```

### Full Cleanup
```bash
# Remove all generated files
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon

rm -rf backend/venv/
rm -rf backend/__pycache__/
rm -rf backend/model_cache/
rm -rf frontend/node_modules/
rm -rf frontend/build/
rm -f backend/*.log
```

---

## ⚡ Quick Aliases (Add to ~/.zshrc)

```bash
# Add these to your ~/.zshrc for quick access

# Navigate to project
alias neural='cd /Users/abdulfarooqui/Desktop/Neural-Hackathon'

# Start backend
alias neural-backend='cd /Users/abdulfarooqui/Desktop/Neural-Hackathon/backend && source venv/bin/activate && python main.py'

# Start frontend
alias neural-frontend='cd /Users/abdulfarooqui/Desktop/Neural-Hackathon/frontend && npm start'

# Test API
alias neural-test='curl http://localhost:8000/health'

# View logs
alias neural-logs='tail -f /Users/abdulfarooqui/Desktop/Neural-Hackathon/backend/backend.log'

# Then reload:
source ~/.zshrc
```

---

## 🎯 Essential Command Sequence

### First Time Setup
```bash
# 1. Navigate to project
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon

# 2. Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# 3. Setup frontend
cd frontend
npm install
cd ..

# 4. Run everything
./start.sh
```

### Daily Development
```bash
# Terminal 1 - Backend
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon/backend
source venv/bin/activate
python main.py

# Terminal 2 - Frontend
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon/frontend
npm start

# Terminal 3 - Testing
curl http://localhost:8000/health
open http://localhost:3000
```

---

## 💾 Backup Commands

```bash
# Backup project (excluding large files)
cd /Users/abdulfarooqui/Desktop
tar -czf neural-hackathon-backup.tar.gz \
  --exclude='node_modules' \
  --exclude='venv' \
  --exclude='model_cache' \
  --exclude='__pycache__' \
  Neural-Hackathon/

# Restore from backup
tar -xzf neural-hackathon-backup.tar.gz
```

---

## 📞 Emergency Commands

If nothing works:

```bash
# Nuclear option - full reinstall
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon

# Backend
cd backend
rm -rf venv model_cache __pycache__ *.log
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Frontend
cd ../frontend
rm -rf node_modules package-lock.json build
npm install

# Restart
cd ..
./start.sh
```

---

**Keep this guide handy during development! 🚀**
