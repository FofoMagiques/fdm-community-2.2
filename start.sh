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

# Aller dans le dossier du projet
cd /volume1/web/FDM

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
curl -s http://teamfdm.fr:8001/api/ || echo "❌ Backend non accessible"

echo "Frontend:"
curl -s -I http://teamfdm.fr:3000 | head -1 || echo "❌ Frontend non accessible"

echo ""
echo "✅ FDM Community est démarré !"
echo "🌐 Site web: http://teamfdm.fr:3000"
echo "🔧 API: http://teamfdm.fr:8001/api/"
echo ""
echo "📝 Logs en temps réel:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Pour arrêter:"
echo "   docker-compose down"