# How to Start the Futures-War Project

## 🚀 Quickest Start

```bash
bash start.sh
```

- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📋 All Startup Options

### 1. Both Backend + Frontend
```bash
bash start.sh all
```
Starts both services simultaneously:
- Backend on port 8000
- Frontend on port 3000

### 2. Backend Only
```bash
bash start.sh backend
```
Runs FastAPI backend with:
- API on http://localhost:8000
- Interactive docs at http://localhost:8000/docs

### 3. Frontend Only
```bash
bash start.sh frontend
```
Runs web interface on http://localhost:3000

### 4. With Docker Compose
```bash
bash start.sh docker
```
Or directly:
```bash
docker-compose up
```

### 5. Run Tests
```bash
bash start.sh test
```
Runs pytest on `backend/test_api.py`
- ✅ All 5 tests should pass

### 6. Stop Services
```bash
bash start.sh stop
```
Stops all running services

---

## 🔧 Manual Start (Development)

If you need to start the backend manually:

```bash
cd backend
source ../.venv/bin/activate
python main.py
```

Or with uvicorn directly:
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🔌 Quick API Tests

Once the server is running, test the API:

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Moderation:**
```bash
curl -X POST "http://localhost:8000/moderate?text=I%20love%20Marseille"
```

**Enrichment:**
```bash
curl -X POST "http://localhost:8000/enrich?text=city&style=cyberpunk"
```

**Image Generation:**
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"marseille future","style":"futuristic"}'
```

---

## ⚙️ Environment Setup

Your `.env` file is already configured with:
- LLM API Token: `tristanlovesia`
- LLM API URL: `http://37.26.187.4:8000`

To update credentials:
```bash
# Edit .env file
nano .env
```

---

## 🐛 Troubleshooting

### Port 8000 is already in use
```bash
# Kill the process using port 8000
kill -9 $(lsof -ti:8000)
bash start.sh
```

### Microphone not working
- Allow microphone access in browser settings
- Check browser console for errors (F12)

### Backend not responding
- Verify backend is running: `bash start.sh backend`
- Wait 2-3 seconds for startup
- Check health: `curl http://localhost:8000/health`

### Virtual environment issues
```bash
# Reactivate venv
source .venv/bin/activate
bash start.sh
```

---

## 📁 What Gets Started

- **Backend**: FastAPI server with all API endpoints
- **Frontend**: Web interface with audio recording
- **API Docs**: Interactive Swagger docs at `/docs`

---

## 🎯 Next Steps

1. Start the project: `bash start.sh`
2. Open http://localhost:8000 in your browser
3. Record audio and watch the full pipeline work
4. Check API docs at http://localhost:8000/docs for all endpoints

**Everything is ready!** 🎉
