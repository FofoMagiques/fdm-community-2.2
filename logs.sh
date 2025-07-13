#!/bin/bash

# Script pour voir les logs des conteneurs
# À utiliser sur votre NAS Synology

echo "📝 Logs FDM Community"
echo "===================="

# Obtenir le répertoire du script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Fonction pour afficher l'aide
show_help() {
    echo "Usage: $0 [OPTIONS] [SERVICE]"
    echo ""
    echo "OPTIONS:"
    echo "  -f, --follow     Suivre les logs en temps réel"
    echo "  -p, --prod       Utiliser la configuration production"
    echo "  -h, --help       Afficher cette aide"
    echo ""
    echo "SERVICE (optionnel):"
    echo "  backend          Logs du backend seulement"
    echo "  frontend         Logs du frontend seulement"
    echo "  mongodb          Logs de MongoDB seulement"
    echo ""
    echo "Exemples:"
    echo "  $0                    # Tous les logs"
    echo "  $0 -f                 # Tous les logs en temps réel"
    echo "  $0 -f backend         # Logs backend en temps réel"
    echo "  $0 -p -f              # Logs production en temps réel"
}

# Variables par défaut
FOLLOW=""
COMPOSE_FILE="docker-compose.yml"
SERVICE=""

# Traitement des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--follow)
            FOLLOW="-f"
            shift
            ;;
        -p|--prod)
            COMPOSE_FILE="docker-compose.production.yml"
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        backend|frontend|mongodb)
            SERVICE="$1"
            shift
            ;;
        *)
            echo "Option inconnue: $1"
            show_help
            exit 1
            ;;
    esac
done

# Commande Docker Compose
if [ -n "$SERVICE" ]; then
    echo "📊 Logs du service: $SERVICE"
    docker-compose -f "$COMPOSE_FILE" logs $FOLLOW "$SERVICE"
else
    echo "📊 Logs de tous les services"
    docker-compose -f "$COMPOSE_FILE" logs $FOLLOW
fi