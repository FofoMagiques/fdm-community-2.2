#!/bin/bash

# Script de configuration des URLs pour FDM Community
# Permet de basculer entre localhost et teamfdm.fr

echo "🔧 Configuration des URLs FDM Community"
echo "======================================="

# Fonction pour configurer localhost
configure_localhost() {
    echo "📍 Configuration pour localhost..."
    
    # Backend
    sed -i 's|REDIRECT_URI=.*|REDIRECT_URI=http://localhost:3000/callback|' backend/.env
    sed -i 's|MONGO_URL=.*|MONGO_URL=mongodb://mongodb:27017|' backend/.env
    
    # Frontend
    sed -i 's|REACT_APP_BACKEND_URL=.*|REACT_APP_BACKEND_URL=http://localhost:8001|' frontend/.env
    
    echo "✅ Configuration localhost terminée"
    echo "🌐 Frontend : http://localhost:3000"
    echo "🔧 Backend : http://localhost:8001"
}

# Fonction pour configurer teamfdm.fr
configure_teamfdm() {
    echo "📍 Configuration pour teamfdm.fr..."
    
    # Backend
    sed -i 's|REDIRECT_URI=.*|REDIRECT_URI=http://teamfdm.fr:3000/callback|' backend/.env
    sed -i 's|MONGO_URL=.*|MONGO_URL=mongodb://mongodb:27017|' backend/.env
    
    # Frontend
    sed -i 's|REACT_APP_BACKEND_URL=.*|REACT_APP_BACKEND_URL=http://teamfdm.fr:8001|' frontend/.env
    
    echo "✅ Configuration teamfdm.fr terminée"
    echo "🌐 Frontend : http://teamfdm.fr:3000"
    echo "🔧 Backend : http://teamfdm.fr:8001"
}

# Menu de sélection
echo "Choisissez votre configuration :"
echo "1. localhost (pour tests locaux)"
echo "2. teamfdm.fr (pour production)"
echo "3. Afficher la configuration actuelle"
echo ""
read -p "Votre choix (1-3) : " choice

case $choice in
    1)
        configure_localhost
        ;;
    2)
        configure_teamfdm
        ;;
    3)
        echo "📊 Configuration actuelle :"
        echo "Backend REDIRECT_URI: $(grep REDIRECT_URI backend/.env)"
        echo "Frontend BACKEND_URL: $(grep REACT_APP_BACKEND_URL frontend/.env)"
        ;;
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
echo "🔄 Redémarrez les services pour appliquer les changements :"
echo "   docker-compose down && docker-compose up -d"
echo "   # ou"
echo "   ./stop.sh && ./start.sh"