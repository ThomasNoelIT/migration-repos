# migration-repos

Un outil d’automatisation pour transférer progressivement des dépôts GitHub d’un compte personnel vers un compte professionnel.  
Chaque jour, un dépôt est migré automatiquement grâce à un workflow GitHub Actions, jusqu’à ce que la liste définie soit entièrement copiée.

---

## 🚀 Fonctionnalités
- Lecture d’une liste de dépôts à migrer (`repos.txt`).
- Création automatique du dépôt cible sur le compte professionnel.
- Migration complète de l’historique Git (`--mirror`).
- Ajout automatique d’un README vide sur chaque nouveau dépôt.
- Gestion de la progression (`progress.txt`) pour migrer un dépôt différent chaque jour.
- Exécution planifiée via **GitHub Actions** (cron job).

---

## 📂 Structure du projet

```text
migration-repos/
├── .github/
│   └── workflows/
│       └── migrate.yml   # Workflow GitHub Actions
├── migrate.py            # Script Python de migration
├── repos.txt             # Liste des dépôts à migrer
└── progress.txt          # Avancement (mis à jour automatiquement)
```


---

## ⚙️ Configuration

### 1. Définir la liste des dépôts
Dans `repos.txt`, ajouter un dépôt par ligne (nom exact tel qu’il apparaît sur GitHub) :

mon-projet-1
mon-projet-2
mon-projet-3


### 2. Créer les tokens GitHub
- **SOURCE_TOKEN** : PAT (Personal Access Token) du compte **personnel** avec accès lecture (`repo`).
- **DEST_TOKEN** : PAT du compte **professionnel** avec accès écriture (`repo`).

> 📌 Les tokens doivent être ajoutés en tant que **secrets GitHub** dans  
> `Settings > Secrets and variables > Actions`.

### 3. Planification du workflow
Le workflow `migrate.yml` est configuré pour tourner **tous les jours à 9h UTC** :

```yaml
on:
  schedule:
    - cron: "0 9 * * *"
  workflow_dispatch: # déclenchement manuel possible
```

▶️ Utilisation
Créer un dépôt migration-repos sur le compte professionnel.
Copier ces fichiers (migrate.py, repos.txt, workflow).
Configurer les secrets SOURCE_TOKEN et DEST_TOKEN.
Pousser le projet sur GitHub.
Laisser GitHub Actions tourner : chaque jour un dépôt sera transféré automatiquement.

📝 Notes
Les dépôts sont créés publics par défaut. Modifier migrate.py (private=True) pour les créer en privé.
Le script ajoute un README.md vide lors de la création. Tu pourras le compléter manuellement plus tard.
La migration inclut tout l’historique Git (git push --mirror).

📜 Licence
Ce projet est fourni tel quel, sans garantie. Utilisation libre et modification autorisée.
