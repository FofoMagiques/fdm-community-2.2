#!/bin/bash

# Script de nettoyage et redémarrage FDM Community
# Résout les problèmes de Docker après modifications

echo "🧹 Nettoyage et redémarrage FDM Community"
echo "========================================="

# Obtenir le répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Fonction pour nettoyer et redémarrer
cleanup_and_restart() {
    local compose_file=$1
    local mode=$2
    
    echo "🛑 Arrêt des conteneurs $mode..."
    docker-compose -f "$compose_file" down -v
    
    echo "🗑️  Suppression des images anciennes..."
    docker rmi -f fdm_backend_prod fdm_frontend_prod 2>/dev/null || true
    docker rmi -f fdm_backend fdm_frontend 2>/dev/null || true
    
    echo "🧹 Nettoyage du système Docker..."
    docker system prune -f
    
    echo "🏗️  Reconstruction des images..."
    docker-compose -f "$compose_file" build --no-cache
    
    echo "🚀 Démarrage des services..."
    docker-compose -f "$compose_file" up -d
    
    echo "⏳ Attente du démarrage (30 secondes)..."
    sleep 30
    
    echo "📊 État des services:"
    docker-compose -f "$compose_file" ps
}

# Menu de sélection
echo "Choisissez le mode :"
echo "1. Développement (docker-compose.yml)"
echo "2. Production (docker-compose.production.yml)"
echo "3. Les deux"
echo ""
read -p "Votre choix (1-3) : " choice

case $choice in
    1)
        cleanup_and_restart "docker-compose.yml" "développement"
        ;;
    2)
        cleanup_and_restart "docker-compose.production.yml" "production"
        ;;
    3)
        cleanup_and_restart "docker-compose.yml" "développement"
        echo ""
        cleanup_and_restart "docker-compose.production.yml" "production"
        ;;
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
echo "✅ Nettoyage et redémarrage terminés !"
echo ""
echo "🧪 Tests de connectivité :"
if [ "$choice" = "1" ] || [ "$choice" = "3" ]; then
    echo "📱 Test développement :"
    curl -s http://localhost:8001/api/ && echo "✅ Backend dev OK" || echo "❌ Backend dev KO"
    curl -s -I http://localhost:3000 | head -1 && echo "✅ Frontend dev OK" || echo "❌ Frontend dev KO"
fi

if [ "$choice" = "2" ] || [ "$choice" = "3" ]; then
    echo "🏭 Test production :"
    curl -s http://localhost:8001/api/ && echo "✅ Backend prod OK" || echo "❌ Backend prod KO"
    curl -s -I http://localhost:3000 | head -1 && echo "✅ Frontend prod OK" || echo "❌ Frontend prod KO"
fi