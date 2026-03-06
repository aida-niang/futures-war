FROM python:3.11-slim

# On définit le répertoire de travail dans le conteneur
WORKDIR /app

# 1. Installation des dépendances système (CURL est obligatoire pour ton WhisperClient)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Copie et installation des bibliothèques Python
# Note : On suppose que ton Dockerfile est à la racine et ton code dans /backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copie de tout le code source du dossier backend vers /app
COPY backend/ .

# 4. Exposition du port pour Dokploy
EXPOSE 8000

# 5. Lancement de l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]