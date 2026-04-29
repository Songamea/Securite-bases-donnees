from flask import Flask, request
from flask_restx import Api, Resource, fields
import psycopg2

app = Flask(__name__)
api = Api(app, title='Labo Injection SQL', description='Interface interactive pour tester les failles')

# Tes identifiants (Pense à mettre les vrais !)
db_config = {
    "dbname": "banque_db",
    "user": "app_user",
    "password": "app_password_123",
    "host": "localhost",
    "port": "5432"
}

@api.route('/user/<string:username>')
class User(Resource):
    def get(self, username):
        """Récupère un utilisateur (Attention: Vulnérable SQLi)"""
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            
            # LA FAILLE : Injection possible via le paramètre username
            query = f"SELECT nom, prenom, email FROM users WHERE username = '{username}';"
            
            cur.execute(query)
            user = cur.fetchone()
            
            cur.close()
            conn.close()
            
            if user:
                return {"nom": user[0], "prenom": user[1], "email": user[2]}, 200
            return {"error": "Utilisateur non trouvé"}, 404
            
        except Exception as e:
            return {"error": str(e)}, 500
        
    
@api.route('/test-security')
class SecurityTest(Resource):
    def get(self):
        """Vérifie si le principe du moindre privilège est appliqué"""
        results = {}
        
        # On essaie de faire un DELETE avec l'utilisateur app_user
        # (Qui n'a que SELECT, INSERT, UPDATE d'après tes contraintes)
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            
            # Tentative d'action interdite
            cur.execute("DELETE FROM users WHERE username = 'admin';")
            conn.commit()
            
            results["delete_test"] = "⚠️ ÉCHEC : L'utilisateur a pu supprimer ! (Pas sécurisé)"
            cur.close()
            conn.close()
        except psycopg2.errors.InsufficientPrivilege:
            results["delete_test"] = "✅ SUCCÈS : Suppression bloquée par PostgreSQL (Sécurisé)"
        except Exception as e:
            results["delete_test"] = f"Erreur : {str(e)}"
            
        return results

if __name__ == '__main__':
    app.run(debug=True, port=5000)