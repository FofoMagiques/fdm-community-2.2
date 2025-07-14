#!/bin/bash

# Script de configuration HTTPS pour FDM Community
# Configure SSL/TLS avec Let's Encrypt ou certificat existant

echo "🔒 Configuration HTTPS pour FDM Community"
echo "=========================================="

# Obtenir le répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions d'affichage
error() { echo -e "${RED}❌ $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

# Fonction pour configurer HTTPS avec reverse proxy Synology
configure_synology_https() {
    echo ""
    info "Configuration via Synology Reverse Proxy"
    echo ""
    echo "1. Accédez au Panneau de contrôle Synology"
    echo "2. Allez dans Sécurité → Certificat"
    echo "3. Ajoutez un certificat Let's Encrypt pour teamfdm.fr"
    echo "4. Allez dans Serveur d'applications → Reverse Proxy"
    echo "5. Créez ces règles :"
    echo ""
    echo "   Règle 1 - Frontend :"
    echo "   Source: HTTPS teamfdm.fr:443"
    echo "   Destination: HTTP localhost:3000"
    echo ""
    echo "   Règle 2 - API Backend :"
    echo "   Source: HTTPS teamfdm.fr:443 /api/*"
    echo "   Destination: HTTP localhost:8001 /api/*"
    echo ""
    echo "6. Activez les règles"
    echo ""
    success "Configuration terminée ! Votre site sera accessible via https://teamfdm.fr"
}

# Fonction pour configurer HTTPS avec Docker + Nginx
configure_docker_https() {
    echo ""
    info "Configuration via Docker + Nginx"
    echo ""
    
    # Vérifier si les certificats existent
    if [ -d "/usr/syno/etc/certificate/_archive/system/default" ]; then
        success "Certificats Synology trouvés"
    else
        error "Certificats Synology non trouvés"
        echo "Générez d'abord un certificat SSL dans le panneau Synology"
        return 1
    fi
    
    # Copier les fichiers de configuration HTTPS
    info "Copie des configurations HTTPS..."
    cp backend/.env.https backend/.env
    cp frontend/.env.https frontend/.env
    
    # Arrêter les services actuels
    info "Arrêt des services actuels..."
    docker-compose -f docker-compose.production.yml down 2>/dev/null || true
    
    # Démarrer avec la configuration HTTPS
    info "Démarrage avec HTTPS..."
    docker-compose -f docker-compose.https.yml up -d --build
    
    # Attendre le démarrage
    info "Attente du démarrage (30 secondes)..."
    sleep 30
    
    # Vérifier les services
    echo ""
    info "État des services :"
    docker-compose -f docker-compose.https.yml ps
    
    echo ""
    success "Configuration Docker HTTPS terminée !"
    echo "🌐 Site accessible via : https://teamfdm.fr"
}

# Fonction pour tester la configuration HTTPS
test_https_config() {
    echo ""
    info "Test de la configuration HTTPS..."
    
    # Test de connectivité
    echo "Test de redirection HTTP → HTTPS :"
    curl -I -s http://teamfdm.fr | grep -i location || echo "Pas de redirection configurée"
    
    echo ""
    echo "Test HTTPS :"
    curl -I -s https://teamfdm.fr && success "HTTPS fonctionne" || error "HTTPS ne fonctionne pas"
    
    echo ""
    echo "Test API HTTPS :"
    curl -s https://teamfdm.fr/api/ && success "API HTTPS fonctionne" || error "API HTTPS ne fonctionne pas"
}

# Fonction pour mettre à jour Discord
update_discord_config() {
    echo ""
    info "Mise à jour de la configuration Discord"
    echo ""
    echo "1. Allez sur https://discord.com/developers/applications"
    echo "2. Sélectionnez votre application FDM"
    echo "3. Onglet OAuth2 → General"
    echo "4. Mettez à jour les Redirect URIs :"
    echo ""
    echo "   Ajoutez : https://teamfdm.fr/callback"
    echo "   Gardez aussi : http://teamfdm.fr:3000/callback (pour les tests)"
    echo ""
    echo "5. Sauvegardez les modifications"
    echo ""
    success "N'oubliez pas de mettre à jour Discord !"
}

# Menu principal
echo ""
echo "Choisissez votre méthode de configuration HTTPS :"
echo ""
echo "1. 🔧 Synology Reverse Proxy (Recommandé - Plus simple)"
echo "2. 🐳 Docker + Nginx (Avancé - Plus de contrôle)"
echo "3. 🧪 Tester la configuration HTTPS actuelle"
echo "4. 📝 Instructions pour Discord"
echo "5. 📋 Afficher les URLs actuelles"
echo ""
read -p "Votre choix (1-5) : " choice

case $choice in
    1)
        configure_synology_https
        update_discord_config
        ;;
    2)
        configure_docker_https
        update_discord_config
        ;;
    3)
        test_https_config
        ;;
    4)
        update_discord_config
        ;;
    5)
        echo ""
        info "URLs actuelles :"
        echo "Frontend: $(grep REACT_APP_BACKEND_URL frontend/.env)"
        echo "Backend: $(grep REDIRECT_URI backend/.env)"
        ;;
    *)
        error "Choix invalide"
        exit 1
        ;;
esac

echo ""
info "Configuration terminée !"
echo ""
echo "🔗 URLs après configuration :"
echo "• Site web : https://teamfdm.fr"
echo "• API : https://teamfdm.fr/api/"
echo "• Documentation : https://teamfdm.fr/api/docs"
echo ""
echo "📝 N'oubliez pas de :"
echo "• Mettre à jour Discord (redirect URIs)"
echo "• Tester la connexion OAuth"
echo "• Vérifier les certificats SSL"