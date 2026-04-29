from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__)

# Configuration (utilise ton app_user)
db_config = {
    "dbname": "banque_db",
    "user": "app_user",
    "password": "app_password_123",
    "host": "localhost",
    "port": "5432"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user_data = None
    error = None
    query_log = ""

    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # LA FAILLE : On concatène les deux entrées dans la requête
        query = f"SELECT username, nom, prenom, role FROM users WHERE username = '{username}' AND password = '{password}';"
        query_log = query # Pour l'afficher sur l'interface
        
        cur.execute(query)
        user_data = cur.fetchone()
        
        cur.close()
        conn.close()
    except Exception as e:
        error = str(e)

    return render_template('index.html', user=user_data, error=error, query=query_log)

@app.route('/test-rbac', methods=['POST'])
def test_rbac():
    """Simule une tentative de suppression interdite"""
    status = ""
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = 1;")
        conn.commit()
        status = "⚠️ FAIL : L'utilisateur a pu supprimer ! (Pas sécurisé)"
    except psycopg2.errors.InsufficientPrivilege:
        status = "✅ SUCCÈS : Accès refusé par Postgres (RBAC OK)"
    except Exception as e:
        status = f"Erreur : {str(e)}"
    return render_template('index.html', rbac_status=status)

if __name__ == '__main__':
    app.run(debug=True, port=5000)