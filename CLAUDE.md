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

## Instructions manuelles pour interfaces tierces (Supabase, GitHub, Vercel, etc.)

Lorsque l'utilisateur doit effectuer une intervention manuelle dans une interface web tierce (Supabase, GitHub, Vercel, Stripe, Google Cloud Console, etc.), suivre cette règle **avant** de rédiger les étapes :

1. **Vérifier l'interface réelle avant de l'écrire.** Ne jamais décrire un bouton, un onglet, un menu ou un libellé de mémoire. Les UIs de ces produits changent souvent et les libellés exacts comptent pour l'utilisateur (qui clique en aveugle).

2. **Méthode de vérification (par ordre de préférence)** :
   - Utiliser `WebFetch` sur la page de documentation officielle qui décrit l'écran concerné (ex: `supabase.com/docs/...`, `vercel.com/docs/...`, `docs.github.com/...`). Citer le lien dans la réponse.
   - Si la doc ne suffit pas, utiliser `WebSearch` pour confirmer le libellé/chemin exact dans la version actuelle de l'UI.
   - Pour GitHub, préférer un outil MCP `mcp__github__*` qui exécute l'action directement plutôt qu'une navigation manuelle.
   - Pour Vercel, utiliser les outils MCP Vercel disponibles (`get_project`, `list_deployments`, `deploy_to_vercel`, etc.) plutôt que d'envoyer l'utilisateur dans le dashboard quand c'est possible.

3. **Format des instructions manuelles** :
   - Donner l'URL exacte de la page de départ (ex: `https://supabase.com/dashboard/project/<ref>/editor`).
   - Indiquer les libellés **mot pour mot** tels qu'ils apparaissent dans l'UI (entre guillemets), pas une paraphrase.
   - Préciser l'emplacement (sidebar gauche, onglet en haut, menu contextuel "...", etc.).
   - Numéroter chaque clic / champ à remplir.
   - Si une étape n'a pas pu être vérifiée, le **dire explicitement** ("je ne suis pas certain du libellé exact, vérifie dans le menu X") plutôt que d'inventer.

4. **Si la vérification échoue** (doc indisponible, page derrière un login), demander à l'utilisateur un screenshot de l'écran de départ **avant** de rédiger les étapes, plutôt que de deviner et d'itérer ensuite sur des erreurs.

5. **Préférer l'automatisation à l'instruction manuelle** quand c'est possible : SQL via le MCP/CLI Supabase, commits via git, déploiements via CLI Vercel, etc. Ne basculer en instructions cliquables que si l'action n'est pas scriptable ou que l'utilisateur le demande.
