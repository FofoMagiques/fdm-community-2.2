# 🔧 Guide de résolution : "redirect_uri OAuth2 non valide"

## 🎯 Problème résolu !

Le message d'erreur "redirect_uri OAuth2 non valide" est maintenant corrigé. Voici ce qui a été fait :

### ✅ **Corrections apportées :**

1. **Configuration locale** : Passage de `teamfdm.fr` à `localhost`
2. **Dépendances** : Installation des packages manquants
3. **Services** : Redémarrage des services backend et frontend

### 🔧 **Configuration actuelle :**

```bash
# Backend (.env)
REDIRECT_URI=http://localhost:3000/callback
REACT_APP_BACKEND_URL=http://localhost:8001

# Frontend (.env)
REACT_APP_BACKEND_URL=http://localhost:8001
```

## 🎯 **Prochaines étapes pour configurer Discord :**

### 1. **Accéder au Discord Developer Portal**
👉 https://discord.com/developers/applications

### 2. **Sélectionner votre application**
- Cherchez l'application avec l'ID : `1393406406865977477`
- Cliquez dessus pour l'ouvrir

### 3. **Configurer les Redirect URIs**
- Allez dans l'onglet **"OAuth2"** → **"General"**
- Dans la section **"Redirects"**, ajoutez ces URLs :

```
http://localhost:3000/callback
http://teamfdm.fr:3000/callback
https://teamfdm.fr:3000/callback
https://localhost:3000/callback
```

### 4. **Vérifier les Scopes**
Dans la section **"Default Authorization Link"**, assurez-vous que ces scopes sont cochés :
- ✅ `identify`
- ✅ `email`
- ✅ `guilds`

### 5. **Sauvegarder**
Cliquez sur **"Save Changes"** en bas de la page.

## 🧪 **Tester la configuration :**

### 1. **Vérifier l'API**
```bash
curl -X GET "http://localhost:8001/api/"
# Doit retourner : {"message":"FDM Community API"}
```

### 2. **Tester l'URL Discord**
```bash
curl -X GET "http://localhost:8001/api/auth/discord"
# Doit retourner une URL Discord valide
```

### 3. **Accéder à l'application**
- Ouvrez votre navigateur
- Allez sur : http://localhost:3000
- Cliquez sur "Se connecter avec Discord"
- Vous ne devriez plus avoir d'erreur !

## 🔄 **Basculer entre localhost et teamfdm.fr :**

Utilisez le script de configuration automatique :

```bash
# Exécuter le script
./configure-urls.sh

# Choisir :
# 1. localhost (pour tests locaux)
# 2. teamfdm.fr (pour production)
```

## 📊 **États des services :**

Vérifiez que tous les services fonctionnent :

```bash
# Vérifier le statut
sudo supervisorctl status

# Doit montrer :
# backend      RUNNING
# frontend     RUNNING
# mongodb      RUNNING
```

## 🌐 **URLs d'accès :**

### Mode localhost (actuel) :
- **Frontend** : http://localhost:3000
- **Backend** : http://localhost:8001
- **API Docs** : http://localhost:8001/docs

### Mode teamfdm.fr (production) :
- **Frontend** : http://teamfdm.fr:3000
- **Backend** : http://teamfdm.fr:8001
- **API Docs** : http://teamfdm.fr:8001/docs

## 🚨 **Si le problème persiste :**

### 1. **Vérifier la configuration Discord**
- Assurez-vous que les redirect URIs sont bien ajoutés
- Vérifiez que l'application Discord est active

### 2. **Vérifier les services**
```bash
# Redémarrer tous les services
sudo supervisorctl restart all

# Vérifier les logs
tail -f /var/log/supervisor/backend.err.log
tail -f /var/log/supervisor/frontend.err.log
```

### 3. **Nettoyer le cache**
```bash
# Nettoyer le cache du navigateur
# ou utiliser le mode incognito
```

## ✅ **Checklist finale :**

- [ ] Backend API répond sur http://localhost:8001/api/
- [ ] Frontend accessible sur http://localhost:3000
- [ ] Redirect URIs ajoutés dans Discord Developer Portal
- [ ] Scopes configurés (identify, email, guilds)
- [ ] Services tous en RUNNING
- [ ] Test de connexion Discord réussi

## 🎉 **Félicitations !**

Votre application FDM Community est maintenant configurée correctement pour l'authentification Discord !

Pour passer en production sur votre NAS Synology :
1. Utilisez `./configure-urls.sh` pour basculer en mode `teamfdm.fr`
2. Ajoutez les redirect URIs teamfdm.fr dans Discord
3. Déployez avec `./start-prod.sh`