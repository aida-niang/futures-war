# Utilise Nginx
FROM nginx:alpine

# Copie tes fichiers statiques
COPY . /usr/share/nginx/html

# EXPOSE LE PORT 80 (Le standard pour Nginx)
EXPOSE 80