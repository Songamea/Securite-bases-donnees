**Labo de Sécurité — Injection SQL & RBAC**

Description
- Projet pédagogique : démonstration des risques d'injection SQL dans une interface d'authentification et vérification de la séparation des privilèges (RBAC) avec PostgreSQL.

Principales fonctionnalités
- Contournement d'authentification (scénarios d'injection SQL).
- Affichage de la requête SQL construite pour faciliter l'analyse pédagogique.
- Tests RBAC : simulation d'opérations protégées (ex. DELETE) pour observer les permissions PostgreSQL.

Prérequis
- Python 3.8+ (ou équivalent)
- PostgreSQL
- (Optionnel) Docker & Docker Compose

Installation (locale)
1. Créez et activez un environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate     # Windows
```

2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

Si `requirements.txt` n'existe pas, installez au minimum :

```bash
pip install flask psycopg2-binary
```

Configuration
- Modifiez la configuration de la base de données dans `app.py` (variable `db_config`) pour pointer vers votre instance PostgreSQL :

```python
db_config = {
        "dbname": "votre_base",
        "user": "app_user",
        "password": "votre_mot_de_passe",
        "host": "localhost",
        "port": "5432"
}
```

Initialisation de la base
- Exécutez les scripts SQL dans `init-scripts/` (si fournis) ou créez la table `users` et les rôles nécessaires.

Exemple minimal :

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    email VARCHAR(255),
    role VARCHAR(20)
);

INSERT INTO users (username, password, nom, prenom, email, role)
VALUES ('admin', 'admin123', 'Leuba', 'Léo', 'admin@lab.com', 'Directeur');

CREATE ROLE app_user WITH LOGIN PASSWORD 'votre_mot_de_passe';
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE ON users TO app_user;
-- Ne pas accorder DELETE si l'on veut démontrer RBAC
```

Exécution
- Local (développement) :

```bash
python app.py
# puis ouvrir http://127.0.0.1:5000
```

- Avec Docker :

```bash
docker-compose up --build
```

Scénarios de test (pédagogiques)
- Contournement de login (commentaire SQL) :

    - Username : `admin' --`
    - Password : (vide)

    Explication : le `--` commente le reste de la requête, neutralisant la vérification du mot de passe.

- Condition "always true" :

    - Username : `admin`
    - Password : `' OR '1'='1`

    Explication : l'expression `'1'='1'` est toujours vraie, donc la condition d'authentification peut être contournée si les entrées ne sont pas paramétrées.

- Test RBAC (suppression) :

    - Cliquez sur le test de suppression dans l'interface.
    - Résultat attendu : PostgreSQL renvoie une erreur `insufficient_privilege` si l'utilisateur de l'application n'a pas le droit `DELETE`.

Structure du projet
- [app.py](app.py) — serveur Flask et logique d'accès aux données
- [docker-compose.yml](docker-compose.yml) — orchestration Docker (si fournie)
- [dockerfile](dockerfile) — image Docker (si fournie)
- [init-scripts/](init-scripts/) — scripts SQL d'initialisation (si présents)
- [templates/index.html](templates/index.html) — interface utilisateur
- [README.md](README.md) — documentation (ce fichier)

Avertissement important
- Ce projet est strictement pédagogique. N'utilisez jamais de concaténation de chaînes ou de f-strings pour construire des requêtes SQL dans une application réelle. Utilisez systématiquement des requêtes paramétrées (prepared statements) ou des ORM sécurisés.

Contribuer
- Vous pouvez ouvrir une issue ou proposer une pull request pour améliorer les scénarios, ajouter des tests ou corriger la documentation.

Licence
- (Indiquez la licence de votre choix ici)
