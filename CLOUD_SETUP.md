# ☁️ Cloud-Based Setup Guide

## Perfect for MacBooks with Limited RAM/Storage!

This guide shows you how to run the AI models in the cloud instead of locally on your MacBook.

---

## 🎯 Why Use Cloud Models?

✅ **No local model downloads** (~10GB saved!)
✅ **No RAM limitations** (runs on Hugging Face servers)
✅ **Works on any MacBook** (even M1/M2 with limited RAM)
✅ **Faster startup** (no model loading time)
✅ **FREE tier available** (Hugging Face provides free API access)

---

## 📋 Setup Steps

### Step 1: Get Free Hugging Face API Token

1. **Create account** (if you don't have one):
   - Go to https://huggingface.co/join
   - Sign up for free

2. **Generate API token**:
   - Go to https://huggingface.co/settings/tokens
   - Click "New token"
   - Name it: `neural-hackathon`
   - Type: **Read** (default)
   - Click "Generate token"
   - **COPY the token** (you'll need it in next step)

### Step 2: Configure Backend

1. **Open terminal** and navigate to backend:
   ```bash
   cd /Users/abdulfarooqui/Desktop/Neural-Hackathon/backend
   ```

2. **Create/edit `.env` file**:
   ```bash
   nano .env
   ```

3. **Add your token**:
   ```
   HUGGINGFACE_API_TOKEN=hf_your_token_here
   ```
   
   Replace `hf_your_token_here` with the token you copied.

4. **Save and exit**:
   - Press `Ctrl + O` (save)
   - Press `Enter` (confirm)
   - Press `Ctrl + X` (exit)

### Step 3: Install Cloud Dependencies

Already done! The requirements are already installed.

### Step 4: Run Cloud Version

**Terminal 1 - Backend (Cloud):**
```bash
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon/backend
source venv/bin/activate
python main_cloud.py
```

**Terminal 2 - Frontend:**
```bash
cd /Users/abdulfarooqui/Desktop/Neural-Hackathon/frontend
npm install @tailwindcss/postcss
npm start
```

---

## 🚀 Quick Start Script

Or use this one-liner in each terminal:

**Terminal 1:**
```bash
cd ~/Desktop/Neural-Hackathon/backend && source venv/bin/activate && python main_cloud.py
```

**Terminal 2:**
```bash
cd ~/Desktop/Neural-Hackathon/frontend && npm start
```

---

## ✅ Verify It's Working

1. **Backend should show**:
   ```
   ☁️ AI SOCIAL MEDIA CONTENT GENERATOR API (CLOUD)
   📡 Starting server on http://localhost:8000
   💡 Using Hugging Face Inference API (No local models needed!)
   ```

2. **Test the API**:
   ```bash
   curl http://localhost:8000/api/models/status
   ```
   
   Should return:
   ```json
   {
     "configured": true,
     "model_type": "cloud",
     "status": "ready"
   }
   ```

3. **Open frontend**: http://localhost:3000

---

## 🎨 What Changed?

### Cloud Version Uses:
- **No local model files** (everything runs on Hugging Face servers)
- **Mistral-7B-Instruct** via API (fast & free)
- **Same features** as local version
- **Slightly slower** (network latency) but **much lighter** on your Mac

### Local Version Uses:
- **Downloads ~10GB models** to your Mac
- **Zephyr-7B & Phi-2** models locally
- **Uses your RAM** (8GB+ needed)
- **Faster response** (no network latency)

---

## 💡 Free Tier Limits

Hugging Face free tier provides:
- **Rate limit**: ~100 requests/hour
- **Perfect for**: Development, demos, hackathons
- **Cost**: $0 (completely free)

For production with higher limits:
- Upgrade to Hugging Face Pro ($9/month)
- Or deploy your own models on other cloud platforms

---

## 🔧 Troubleshooting

### Error: "API token not configured"

**Solution**:
```bash
cd ~/Desktop/Neural-Hackathon/backend
echo 'HUGGINGFACE_API_TOKEN=hf_your_token_here' > .env
```

### Error: "Rate limit exceeded"

**Solution**: You've hit the free tier limit. Wait an hour or upgrade to Pro.

### Error: "Model loading failed"

**Solution**: Check internet connection. Cloud models require internet access.

### Frontend won't start

**Solution**:
```bash
cd ~/Desktop/Neural-Hackathon/frontend
npm install @tailwindcss/postcss
npm start
```

---

## 📊 Comparison Table

| Feature | Local Models | Cloud Models (☁️) |
|---------|-------------|------------------|
| Setup Time | 10-20 mins | 2 mins |
| Storage | ~10GB | ~0GB |
| RAM Usage | 8GB+ | Minimal |
| Speed | Fast (local) | Medium (network) |
| Cost | Free | Free (with limits) |
| Internet | Not needed | Required |
| Mac Compatibility | M1/M2 issues | Works everywhere |

---

## 🎯 For Your Hackathon Demo

**Recommended**: Use **Cloud Version** because:
1. ✅ Faster setup (2 minutes vs 20 minutes)
2. ✅ No storage issues on your Mac
3. ✅ No RAM limitations
4. ✅ More reliable (no local model issues)
5. ✅ Same impressive features for judges

Just make sure you have:
- ✅ Internet connection at the venue
- ✅ Backup demo video (in case of network issues)
- ✅ Screenshots of working app

---

## 🚀 Other Cloud Options

If you need even more power:

### Option 2: Google Colab (FREE GPU)
```python
# Run models on Google's free GPU
# Good for: Training, heavy processing
# Limit: 12 hours per session
```

### Option 3: Replicate.com
```python
# Pay-per-use API
# Good for: Production apps
# Cost: ~$0.002 per request
```

### Option 4: AWS SageMaker / Azure ML
```python
# Enterprise solutions
# Good for: Large scale production
# Cost: ~$0.05-0.50 per hour
```

---

## 📞 Quick Commands Reference

### Start Cloud Backend
```bash
cd ~/Desktop/Neural-Hackathon/backend
source venv/bin/activate
python main_cloud.py
```

### Check API Status
```bash
curl http://localhost:8000/api/models/status
```

### Test Content Generation
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "user_instruction": "Create an Instagram post for eco-friendly water bottles",
    "tone": "Fun and Playful",
    "style": "Short caption with hashtags"
  }'
```

### View Logs
```bash
tail -f backend.log
```

---

## 🎉 Ready to Test!

Your project is now configured for **cloud-based AI** that works perfectly on any MacBook!

**Next steps**:
1. ✅ Get your Hugging Face API token
2. ✅ Add it to `.env` file
3. ✅ Run `python main_cloud.py`
4. ✅ Test in browser at http://localhost:3000

**Need help?** Check the troubleshooting section above!
