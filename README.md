🛡️ Labo de Sécurité : SQL Injection & RBAC
Ce projet est une application web de démonstration conçue pour illustrer les risques d'injection SQL dans une interface d'authentification et l'efficacité des politiques de moindre privilège (RBAC) avec PostgreSQL.

📋 Fonctionnalités
Contournement d'authentification : Tester des injections SQL pour se connecter sans mot de passe.

Visualisation en temps réel : Affichage de la requête SQL générée par le serveur.

Audit RBAC : Bouton de test pour vérifier si les droits de l'utilisateur de l'application sont correctement restreints.

🛠️ Installation et Configuration
1. Prérequis
Python 3.x

PostgreSQL

Bibliothèques Python :

Bash
pip install flask psycopg2
2. Configuration de la Base de Données
Exécutez le script SQL suivant dans votre terminal psql ou via pgAdmin pour créer la structure et les rôles :

SQL
-- Création de la table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    email VARCHAR(255),
    role VARCHAR(20)
);

-- Insertion de données de test
INSERT INTO users (username, password, nom, prenom, email, role) 
VALUES ('admin', 'admin123', 'Leuba', 'Léo', 'admin@lab.com', 'Directeur');

-- Configuration du RBAC
CREATE ROLE app_user WITH LOGIN PASSWORD 'votre_mot_de_passe';
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE ON users TO app_user; 
-- Note : app_user n'a PAS le droit de DELETE
3. Configuration de l'Application
Modifiez le dictionnaire db_config dans app.py avec vos accès :

Python
db_config = {
    "dbname": "votre_base",
    "user": "app_user",
    "password": "votre_mot_de_passe",
    "host": "localhost",
    "port": "5432"
}
🚀 Utilisation
Lancez le serveur :

Bash
python app.py
Ouvrez votre navigateur sur http://127.0.0.1:5000.

🧪 Scénarios de Test
A. Attaque par Injection SQL (Contournement de Login)
Pour se connecter en tant qu'administrateur sans connaître son mot de passe :

Username : admin' --

Password : (Laissez vide ou n'importe quoi)

Explication : Le -- commente la vérification du mot de passe dans la requête SQL.

B. Attaque "Always True"
Username : admin

Password : ' OR '1'='1

Explication : La condition '1'='1' étant toujours vraie, le moteur SQL autorise la connexion.

C. Test de Résilience (RBAC)
Cliquez sur le bouton "Lancer le test de suppression".

L'application tentera d'exécuter DELETE FROM users.

Résultat attendu : Une erreur PostgreSQL InsufficientPrivilege s'affiche, prouvant que même si une injection permet de lancer la commande, la base de données bloque l'action.

📂 Structure du Projet
Plaintext
.
├── app.py              # Serveur Flask et logique SQL
├── templates/
│   └── index.html      # Interface utilisateur (Bootstrap)
└── README.md           # Ce fichier
⚠️ Avertissement : Ce projet est à but pédagogique uniquement. Ne jamais utiliser de requêtes formatées avec des f-strings (f"...") dans une application réelle. Utilisez toujours des requêtes paramétrées.
