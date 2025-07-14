FROM nginx:alpine

# Copier la configuration Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Créer les répertoires pour les certificats
RUN mkdir -p /etc/ssl/certs /etc/ssl/private

# Exposer les ports
EXPOSE 80 443

# Commande par défaut
CMD ["nginx", "-g", "daemon off;"]