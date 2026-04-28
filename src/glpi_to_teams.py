import os
import requests
import time
from datetime import datetime
import pytz
import logging
import json
from glpi_service import GlpiClient

logging.basicConfig(
    filename='logs/glpi_to_teams.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL')
GLPI_URL = os.getenv('GLPI_URL')

if not TEAMS_WEBHOOK_URL:
    logging.error("Variável TEAMS_WEBHOOK_URL não configurada")
    # Removido exit(1) para não quebrar o docker container caso falte temporariamente

glpi = GlpiClient()

def send_to_teams(payload):
    if not TEAMS_WEBHOOK_URL:
        return False
    try:
        response = requests.post(
            TEAMS_WEBHOOK_URL,
            headers={"Content-Type": "application/json"},
            json=payload
        )
        response.raise_for_status()
        return True
    except Exception as e:
        logging.error(f"Erro ao enviar para o Teams: {e}")
        return False

def pull_and_send_notifications():
    tz = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.now(tz).strftime('%d/%m/%Y %H:%M')
    
    try:
        data = glpi.get_dashboard_data()

        first_message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0078D7",
            "title": "Seus Chamados no GLPI",
            "text": f"Atualizado em: {current_time}",
            "sections": []
        }

        sections_config = [
            {"key": "aguardando", "title": "⏳ Chamados Aguardando Atendimento"},
            {"key": "sla", "title": "⚠️ Chamados que o SLA Vai Estourar"},
            {"key": "sem_interacao", "title": "🕰️ Chamados Sem Interação"},
            {"key": "projetos", "title": "🚀 Projetos Ativos"},
            {"key": "finalizados", "title": "✅ Chamados Finalizados"}
        ]

        for config in sections_config:
            issues = data.get(config["key"], [])
            section = {
                "activityTitle": f"**{config['title']}** ({len(issues)})",
                "facts": []
            }
            
            if not issues:
                section["facts"].append({"name": "Status", "value": "Nenhum chamado encontrado."})
            else:
                for issue in issues:
                    section["facts"].append({
                        "name": issue["key"],
                        "value": f"{issue['summary']} | Atualizado: {issue['created']} | [Abrir]({issue['url']})"
                    })
            first_message["sections"].append(section)

        first_message["potentialAction"] = [{
            "@type": "OpenUri",
            "name": "Ver todos no GLPI",
            "targets": [{"os": "default", "uri": f"{GLPI_URL}/front/ticket.php"}]
        }]

        send_to_teams(first_message)

        dba_issues = data.get("dba", [])
        second_message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FF0000",
            "title": "Alertas de Fila DBA no GLPI",
            "text": f"Atualizado em: {current_time}",
            "sections": [{
                "activityTitle": f"**🔥 Fila DBA Sem Responsável** ({len(dba_issues)})",
                "facts": []
            }]
        }

        if not dba_issues:
            second_message["sections"][0]["facts"].append({"name": "Status", "value": "Nenhum chamado encontrado."})
        else:
            for issue in dba_issues:
                second_message["sections"][0]["facts"].append({
                    "name": issue["key"],
                    "value": f"{issue['summary']} | Atualizado: {issue['created']} | [Abrir]({issue['url']})"
                })

        second_message["potentialAction"] = [{
            "@type": "OpenUri",
            "name": "Ver Fila DBA no GLPI",
            "targets": [{"os": "default", "uri": f"{GLPI_URL}/front/ticket.php"}]
        }]

        send_to_teams(second_message)

        logging.info("Processo concluído via Service")
    except Exception as e:
        logging.error(f"Erro na execução da rotina: {e}")

logging.info("Iniciando rotina de monitoramento GLPI para Teams...")

if __name__ == "__main__":
    while True:
        try:
            tz = pytz.timezone('America/Sao_Paulo')
            now = datetime.now(tz)
            
            if now.minute == 59 and 7 <= now.hour <= 17 and now.weekday() <= 4:
                logging.info(f"Executando envio agendado das {now.strftime('%H:%M')}")
                pull_and_send_notifications()
                time.sleep(61)
            else:
                time.sleep(30)
        except Exception as e:
            logging.error(f"Erro no loop principal do Teams Notifier: {e}")
            time.sleep(30)
