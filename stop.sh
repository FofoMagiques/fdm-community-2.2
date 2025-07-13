#!/bin/bash

# Script d'arrêt FDM Community
# À utiliser sur votre NAS Synology

echo "🛑 Arrêt de FDM Community"
echo "========================"

# Obtenir le répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Répertoire du projet: $SCRIPT_DIR"

# Aller dans le dossier du projet
cd "$SCRIPT_DIR"

# Arrêter les conteneurs
echo "🛑 Arrêt des conteneurs..."
docker-compose down

# Nettoyer les images inutilisées (optionnel)
echo "🧹 Nettoyage des images inutilisées..."
docker system prune -f

echo "✅ FDM Community arrêté !"