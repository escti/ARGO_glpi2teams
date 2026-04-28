import os
import requests
import urllib3
import urllib.parse
from datetime import datetime, timedelta
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

GLPI_URL = os.getenv('GLPI_URL', '').rstrip('/')
GLPI_APP_TOKEN = os.getenv('GLPI_APP_TOKEN', '')
GLPI_USER_TOKEN = os.getenv('GLPI_USER_TOKEN', '')

class GlpiClient:
    def __init__(self):
        self.base_url = f"{GLPI_URL}/apirest.php"
        self.session_token = None
        self.headers = {
            'Content-Type': 'application/json'
        }
        if GLPI_APP_TOKEN:
            self.headers['App-Token'] = GLPI_APP_TOKEN

    def _init_session(self):
        if self.session_token:
            return True
            
        try:
            headers = self.headers.copy()
            headers['Authorization'] = f"user_token {GLPI_USER_TOKEN}"
            
            response = requests.get(
                f"{self.base_url}/initSession", 
                headers=headers,
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            
            self.session_token = response.json().get('session_token')
            self.headers['Session-Token'] = self.session_token
            return True
        except Exception as e:
            print(f"Erro ao inicializar sessão no GLPI: {e}")
            return False

    def _search_tickets(self, criteria_list, forcedisplay=None):
        if not self._init_session():
            return []
            
        params = {
            'is_deleted': 0,
            'as_map': 0,
            'range': '0-100'
        }
        
        # Monta os critérios dinamicamente
        for idx, criteria in enumerate(criteria_list):
            params[f'criteria[{idx}][link]'] = criteria.get('link', 'AND')
            params[f'criteria[{idx}][field]'] = criteria['field']
            params[f'criteria[{idx}][searchtype]'] = criteria.get('searchtype', 'equals')
            params[f'criteria[{idx}][value]'] = criteria['value']
            
        # Força exibição de colunas específicas para não precisar fazer múltiplas chamadas
        if forcedisplay:
            for idx, field in enumerate(forcedisplay):
                params[f'forcedisplay[{idx}]'] = field
                
        try:
            query_string = urllib.parse.urlencode(params)
            response = requests.get(
                f"{self.base_url}/search/Ticket?{query_string}", 
                headers=self.headers,
                verify=False,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            return data.get('data', [])
        except Exception as e:
            print(f"Erro ao buscar chamados no GLPI: {e}")
            return []

    def _format_ticket(self, ticket_data):
        # Mapeamento padrão dos campos de retorno da API do GLPI
        # 1: Título, 2: ID, 12: Status, 15: Data Criação, 19: Data Atualização, 18: Tempo Solução
        ticket_id = ticket_data.get('2', '')
        return {
            "key": f"GLPI-{ticket_id}",
            "summary": ticket_data.get('1', 'Sem título'),
            "status": str(ticket_data.get('12', '')), # Pode ser o ID do status ou nome dependendo do GLPI
            "created": ticket_data.get('15', ''),
            "updated": ticket_data.get('19', ''),
            "time_to_resolve": ticket_data.get('18', ''),
            "url": f"{GLPI_URL}/front/ticket.form.php?id={ticket_id}"
        }

    def _get_user_id(self, username):
        if not username or username == 'Todos':
            return 'myself'
        if not self._init_session():
            return 'myself'
        try:
            params = {
                'is_deleted': 0,
                'as_map': 0,
                'range': '0-1',
                'criteria[0][field]': 1, # name (username) ou 9 para e-mail
                'criteria[0][searchtype]': 'contains',
                'criteria[0][value]': username
            }
            query_string = urllib.parse.urlencode(params)
            response = requests.get(
                f"{self.base_url}/search/User?{query_string}", 
                headers=self.headers,
                verify=False,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                users = data.get('data', [])
                if users:
                    return users[0].get('2', 'myself') # id do usuário é o field 2
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
        return 'myself'

    def get_dashboard_data(self, user=None):
        user_id = self._get_user_id(user)
        
        dashboard = {
            'aguardando': [],
            'sla': [],
            'sem_interacao': [],
            'projetos': [],
            'dba': []
        }
        
        # Campos que queremos: 1(Título), 2(ID), 12(Status), 15(Criação), 19(Atualização), 18(SLA)
        forced_fields = [1, 2, 12, 15, 19, 18]
        
        # 1. BUSCA DOS CHAMADOS DO USUÁRIO
        user_criteria = [
            {'field': 12, 'value': 'notold'},
            {'field': 5, 'value': user_id}
        ]
        user_tickets = self._search_tickets(user_criteria, forcedisplay=forced_fields)
        
        now = datetime.now()
        three_days_ago = now - timedelta(days=3)
        
        for t in user_tickets:
            formatted = self._format_ticket(t)
            
            # Todos vão para aguardando
            dashboard['aguardando'].append(formatted)
            
            # Verifica Sem Interação (Data de atualização > 3 dias)
            updated_str = formatted.get('updated')
            if updated_str:
                try:
                    updated_date = datetime.strptime(updated_str, "%Y-%m-%d %H:%M:%S")
                    if updated_date < three_days_ago:
                        dashboard['sem_interacao'].append(formatted)
                except:
                    pass
                    
            # Verifica SLA (Menos de 1h)
            sla_str = formatted.get('time_to_resolve')
            if sla_str:
                try:
                    sla_date = datetime.strptime(sla_str, "%Y-%m-%d %H:%M:%S")
                    if now <= sla_date <= (now + timedelta(hours=1)):
                        dashboard['sla'].append(formatted)
                except:
                    pass
        
        # 2. BUSCA DA FILA DBA
        dba_criteria = [
            {'field': 12, 'value': 'notold'},
            {'field': 8, 'value': '137'}, # Grupo DBA
            {'field': 5, 'searchtype': 'notequals', 'value': 'myself'} # Conforme seu filtro
        ]
        dba_tickets = self._search_tickets(dba_criteria, forcedisplay=forced_fields)
        
        for t in dba_tickets:
            dashboard['dba'].append(self._format_ticket(t))
            
        return dashboard
