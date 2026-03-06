# Utilise une version légère de Python
FROM python:3.10-slim

# Définit le dossier de travail
WORKDIR /app

# IMPORTANT : Installe curl (car ton code python l'utilise via subprocess)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copie les dépendances et installe-les
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code
COPY . .

# Ouvre le port 8000
EXPOSE 8000

# Lance le serveur (adapte "main:app" si ton fichier principal ne s'appelle pas main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]