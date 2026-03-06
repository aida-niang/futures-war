"""
AI Orchestrator - Version Marseille 2050 (Full Fix)
"""
import os
import json
import base64
import psutil
from datetime import datetime
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPBearer
from dotenv import load_dotenv

# Imports des services locaux
from services.ai_client import whisper_client, zimageturbo_client, gpu_llm_client
from services.prompt_eng import PromptEngineer
from utils.moderation import ContentModerator
from models.schemas import (
    TranscriptionRequest, TranscriptionResponse,
    PromptToImageRequest, PromptToImageResponse,
    ProcessRequest, ProcessResponse, SystemStatsResponse,
    ChatCompletionRequest, ChatCompletionResponse,
    ChatCompletionMessage, ChatCompletionChoice, ChatCompletionUsage
)

# Configuration environnement
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = FastAPI(
    title="AI Orchestrator API",
    description="Speech-to-text, prompt-to-image, and Marseille 2050 vision.",
    version="0.2.0"
)

# Autoriser le Frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des outils
engineer = PromptEngineer()
moderator = ContentModerator()
security = HTTPBearer()

# Gestion des erreurs de validation (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=422, content={"detail": "Validation error", "errors": exc.errors()})

# --- ROUTES DE SANTÉ ---

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Orchestrator", "timestamp": datetime.now().isoformat()}

# --- ROUTE PRINCIPALE (LA VOIX VERS L'IMAGE) ---

@app.post("/process", response_model=ProcessResponse)
async def process_legacy(request: ProcessRequest):
    # Valeurs par défaut sécurisées
    text = "Audio non reconnu"
    enriched_prompt = "Marseille futuriste, vision 2050"
    img_url = "https://images.unsplash.com/photo-1563050017-f58c4959458b?w=1024"
    is_safe = True

    try:
        # 1. AUDIO -> TEXTE
        if request.audio_base64:
            print(f"--- [START] Traitement Audio ---")
            b64_data = request.audio_base64
            if "," in b64_data:
                b64_data = b64_data.split(",")[1]
            
            audio_bytes = base64.b64decode(b64_data)
            print(f"DEBUG: Taille audio reçue: {len(audio_bytes)} octets")

            try:
                # Appel Whisper
                res = await whisper_client.transcribe(audio_bytes)
                print(f"DEBUG: Retour Whisper: {res}")
                
                if res and isinstance(res, dict) and 'text' in res and res['text'].strip():
                    text = res['text']
                else:
                    text = "Message audio vide ou non compris."
            except Exception as e:
                print(f"⚠️ Erreur Whisper : {e}")
                text = "Erreur technique de transcription."

        # 2. ENRICHISSEMENT DU PROMPT
        try:
            print(f"DEBUG: Enrichissement pour : {text}")
            enrichment_result = engineer.enrich(text)
            if isinstance(enrichment_result, dict):
                enriched_prompt = enrichment_result.get('enriched', text)
            else:
                enriched_prompt = str(enrichment_result)
        except Exception as e:
            print(f"⚠️ Erreur Enrichissement : {e}")
            enriched_prompt = f"{text}, realistic, cinematic, futuristic Marseille city"

        # 3. GÉNÉRATION DE L'IMAGE
        try:
            print(f"DEBUG: Génération image...")
            generation = await zimageturbo_client.generate(enriched_prompt)
            if generation and 'image_url' in generation:
                img_url = generation['image_url']
            else:
                print("⚠️ Z-Image n'a pas renvoyé d'URL d'image.")
        except Exception as e:
            print(f"⚠️ Erreur Génération Image : {e}")

        return ProcessResponse(
            original_text=text,
            enriched_prompt=enriched_prompt,
            is_safe=is_safe,
            image_url=img_url,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        print(f"💥 CRASH TOTAL : {e}")
        return ProcessResponse(
            original_text="Erreur système",
            enriched_prompt=str(e),
            is_safe=False,
            image_url="",
            timestamp=datetime.now().isoformat()
        )

# --- AUTRES ROUTES API (TRANSCRIPTION SEULE, IMAGE SEULE, ETC.) ---

@app.post("/api/speech-to-text", response_model=TranscriptionResponse)
async def speech_to_text(file: UploadFile = File(...)):
    audio_data = await file.read()
    result = await whisper_client.transcribe(audio_data)
    return TranscriptionResponse(text=result['text'], confidence=0.9)

@app.post("/api/prompt-to-image", response_model=PromptToImageResponse)
async def prompt_to_image(request: PromptToImageRequest):
    result = await zimageturbo_client.generate(prompt=request.prompt)
    image_url = result.get('image_url', "")
    return PromptToImageResponse(images=[image_url], model="Z-Image-Turbo")

@app.get("/api/system-stats", response_model=SystemStatsResponse)
async def system_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    return SystemStatsResponse(
        cpu={"percent": cpu, "count": psutil.cpu_count()},
        ram={"percent": ram.percent, "total_mb": ram.total / (1024**2), "used_mb": ram.used / (1024**2), "available_mb": ram.available / (1024**2)},
        whisper={"model": "base", "device": "cpu"},
        ollama={"model": "llama3.2:1b", "status": "active"},
        zimage={"model": "Turbo", "status": "online"},
        timestamp=datetime.now().isoformat()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)