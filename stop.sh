#!/bin/bash

# Script d'arrêt FDM Community
# À utiliser sur votre NAS Synology

echo "🛑 Arrêt de FDM Community"
echo "========================"

# Aller dans le dossier du projet
cd /volume1/web/FDM

# Arrêter les conteneurs
echo "🛑 Arrêt des conteneurs..."
docker-compose down

# Nettoyer les images inutilisées (optionnel)
echo "🧹 Nettoyage des images inutilisées..."
docker system prune -f

echo "✅ FDM Community arrêté !"