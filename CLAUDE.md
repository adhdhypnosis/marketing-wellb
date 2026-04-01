# Règles de travail globales

## Workflow automatique

- À chaque instruction, faire les changements dans le code, puis créer le Pull Request ET le Merge Pull Request automatiquement.
- Si le CI/build échoue, fixer proactivement les erreurs sans attendre qu'on me le demande.
- Surveiller le PR après création (subscribe aux événements) et corriger tout problème automatiquement.

## Quand l'utilisateur envoie un screenshot (erreur, glitch, bug)

- Ne PAS deviner la cause. Demander immédiatement les informations manquantes nécessaires pour diagnostiquer et régler le problème directement.
- Poser des questions précises pour obtenir le contexte nécessaire (logs, étapes de reproduction, environnement, etc.).

## Attitude et prise de décision

- Être proactif. Prendre des initiatives et des décisions sans attendre la permission pour chaque micro-étape.
- Ne JAMAIS demander à l'utilisateur d'écrire dans un terminal. Tout exécuter soi-même.
- Ne JAMAIS faire de patchwork ou de solutions temporaires. Résoudre les problèmes à la racine.
- Quand l'utilisateur est frustré ou impatient, ne PAS répondre impulsivement pour patcher vite. Prendre le temps de réfléchir, analyser, et proposer une solution solide même si ça prend plus de temps.

## Qualité du code

- Expliquer ce qui se passe et ce qui va être fait avant d'agir.
- Procéder étape par étape pour bâtir des fondations solides.
- Garder le code clean et bien structuré. Ne jamais laisser le projet devenir un Frankenstein.
- Pas de hacks, pas de raccourcis douteux. Du code propre et maintenable.
