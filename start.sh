#!/bin/bash

# Script de démarrage FDM Community
# À utiliser sur votre NAS Synology

echo "🚀 Démarrage de FDM Community avec Docker"
echo "========================================"

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker sur votre NAS."
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose sur votre NAS."
    exit 1
fi

# Obtenir le répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "📁 Répertoire du projet: $SCRIPT_DIR"

# Aller dans le dossier du projet
cd "$SCRIPT_DIR"

# Vérifier que les fichiers .env existent
if [ ! -f "./backend/.env" ]; then
    echo "❌ Fichier ./backend/.env manquant"
    exit 1
fi

if [ ! -f "./frontend/.env" ]; then
    echo "❌ Fichier ./frontend/.env manquant"
    exit 1
fi

# Arrêter les conteneurs existants
echo "🛑 Arrêt des conteneurs existants..."
docker-compose down

# Construire et démarrer les services
echo "🏗️  Construction et démarrage des services..."
docker-compose up -d --build

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 30

# Vérifier l'état des services
echo "📊 État des services:"
docker-compose ps

# Tester les services
echo "🧪 Test des services..."
echo "Backend API:"
curl -s http://localhost:8001/api/ && echo "✅ Backend OK" || echo "❌ Backend non accessible"

echo "Frontend:"
curl -s -I http://localhost:3000 | head -1 && echo "✅ Frontend OK" || echo "❌ Frontend non accessible"

echo ""
echo "✅ FDM Community est démarré !"
echo "🌐 Site web: http://localhost:3000"
echo "🔧 API: http://localhost:8001/api/"
echo ""
echo "📝 Logs en temps réel:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Pour arrêter:"
echo "   docker-compose down"