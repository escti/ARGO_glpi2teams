import os
import requests
import urllib3
from datetime import datetime
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

GLPI_URL = os.getenv('GLPI_URL', '')
GLPI_APP_TOKEN = os.getenv('GLPI_APP_TOKEN', '')
GLPI_USER_TOKEN = os.getenv('GLPI_USER_TOKEN', '')

class GlpiClient:
    def __init__(self):
        self.base_url = f"{GLPI_URL.rstrip('/')}/apirest.php"
        self.session_token = None
        self.headers = {
            'App-Token': GLPI_APP_TOKEN,
            'Content-Type': 'application/json'
        }

    def _init_session(self):
        # Mock do initSession
        self.session_token = "mock_session_token_12345"
        self.headers['Session-Token'] = self.session_token
        return True

    def get_dashboard_data(self, user=None):
        print(f"Buscando dados mockados do GLPI para o usuário: {user or 'Todos'}")
        
        # Mocks baseados nas necessidades da interface
        return {
            'aguardando': [
                {"key": "GLPI-001", "summary": "Problema de acesso a rede", "status": "Novo", "created": "2026-04-27T10:00:00.000+0000", "url": f"{GLPI_URL}/front/ticket.form.php?id=1"}
            ],
            'sla': [
                {"key": "GLPI-002", "summary": "Troca de HD", "status": "Em andamento", "created": "2026-04-26T10:00:00.000+0000", "url": f"{GLPI_URL}/front/ticket.form.php?id=2"}
            ],
            'sem_interacao': [],
            'projetos': [
                {"key": "GLPI-003", "summary": "Migração de Servidor", "status": "Planejado", "created": "2026-04-20T10:00:00.000+0000", "url": f"{GLPI_URL}/front/ticket.form.php?id=3"}
            ],
            'finalizados': [
                {"key": "GLPI-004", "summary": "Reset de senha", "status": "Resolvido", "created": "2026-04-27T08:00:00.000+0000", "url": f"{GLPI_URL}/front/ticket.form.php?id=4"}
            ],
            'dba': []
        }
