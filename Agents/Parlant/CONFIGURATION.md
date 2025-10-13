# ⚙️ Configuration de votre Agent Médical

## 🔑 Configuration OpenAI (REQUIS)

### Étape 1 : Obtenir une clé API

1. Allez sur https://platform.openai.com/api-keys
2. Créez un compte si nécessaire
3. Cliquez sur "Create new secret key"
4. Copiez la clé (elle commence par `sk-...`)

### Étape 2 : Créer le fichier `.env`

Créez un fichier `.env` dans le dossier `mon_agent_medical/` avec ce contenu :

```bash
# Votre clé API OpenAI
OPENAI_API_KEY=sk-votre-vraie-clé-ici
```

**⚠️ IMPORTANT : Ne partagez JAMAIS votre clé API !**

### Étape 3 : (Optionnel) Choisir le modèle

Par défaut, Parlant utilise `gpt-4o`. Vous pouvez changer en ajoutant dans `.env` :

```bash
# Pour plus de performance
OPENAI_MODEL=gpt-4o

# Pour réduire les coûts
OPENAI_MODEL=gpt-4o-mini

# Pour maximum de performance
OPENAI_MODEL=gpt-4-turbo
```

## 💰 Coûts estimés

| Modèle | Prix | Usage recommandé |
|--------|------|------------------|
| `gpt-4o` | $$ | Production (balance coût/perf) |
| `gpt-4o-mini` | $ | Développement/tests |
| `gpt-4-turbo` | $$$ | Cas critiques |

## ✅ Vérifier la configuration

Une fois configuré, testez :

```bash
python my_healthcare_agent.py
```

Si la clé est invalide, vous verrez une erreur :
```
OpenAI API Error: Incorrect API key provided
```

## 🔄 Autres LLM (Optionnel)

Si vous préférez Claude, Gemini ou d'autres, consultez :
- [Documentation Vertex AI](../parlant/docs/adapters/nlp/vertex.md)
- [Documentation Ollama](../parlant/docs/adapters/nlp/ollama.md) (modèles locaux gratuits)

