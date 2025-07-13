#!/bin/bash

# Script de test de la configuration Docker
# À utiliser sur votre NAS Synology

echo "🧪 Test de la configuration Docker FDM Community"
echo "================================================"

# Obtenir le répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher un message d'erreur
error() {
    echo -e "${RED}❌ $1${NC}"
}

# Fonction pour afficher un message de succès
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Fonction pour afficher un message d'information
info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Test 1: Vérifier Docker
echo "1. Vérification de Docker..."
if command -v docker &> /dev/null; then
    success "Docker est installé"
    docker --version
else
    error "Docker n'est pas installé"
    echo "   Installez Docker sur votre NAS Synology"
    exit 1
fi

# Test 2: Vérifier Docker Compose
echo ""
echo "2. Vérification de Docker Compose..."
if command -v docker-compose &> /dev/null; then
    success "Docker Compose est installé"
    docker-compose --version
else
    error "Docker Compose n'est pas installé"
    echo "   Installez Docker Compose sur votre NAS Synology"
    exit 1
fi

# Test 3: Vérifier les fichiers de configuration
echo ""
echo "3. Vérification des fichiers de configuration..."

# Vérifier docker-compose.yml
if [ -f "docker-compose.yml" ]; then
    success "docker-compose.yml trouvé"
    
    # Valider la syntaxe
    if docker-compose config > /dev/null 2>&1; then
        success "docker-compose.yml syntaxe OK"
    else
        error "docker-compose.yml syntaxe invalide"
        docker-compose config
    fi
else
    error "docker-compose.yml manquant"
fi

# Vérifier docker-compose.production.yml
if [ -f "docker-compose.production.yml" ]; then
    success "docker-compose.production.yml trouvé"
    
    # Valider la syntaxe
    if docker-compose -f docker-compose.production.yml config > /dev/null 2>&1; then
        success "docker-compose.production.yml syntaxe OK"
    else
        error "docker-compose.production.yml syntaxe invalide"
        docker-compose -f docker-compose.production.yml config
    fi
else
    error "docker-compose.production.yml manquant"
fi

# Test 4: Vérifier les fichiers .env
echo ""
echo "4. Vérification des fichiers .env..."

if [ -f "backend/.env" ]; then
    success "backend/.env trouvé"
    
    # Vérifier les variables importantes
    if grep -q "CLIENT_ID" backend/.env; then
        success "CLIENT_ID défini"
    else
        error "CLIENT_ID manquant dans backend/.env"
    fi
    
    if grep -q "CLIENT_SECRET" backend/.env; then
        success "CLIENT_SECRET défini"
    else
        error "CLIENT_SECRET manquant dans backend/.env"
    fi
    
    if grep -q "DISCORD_BOT_TOKEN" backend/.env; then
        success "DISCORD_BOT_TOKEN défini"
    else
        error "DISCORD_BOT_TOKEN manquant dans backend/.env"
    fi
    
else
    error "backend/.env manquant"
fi

if [ -f "frontend/.env" ]; then
    success "frontend/.env trouvé"
    
    if grep -q "REACT_APP_BACKEND_URL" frontend/.env; then
        success "REACT_APP_BACKEND_URL défini"
    else
        error "REACT_APP_BACKEND_URL manquant dans frontend/.env"
    fi
else
    error "frontend/.env manquant"
fi

# Test 5: Vérifier les Dockerfiles
echo ""
echo "5. Vérification des Dockerfiles..."

if [ -f "backend/Dockerfile" ]; then
    success "backend/Dockerfile trouvé"
else
    error "backend/Dockerfile manquant"
fi

if [ -f "frontend/Dockerfile" ]; then
    success "frontend/Dockerfile trouvé"
else
    error "frontend/Dockerfile manquant"
fi

# Test 6: Vérifier les scripts
echo ""
echo "6. Vérification des scripts..."

for script in "start.sh" "stop.sh" "start-prod.sh" "logs.sh"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            success "$script trouvé et exécutable"
        else
            error "$script trouvé mais pas exécutable"
            echo "   Exécutez: chmod +x $script"
        fi
    else
        error "$script manquant"
    fi
done

# Test 7: Test de construction (sans démarrage)
echo ""
echo "7. Test de construction des images..."

info "Test de construction du backend..."
if docker-compose build backend > /dev/null 2>&1; then
    success "Image backend construite avec succès"
else
    error "Erreur lors de la construction de l'image backend"
    echo "   Détails:"
    docker-compose build backend
fi

info "Test de construction du frontend..."
if docker-compose build frontend > /dev/null 2>&1; then
    success "Image frontend construite avec succès"
else
    error "Erreur lors de la construction de l'image frontend"
    echo "   Détails:"
    docker-compose build frontend
fi

# Résumé
echo ""
echo "📊 Résumé des tests"
echo "=================="

if [ $? -eq 0 ]; then
    success "Tous les tests sont passés ! 🎉"
    echo ""
    echo "🚀 Pour démarrer l'application:"
    echo "   ./start.sh        # Mode développement"
    echo "   ./start-prod.sh   # Mode production"
    echo ""
    echo "📝 Pour voir les logs:"
    echo "   ./logs.sh -f      # Logs en temps réel"
    echo ""
    echo "🛑 Pour arrêter:"
    echo "   ./stop.sh         # Arrêt normal"
else
    error "Certains tests ont échoué"
    echo ""
    echo "🔧 Corrigez les erreurs ci-dessus avant de continuer"
fi