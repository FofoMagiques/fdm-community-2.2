# FDM Community 🚀

Une application web communautaire moderne avec authentification Discord, développée pour la communauté FDM.

![FDM Community](https://img.shields.io/badge/FDM-Community-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![React](https://img.shields.io/badge/React-19.0+-blue.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-5.0+-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)

## 📋 Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [API Endpoints](#api-endpoints)
- [Déploiement](#déploiement)
- [Développement](#développement)
- [Contribution](#contribution)
- [Support](#support)

## 🌟 Aperçu

FDM Community est une application web full-stack qui permet aux membres du serveur Discord FDM de se connecter via OAuth Discord et d'accéder à un tableau de bord communautaire avec des statistiques du serveur et des fonctionnalités de gestion d'utilisateurs.

### Captures d'écran

*Screenshots à venir...*

## ✨ Fonctionnalités

### 🔐 Authentification
- **OAuth Discord** : Connexion sécurisée via Discord
- **Vérification serveur** : Seuls les membres du serveur Discord FDM peuvent se connecter
- **Gestion des sessions** : Sessions sécurisées avec JWT
- **Rôles administrateurs** : Accès privilégié pour les administrateurs

### 📊 Tableau de bord
- **Statistiques du serveur** : Nombre de membres, statut en ligne, boosts
- **Informations utilisateur** : Profil Discord, historique de connexion
- **Dashboard admin** : Gestion des utilisateurs, statistiques détaillées

### 🛡️ Sécurité
- **Tokens JWT** : Authentification sécurisée
- **CORS configuré** : Protection cross-origin
- **Variables d'environnement** : Configuration sécurisée
- **Validation des données** : Vérification avec Pydantic

## 🛠️ Technologies

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderne et performant
- **[MongoDB](https://www.mongodb.com/)** - Base de données NoSQL
- **[Motor](https://motor.readthedocs.io/)** - Driver MongoDB asynchrone
- **[PyJWT](https://pyjwt.readthedocs.io/)** - Gestion des tokens JWT
- **[HTTPX](https://www.python-httpx.org/)** - Client HTTP asynchrone
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Validation des données

### Frontend
- **[React](https://reactjs.org/)** - Bibliothèque UI moderne
- **[Axios](https://axios-http.com/)** - Client HTTP pour les API
- **[React Router](https://reactrouter.com/)** - Navigation côté client
- **[Tailwind CSS](https://tailwindcss.com/)** - Framework CSS utilitaire

### Infrastructure
- **[Docker](https://www.docker.com/)** - Conteneurisation
- **[Docker Compose](https://docs.docker.com/compose/)** - Orchestration multi-conteneurs
- **[Uvicorn](https://www.uvicorn.org/)** - Serveur ASGI

## 📦 Installation

### Prérequis
- **Python 3.9+**
- **Node.js 18+**
- **MongoDB 5.0+**
- **Docker** (optionnel)

### Installation manuelle

#### 1. Cloner le projet
```bash
git clone https://github.com/votre-username/fdm-community.git
cd fdm-community
```

#### 2. Configuration Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Éditer .env avec vos configurations
```

#### 3. Configuration Frontend
```bash
cd frontend
yarn install
cp .env.example .env
# Éditer .env avec vos configurations
```

#### 4. Démarrer MongoDB
```bash
# Avec Docker
docker run -d -p 27017:27017 --name mongodb mongo:5.0

# Ou installer MongoDB localement
```

#### 5. Lancer l'application
```bash
# Terminal 1 - Backend
cd backend
python server.py

# Terminal 2 - Frontend
cd frontend
yarn start
```

### Installation avec Docker 🐳

#### 1. Prérequis Docker
```bash
# Installer Docker et Docker Compose
# Voir INSTALL-Synology.md pour NAS Synology
```

#### 2. Configuration
```bash
# Vérifier les fichiers .env
ls backend/.env frontend/.env

# Tester la configuration
./test-docker.sh
```

#### 3. Démarrage
```bash
# Mode développement
./start.sh

# Mode production
./start-prod.sh
```

## ⚙️ Configuration

### Variables d'environnement

#### Backend (`backend/.env`)
```env
# Discord OAuth
CLIENT_ID=your_discord_client_id
CLIENT_SECRET=your_discord_client_secret
REDIRECT_URI=http://localhost:3000/callback

# Application
SESSION_SECRET=your_session_secret
DB_NAME=fdm_community

# Database
MONGO_URL=mongodb://localhost:27017

# Discord Bot
DISCORD_GUILD_ID=your_guild_id
DISCORD_BOT_TOKEN=your_bot_token
```

#### Frontend (`frontend/.env`)
```env
# API Configuration
REACT_APP_BACKEND_URL=http://localhost:8001
```

### Configuration Discord

#### 1. Créer une application Discord
1. Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
2. Créez une nouvelle application
3. Notez le `Client ID` et `Client Secret`

#### 2. Configurer OAuth2
- **Redirect URI** : `http://localhost:3000/callback`
- **Scopes** : `identify`, `email`, `guilds`

#### 3. Créer un bot Discord
1. Dans votre application Discord, onglet "Bot"
2. Créez un bot et notez le token
3. Invitez le bot sur votre serveur

## 🚀 Utilisation

### Accès à l'application
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8001/api/
- **Documentation API** : http://localhost:8001/docs

### Workflow utilisateur
1. **Connexion** : Cliquez sur "Se connecter avec Discord"
2. **Autorisation** : Autorisez l'application Discord
3. **Vérification** : L'application vérifie votre appartenance au serveur
4. **Tableau de bord** : Accédez aux fonctionnalités

### Fonctionnalités administrateur
- Accès au dashboard admin
- Gestion des utilisateurs
- Statistiques détaillées du serveur
- Suppression d'utilisateurs

## 🔌 API Endpoints

### Authentification
```bash
GET  /api/auth/discord      # Initier OAuth Discord
GET  /api/auth/callback     # Callback OAuth
GET  /api/auth/me          # Informations utilisateur actuel
POST /api/auth/logout      # Déconnexion
```

### Utilisateurs
```bash
GET    /api/users          # Liste des utilisateurs (admin)
GET    /api/users/{id}     # Détails utilisateur
DELETE /api/users/{id}     # Supprimer utilisateur (admin)
```

### Statistiques
```bash
GET /api/stats             # Statistiques du serveur Discord
GET /api/admin/dashboard   # Dashboard admin
```

### Exemple d'utilisation
```bash
# Tester l'API
curl -X GET "http://localhost:8001/api/"

# Obtenir les statistiques
curl -X GET "http://localhost:8001/api/stats"

# Connexion Discord
curl -X GET "http://localhost:8001/api/auth/discord"
```

## 🚢 Déploiement

### Déploiement Docker

#### Sur serveur local
```bash
# Cloner le projet
git clone https://github.com/votre-username/fdm-community.git
cd fdm-community

# Configuration
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
# Éditer les fichiers .env

# Démarrer
./start-prod.sh
```

#### Sur NAS Synology
Voir le guide détaillé : [INSTALL-Synology.md](INSTALL-Synology.md)

### Déploiement manuel

#### Configuration de production
```bash
# Variables d'environnement production
export NODE_ENV=production
export MONGO_URL=mongodb://your-production-db:27017

# Build frontend
cd frontend
yarn build

# Démarrer backend
cd backend
uvicorn server:app --host 0.0.0.0 --port 8001
```

### Nginx (optionnel)
```nginx
server {
    listen 80;
    server_name teamfdm.fr;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8001/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 💻 Développement

### Structure du projet
```
fdm-community/
├── backend/                 # API FastAPI
│   ├── server.py           # Application principale
│   ├── requirements.txt    # Dépendances Python
│   ├── Dockerfile         # Image Docker backend
│   └── .env               # Variables d'environnement
├── frontend/               # Application React
│   ├── src/               # Code source
│   ├── public/            # Assets statiques
│   ├── package.json       # Dépendances Node.js
│   ├── Dockerfile         # Image Docker frontend
│   └── .env               # Variables d'environnement
├── docker-compose.yml      # Configuration Docker dev
├── docker-compose.production.yml  # Configuration Docker prod
├── start.sh               # Script de démarrage
├── stop.sh                # Script d'arrêt
├── logs.sh                # Script de logs
├── test-docker.sh         # Tests Docker
└── README.md              # Ce fichier
```

### Scripts disponibles

#### Backend
```bash
cd backend
python server.py          # Démarrer le serveur
pip install -r requirements.txt  # Installer dépendances
```

#### Frontend
```bash
cd frontend
yarn start                 # Démarrer en mode développement
yarn build                 # Build pour production
yarn test                  # Lancer les tests
```

#### Docker
```bash
./start.sh                 # Démarrer tous les services
./stop.sh                  # Arrêter tous les services
./logs.sh -f               # Voir les logs en temps réel
./test-docker.sh           # Tester la configuration
```

### Développement avec hot-reload
```bash
# Démarrer avec Docker (hot-reload activé)
./start.sh

# Les modifications seront automatiquement rechargées
```

## 🤝 Contribution

### Comment contribuer
1. **Fork** le projet
2. **Créer** une branche (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos modifications (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### Standards de code
- **Python** : PEP 8, type hints
- **JavaScript** : ESLint, Prettier
- **Commits** : Messages descriptifs
- **Tests** : Ajouter des tests pour les nouvelles fonctionnalités

### Signaler des bugs
Utilisez les [GitHub Issues](https://github.com/votre-username/fdm-community/issues) pour signaler des bugs ou demander des fonctionnalités.

## 📞 Support

### Documentation
- **[README-Docker.md](README-Docker.md)** - Guide Docker détaillé
- **[INSTALL-Synology.md](INSTALL-Synology.md)** - Installation sur NAS Synology
- **API Docs** - http://localhost:8001/docs

### Aide
- **Issues GitHub** : [Signaler un problème](https://github.com/votre-username/fdm-community/issues)
- **Discord** : Rejoignez le serveur FDM
- **Email** : contact@teamfdm.fr

### Logs et debugging
```bash
# Logs Docker
./logs.sh -f

# Logs spécifiques
./logs.sh -f backend
./logs.sh -f frontend

# Debug mode
export DEBUG=true
python backend/server.py
```

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **Discord** pour leur API OAuth2
- **FastAPI** pour le framework backend
- **React** pour le framework frontend
- **MongoDB** pour la base de données
- **Communauté FDM** pour les retours et tests

---

<div align="center">
  <strong>Développé avec ❤️ pour la communauté FDM</strong>
</div>

<div align="center">
  <a href="http://teamfdm.fr">🌐 Site web</a> •
  <a href="https://discord.gg/fdm">💬 Discord</a> •
  <a href="mailto:contact@teamfdm.fr">📧 Contact</a>
</div>