---
name: documentation-algo
description: Génère la documentation technique, métier et HTML d'un script SQL Server (rétro-ingénierie d'algorithmes de santé/pharma). À utiliser quand l'utilisateur fournit un script SQL et demande sa documentation, ou demande à transformer une doc technique en doc métier, ou à mettre en forme une doc métier en HTML.
---

# Documentation d'algorithme SQL

Ce skill encode le savoir-faire pour documenter un script SQL Server
multi-statements en 3 étapes successives. Chaque étape a ses propres
règles strictes — charge UNIQUEMENT le fichier de référence correspondant
à l'étape demandée.

## Étapes disponibles

1. **Analyse technique du SQL** → charge `references/sql-analysis-rules.md`
   - Déclenché quand l'input est un script SQL brut à documenter.
   - Produit une description syntaxique et séquentielle, sans interprétation métier.

2. **Traduction en langage métier** → charge `references/business-vocabulary.md`
   - Déclenché quand l'input est une documentation technique déjà produite.
   - Traduit en langage métier, sans jamais citer de SQL/tables/colonnes.

3. **Mise en forme HTML finale** → charge `references/html-template-spec.md`
   - Déclenché quand l'input est une documentation métier validée.
   - Produit un document HTML structuré en sections A à F.

## Règle générale (toutes étapes)

- Zéro invention : si une information manque, la signaler explicitement
  dans une section "Questions / ambiguïtés" plutôt que de l'inventer.
- Ne jamais se fier aux commentaires SQL s'ils contredisent le code réel.
- Toujours terminer par une demande de validation explicite à l'utilisateur.
