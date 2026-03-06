FROM python:3.11-slim

WORKDIR /app

# 1. Installation des dépendances système (CURL et FFMPEG pour Whisper)
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 2. Copie et installation des bibliothèques Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copie de tout le code source du backend
COPY . .

# 4. Exposition du port pour Dokploy
EXPOSE 8000

# 5. Lancement de l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]