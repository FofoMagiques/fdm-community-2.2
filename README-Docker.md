# FDM Community - Configuration Docker

## 🚀 Démarrage rapide

### Développement
```bash
# Démarrer tous les services
./start.sh

# Voir les logs
./logs.sh -f

# Arrêter les services
./stop.sh
```

### Production
```bash
# Démarrer en mode production
./start-prod.sh

# Voir les logs production
./logs.sh -p -f

# Arrêter les services production
docker-compose -f docker-compose.production.yml down
```

## 📁 Structure des fichiers

```
/app/
├── docker-compose.yml           # Configuration développement
├── docker-compose.production.yml # Configuration production
├── .env                        # Variables d'environnement globales
├── start.sh                    # Script démarrage développement
├── start-prod.sh               # Script démarrage production
├── stop.sh                     # Script arrêt
├── logs.sh                     # Script pour voir les logs
├── backend/
│   ├── Dockerfile
│   ├── .env                    # Variables backend
│   └── server.py
├── frontend/
│   ├── Dockerfile
│   ├── .env                    # Variables frontend
│   └── src/
└── README-Docker.md            # Ce fichier
```

## 🔧 Configuration

### Variables d'environnement

#### Backend (.env)
- `CLIENT_ID` : ID client Discord
- `CLIENT_SECRET` : Secret client Discord
- `REDIRECT_URI` : URI de redirection OAuth
- `SESSION_SECRET` : Secret pour les sessions
- `MONGO_URL` : URL MongoDB
- `DB_NAME` : Nom de la base de données
- `DISCORD_GUILD_ID` : ID du serveur Discord
- `DISCORD_BOT_TOKEN` : Token du bot Discord

#### Frontend (.env)
- `REACT_APP_BACKEND_URL` : URL du backend

### Ports utilisés
- **3000** : Frontend React
- **8001** : Backend FastAPI
- **27017** : MongoDB

## 🐳 Commandes Docker utiles

### Gestion des conteneurs
```bash
# Voir les conteneurs en cours
docker-compose ps

# Redémarrer un service
docker-compose restart backend

# Rebuild un service
docker-compose build backend
docker-compose up -d backend

# Voir les logs d'un service
docker-compose logs -f backend
```

### Gestion des volumes
```bash
# Voir les volumes
docker volume ls

# Supprimer le volume MongoDB (⚠️ perte de données)
docker volume rm fdm_mongodb_data
```

### Nettoyage
```bash
# Nettoyer les images inutilisées
docker system prune -f

# Supprimer tous les conteneurs et volumes
docker-compose down -v
```

## 🔍 Dépannage

### Problème : Conteneur qui ne démarre pas
```bash
# Voir les logs détaillés
docker-compose logs service_name

# Vérifier la configuration
docker-compose config
```

### Problème : Base de données MongoDB
```bash
# Accéder à MongoDB
docker-compose exec mongodb mongo

# Vérifier les données
docker-compose exec mongodb mongo fdm_community --eval "db.users.find()"
```

### Problème : Permissions
```bash
# Donner les permissions d'exécution aux scripts
chmod +x start.sh stop.sh start-prod.sh logs.sh
```

## 📊 Monitoring

### Vérifier l'état des services
```bash
# Status des conteneurs
docker-compose ps

# Utilisation des ressources
docker stats

# Logs en temps réel
./logs.sh -f
```

### Tests de connectivité
```bash
# Test backend
curl http://localhost:8001/api/

# Test frontend
curl -I http://localhost:3000

# Test MongoDB
docker-compose exec mongodb mongo --eval "db.runCommand('ping')"
```

## 🚨 Sécurité

### Fichiers à protéger
- `backend/.env` : Contient les secrets Discord
- `frontend/.env` : Variables d'environnement React

### Bonnes pratiques
1. Ne jamais commiter les fichiers `.env`
2. Utiliser des secrets forts
3. Régénérer les tokens périodiquement
4. Limiter l'accès aux fichiers de configuration

## 🆘 Support

En cas de problème :
1. Vérifier les logs avec `./logs.sh -f`
2. Vérifier la configuration avec `docker-compose config`
3. Redémarrer les services avec `./start.sh`
4. Vérifier l'état avec `docker-compose ps`