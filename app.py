from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Configuration de ta base (à adapter)
db_config = {
    "dbname": "banque_db",
    "user": "banque_user",
    "password": "ChangeMe123!",
    "port": "5432"
}

@app.route('/user', methods=['GET'])
def get_user():
    username = request.args.get('username')
    
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    
    # --- LA FAILLE EST ICI ---
    # On insère directement la variable dans la chaîne SQL
    query = f"SELECT nom, prenom, email FROM users WHERE username = '{username}';"
    
    try:
        cur.execute(query)
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            return jsonify({"nom": user[0], "prenom": user[1], "email": user[2]})
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)