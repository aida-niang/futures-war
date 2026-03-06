# On utilise Nginx pour afficher ton site web
FROM nginx:alpine

# On copie les fichiers de ton interface web vers le dossier public de Nginx
# (Assure-toi que tes fichiers HTML/CSS/JS sont bien accessibles ici)
COPY . /usr/share/nginx/html

# On expose le port 80 pour le web
EXPOSE 3000