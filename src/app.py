from flask import Flask, render_template, jsonify, request
from glpi_service import GlpiClient
import os

app = Flask(__name__)
glpi_client = GlpiClient()

@app.route('/')
def index():
    # Pega os usuários definidos no .env para popular o dropdown
    users_str = os.getenv('GLPI_DASHBOARD_USERS', '')
    users = [u.strip() for u in users_str.split(',')] if users_str else ['Todos']
    return render_template('index.html', users=users)

@app.route('/api/data')
def get_data():
    user = request.args.get('user')
    try:
        data = glpi_client.get_dashboard_data(user=user)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
