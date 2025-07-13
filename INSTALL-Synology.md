# Guide d'installation Docker sur NAS Synology

## 🎯 Prérequis

### 1. Modèles compatibles
Votre NAS Synology doit être compatible avec Docker. Voici les modèles supportés :

**Séries compatibles :**
- DS718+, DS918+, DS1019+, DS1618+, DS1819+
- DS920+, DS1520+, DS1621+, DS1821+
- RS818+, RS1219+, RS1619xs+, RS2419+
- DS723+, DS923+, DS1522+, DS1821+

### 2. Système d'exploitation
- DSM 7.0 ou supérieur

## 🛠️ Installation Docker sur Synology

### Méthode 1 : Via le Package Center (Recommandée)
1. Ouvrez le **Package Center** sur votre NAS
2. Recherchez **"Docker"**
3. Cliquez sur **"Installer"**
4. Attendez la fin de l'installation

### Méthode 2 : Via SSH (Avancée)
```bash
# Se connecter en SSH à votre NAS
ssh admin@teamfdm.fr

# Installer Docker manuellement (si nécessaire)
sudo synopackage --install Docker
```

## 🔧 Configuration initiale

### 1. Vérifier l'installation
```bash
# Se connecter en SSH
ssh admin@teamfdm.fr

# Vérifier Docker
docker --version

# Vérifier Docker Compose
docker-compose --version
```

### 2. Permissions utilisateur
```bash
# Ajouter votre utilisateur au groupe docker
sudo synogroup --add docker admin

# Redémarrer la session SSH
exit
# Reconnectez-vous
```

## 📁 Déploiement FDM Community

### 1. Transférer les fichiers
Copiez tous les fichiers du projet dans `/volume1/web/FDM/` sur votre NAS.

### 2. Définir les permissions
```bash
# Aller dans le dossier du projet
cd /volume1/web/FDM

# Rendre les scripts exécutables
chmod +x start.sh stop.sh start-prod.sh logs.sh test-docker.sh
```

### 3. Tester la configuration
```bash
# Exécuter le script de test
./test-docker.sh
```

### 4. Démarrer l'application
```bash
# Mode développement
./start.sh

# OU mode production
./start-prod.sh
```

## 🌐 Configuration réseau

### 1. Ports à ouvrir
Dans le panneau de contrôle Synology :
- **3000** : Frontend React
- **8001** : Backend FastAPI
- **27017** : MongoDB

### 2. Configuration DNS
Si vous utilisez un nom de domaine personnalisé :
1. Panneau de contrôle → **Connectivité externe** → **DDNS**
2. Ajoutez votre domaine `teamfdm.fr`

## 🔒 Sécurité

### 1. Firewall
```bash
# Configurer le firewall (optionnel)
sudo synofw --enable
sudo synofw --rule add --port 3000 --protocol tcp --action allow
sudo synofw --rule add --port 8001 --protocol tcp --action allow
```

### 2. Certificats SSL
1. Panneau de contrôle → **Sécurité** → **Certificat**
2. Ajoutez un certificat SSL pour `teamfdm.fr`

## 📊 Monitoring

### 1. Logs des conteneurs
```bash
# Voir tous les logs
./logs.sh -f

# Logs d'un service spécifique
./logs.sh -f backend
```

### 2. Utilisation des ressources
```bash
# Statistiques en temps réel
docker stats

# Espace disque
docker system df
```

## 🚨 Dépannage

### Problème : Docker non trouvé
```bash
# Vérifier si Docker est démarré
sudo systemctl status docker

# Démarrer Docker si nécessaire
sudo systemctl start docker
```

### Problème : Permissions
```bash
# Vérifier les permissions
ls -la /var/run/docker.sock

# Corriger les permissions
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock
```

### Problème : Espace disque
```bash
# Nettoyer Docker
docker system prune -a

# Voir l'utilisation
docker system df
```

## 🔄 Mise à jour

### 1. Mise à jour de l'application
```bash
# Arrêter l'application
./stop.sh

# Mettre à jour le code
# (copier les nouveaux fichiers)

# Redémarrer
./start.sh
```

### 2. Mise à jour Docker
Via le Package Center → Docker → Mettre à jour

## 📞 Support

En cas de problème :
1. Vérifiez les logs : `./logs.sh -f`
2. Testez la configuration : `./test-docker.sh`
3. Consultez les logs Synology : `/var/log/`

## 📋 Checklist finale

- [ ] Docker installé et fonctionnel
- [ ] Fichiers copiés dans `/volume1/web/FDM/`
- [ ] Scripts exécutables (`chmod +x`)
- [ ] Test de configuration réussi (`./test-docker.sh`)
- [ ] Ports ouverts (3000, 8001, 27017)
- [ ] DNS configuré pour `teamfdm.fr`
- [ ] Application démarrée (`./start.sh`)
- [ ] Services accessibles via navigateur

🎉 **Votre application FDM Community est maintenant prête !**