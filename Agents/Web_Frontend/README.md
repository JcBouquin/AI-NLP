# 🌐 Frontend Web pour Agent Parlant

Interface web moderne pour interagir avec un agent Parlant équipé des tools **QNA** et **SQL**.

---

## 📋 Contenu

- `index.html` - Interface chatbot responsive
- `chat.js` - Logique JavaScript (appels API Parlant)
- `setup_agent.py` - Script de configuration de l'agent
- `README.md` - Ce fichier

---

## 🚀 Installation Rapide

### Prérequis

✅ Python 3.10+  
✅ Parlant installé (`pip install parlant`)  
✅ Modules QNA et SQL configurés  
✅ OpenAI API key dans `.env`

### Étape 1 : Créer l'Agent

```bash
# Depuis le dossier web_frontend/
python setup_agent.py
```

**Résultat :**
```
✅ AGENT CONFIGURÉ AVEC SUCCÈS !
   Agent ID: abc123-def456-ghi789
```

### Étape 2 : Mettre à Jour la Configuration

Copiez l'**Agent ID** affiché et mettez-le dans `chat.js` :

```javascript
const CONFIG = {
    PARLANT_API_URL: 'http://localhost:8000/api/v1',
    AGENT_ID: 'abc123-def456-ghi789', // ← Collez votre ID ici
    CUSTOMER_ID: 'customer-demo-123',
};
```

### Étape 3 : Charger les Données (si pas déjà fait)

```bash
# FAQ (depuis mon_agent_medical/)
cd ../../mon_agent_medical
load_medical_faq.bat

# Schémas SQL (depuis parlant-sql/)
cd ../parlant-sql
load_schemas.bat
python create_demo_database.py
```

### Étape 4 : Démarrer Parlant Server

```bash
# Terminal 1
parlant-server \
  --module parlant_qna.module \
  --module parlant_sql.module \
  --host 0.0.0.0 \
  --port 8000
```

### Étape 5 : Lancer le Frontend

```bash
# Terminal 2 (depuis web_frontend/)
python -m http.server 8080
```

### Étape 6 : Ouvrir le Navigateur

Allez sur : **http://localhost:8080**

---

## 🎯 Fonctionnalités

### ✅ Interface Moderne

- Design responsive (mobile + desktop)
- Bulles de chat animées
- Indicateur de frappe
- Avatars utilisateur/agent
- Timestamps des messages

### ✅ Actions Rapides

Boutons prédéfinis pour :
- 🕐 Horaires du cabinet
- 👨‍⚕️ Équipe médicale
- 📅 Mes rendez-vous
- ➕ Prendre RDV

### ✅ Indicateurs de Tools

Chaque réponse affiche le tool utilisé :
- 📚 **FAQ** : Réponse depuis `qna`
- 🗄️ **Base de données** : Réponse depuis `sql_query`

### ✅ Gestion d'Erreurs

- Détection de perte de connexion
- Messages d'erreur clairs
- Reconnexion automatique

---

## 🔧 Configuration Avancée

### Changer l'URL du Backend

Dans `chat.js` :

```javascript
const CONFIG = {
    PARLANT_API_URL: 'https://votre-serveur.com/api/v1',
    // ...
};
```

### Personnaliser les Actions Rapides

Dans `index.html`, section `.quick-actions` :

```html
<button class="quick-action-btn" data-message="Votre question">
    🔹 Libellé
</button>
```

### Ajouter des Tools Custom

Dans `chat.js`, fonction `getToolInfo()` :

```javascript
const tools = {
    'qna': { icon: '📚', label: 'Réponse FAQ' },
    'sql_query': { icon: '🗄️', label: 'Base de données' },
    'mon_nouveau_tool': { icon: '🔧', label: 'Mon Tool' }, // ← Ajoutez ici
};
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│ NAVIGATEUR (localhost:8080)             │
│                                          │
│  index.html + chat.js                   │
│  ↓ fetch() HTTP POST                    │
└──────────────┬──────────────────────────┘
               ↓
┌──────────────────────────────────────────┐
│ PARLANT SERVER (localhost:8000)          │
│                                           │
│  API REST: /api/v1/agents/.../messages  │
│  ↓                                        │
└──────────────┬───────────────────────────┘
               ↓
┌──────────────────────────────────────────┐
│ AGENT PARLANT                            │
│                                           │
│  Guidelines évalue la question           │
│  ↓                                        │
│  Condition 1: "infos cabinet"            │
│    → Tool: qna                           │
│  Condition 2: "données dynamiques"       │
│    → Tool: sql_query                     │
│  ↓                                        │
└──────────────┬───────────────────────────┘
               ↓
     ┌─────────┴──────────┐
     ↓                    ↓
┌─────────────┐    ┌──────────────────┐
│ parlant-qna │    │  parlant-sql     │
│             │    │                  │
│ FAQ (.json) │    │  SQLite (.db)    │
└─────────────┘    └──────────────────┘
```

---

## 🧪 Tester

### Test 1 : QNA (FAQ Statiques)

**Question :** "Quels sont vos horaires ?"

**Attendu :**
- Réponse rapide depuis la FAQ
- Badge : `📚 Réponse FAQ`

### Test 2 : SQL (Base Dynamique)

**Question :** "Combien de rendez-vous ai-je ce mois ?"

**Attendu :**
- Génération SQL automatique
- Résultat depuis la base
- Badge : `🗄️ Base de données`

### Test 3 : Journey

**Question :** "Je voudrais prendre rendez-vous"

**Attendu :**
- Activation du parcours de prise de RDV
- Questions guidées étape par étape

### Test 4 : Urgence

**Question :** "J'ai des douleurs thoraciques"

**Attendu :**
- Override immédiat
- Message d'urgence (appeler le 15)

---

## 🐛 Dépannage

### ❌ "Impossible de se connecter au serveur"

**Solution :**
```bash
# Vérifier que Parlant est démarré
curl http://localhost:8000/health

# Redémarrer Parlant
parlant-server --module parlant_qna.module --module parlant_sql.module
```

### ❌ "Agent non trouvé"

**Solution :**
1. Vérifiez l'Agent ID dans `chat.js`
2. Relancez `setup_agent.py` si nécessaire

### ❌ "Module not found: parlant_qna"

**Solution :**
```bash
# Installer les modules
pip install parlant-qna
pip install parlant-sql  # (votre module custom)

# OU charger localement
parlant-server --module /chemin/vers/parlant_qna/module.py
```

### ❌ CORS Error

**Solution :**

Si vous accédez depuis un domaine différent :

```bash
# Démarrer Parlant avec CORS activé
parlant-server --cors-origin "*"
```

---

## 🎨 Personnalisation du Style

### Changer les Couleurs

Dans `index.html`, section `<style>` :

```css
/* Couleur principale */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
/* Remplacez par vos couleurs */

/* Bulles utilisateur */
.message.user .message-bubble {
    background: linear-gradient(135deg, #votre-couleur-1, #votre-couleur-2);
}
```

### Changer les Émojis

```html
<!-- Avatar agent -->
<div class="message-avatar">🤖</div>  <!-- Changez ici -->

<!-- Avatar utilisateur -->
<div class="message-avatar">👤</div>  <!-- Changez ici -->
```

---

## 📱 Version Mobile

Le frontend est **100% responsive** :
- Layout adaptatif
- Bulles ajustées
- Boutons tactiles optimisés

Testez sur mobile en ouvrant :
```
http://votre-ip-locale:8080
```

---

## 🚢 Déploiement Production

### Option 1 : Serveur Nginx

```nginx
server {
    listen 80;
    server_name votre-domaine.com;
    
    location / {
        root /chemin/vers/web_frontend;
        index index.html;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

### Option 2 : Serveur Node.js

```javascript
const express = require('express');
const app = express();

app.use(express.static('web_frontend'));
app.listen(3000);
```

### Option 3 : Docker

```dockerfile
FROM nginx:alpine
COPY web_frontend/ /usr/share/nginx/html/
EXPOSE 80
```

---

## 🔐 Sécurité

### À Faire en Production

✅ **HTTPS** : Activer SSL/TLS  
✅ **Authentification** : Ajouter JWT ou OAuth  
✅ **Rate Limiting** : Limiter les appels API  
✅ **CORS** : Restreindre les origines autorisées  
✅ **Validation** : Sanitize les inputs utilisateur  
✅ **Logs** : Monitorer les requêtes

---

## 📚 Ressources

- [Documentation Parlant](https://parlant.io/docs)
- [API Reference](https://parlant.io/docs/api)
- [Examples](https://github.com/emcie-co/parlant/examples)

---

## 🤝 Contribution

Améliorations bienvenues ! N'hésitez pas à :
- Ajouter des fonctionnalités
- Améliorer le design
- Corriger des bugs

---

## 📄 Licence

Apache 2.0 - Voir LICENSE

---

**Besoin d'aide ?** Consultez la [documentation principale](../README.md)

