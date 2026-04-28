"# ARGO GLPI Monitor - Web & Teams

## ðŸŽ¯ VisÃ£o Geral

Este projeto contÃ©m **duas funcionalidades** para monitoramento de chamados do GLPI:

1. **Dashboard Web** - Interface grÃ¡fica acessÃ­vel via navegador
2. **Script Teams** - Envio automÃ¡tico de notificaÃ§Ãµes para o Microsoft Teams

---

## ðŸš€ Funcionalidades

### **1. Dashboard Web**
- Interface fluida com **Sistema de Abas (Tabs)** e layout **Masonry** (Colunas dinÃ¢micas).
- Suporte nativo ao Dark Mode usando Tailwind CSS.
- Abas de monitoramento:
  - ðŸ•’ **SustentaÃ§Ã£o & DBA**: Aguardando Atendimento, SLA CrÃ­tico (< 1h), Sem InteraÃ§Ã£o (+3 dias) e DBA Urgente.
  - ðŸš€ **Projetos Ativos**: Chamados especÃ­ficos de escopos de projeto (TIC/GPM).
  - âœ… **Finalizados**: HistÃ³rico visual do que foi entregue no mÃªs.
- MultiusuÃ¡rio com input livre de e-mail e auto-refresh dinÃ¢mico (5 a 60 minutos).

### **2. Script Teams**
- Envia notificaÃ§Ãµes automÃ¡ticas para o Microsoft Teams
- Dois cards: Pessoal (3 seÃ§Ãµes) e Fila DBA (1 seÃ§Ã£o)
- ExecuÃ§Ã£o manual ou agendada via cron/task scheduler

### **3. Controles de AtualizaÃ§Ã£o**
- Auto-refresh a cada 5 minutos
- BotÃ£o "Atualizar Agora" para refresh manual
- Tratamento de erros com mensagens visÃ­veis na tela

---

## ðŸ“‹ PrÃ©-requisitos

- Python 3.8+
- GLPI Server/DC com API v3
- Flask
- Python-dotenv
- requests

---

## ðŸ› ï¸ InstalaÃ§Ã£o (ProduÃ§Ã£o na OCI)

O sistema conta com uma esteira de deploy 100% automatizada. Para instalar ou atualizar o sistema no servidor de produÃ§Ã£o (Oracle Linux), um humano precisa executar apenas 1 comando:

```bash
curl -sSL https://raw.githubusercontent.com/escti/ARGO_glpi2teams/main/deploy.sh | bash
```

**O que o script faz sozinho:**
1. Instala Git e Docker (se nÃ£o existirem)
2. Clona ou sincroniza o repositÃ³rio (`git reset --hard`)
3. Valida a existÃªncia do arquivo `.env` de seguranÃ§a
4. DestrÃ³i containers antigos, recria a build com as novas modificaÃ§Ãµes e limpa o lixo de memÃ³ria do Docker

*(AtenÃ§Ã£o: Na primeira vez, o script irÃ¡ pausar pedindo que vocÃª edite o `.env` com seu Token do GLPI antes de prosseguir).*

---

## ðŸ› ï¸ Modo Desenvolvimento Local
Caso nÃ£o queira rodar em containers para criar testes na prÃ³pria mÃ¡quina:
1. `pip install -r requirements.txt`
2. `copy .env.example .env` e o edite.
3. Para UI web: `python src/app.py`
4. Para fluxo bot: `python src/GLPI_to_teams.py`

---

## ðŸŽ® Como Usar

### **1. Dashboard Web**

**Primeira vez:**
1. Abra a URL do dashboard
2. Aguarde o carregamento automÃ¡tico (5 minutos) ou clique em "Atualizar Agora"

**Alternar usuÃ¡rio:**
1. Clique no dropdown "UsuÃ¡rio" no topo direito
2. Selecione o usuÃ¡rio desejado
3. Os dados atualizam automaticamente para aquele usuÃ¡rio

**AtualizaÃ§Ã£o manual:**
1. Clique no botÃ£o "Atualizar Agora"
2. Aguarde o spinner de carregamento
3. Dados atualizados!

### **2. Bot Microsoft Teams**

**Funcionamento em Fundo (Docker):**
ApÃ³s lanÃ§ada pela instalaÃ§Ã£o, o Bot passarÃ¡ a rodar automaticamente e nÃ£o requer ativaÃ§Ã£o manual. 
Sempre que uma hora se passar (entre as 07h e 17h, **de segunda a sexta-feira**) ele baterÃ¡ automaticamente o relÃ³gio interno no minuto `59` para puxar os novos resultados e mandar os Cards.

Cheque a atividade utilizando:
```bash
docker-compose logs -f GLPI-notifier
```

---

## ðŸ”„ Comparativo: Web vs Teams

| CaracterÃ­stica | Web | Teams |
|---------------|-----|-------|
| **Interface** | Navegador (Bootstrap) | NotificaÃ§Ã£o inline |
| **UsuÃ¡rios** | MultiusuÃ¡rio (dropdown) | Geralmente 1 destinatÃ¡rio |
| **AtualizaÃ§Ã£o** | Auto-refresh a cada 5 min | Manual ou agendado |
| **Interatividade** | Alta (botÃµes, links) | Baixa (links clicÃ¡veis) |
| **PersistÃªncia** | SessÃ£o do navegador | Mensagem no chat |
| **Melhor para** | Monitoramento ativo | Alertas rÃ¡pidos |

---

## ðŸ”§ Estrutura do Projeto

Para facilitar o entendimento profundo da arquitetura, criamos um mapa detalhado. 
ðŸ‘‰ **Consulte o arquivo [FILE_MAP.md](FILE_MAP.md)** para ver a explicaÃ§Ã£o de lÃ³gica, funÃ§Ãµes e mÃ©todos de cada um dos arquivos abaixo.

```
ARGO_glpi2teams/
â”œâ”€â”€ docs/                       # DocumentaÃ§Ãµes de setup e versÃµes antigas
â”œâ”€â”€ src/                        # CÃ³digo-fonte da aplicaÃ§Ã£o
â”‚   â”œâ”€â”€ app.py                  # Backend Flask (Web)
â”‚   â”œâ”€â”€ GLPI_service.py         # LÃ³gica integrada de conexÃ£o com GLPI
â”‚   â”œâ”€â”€ GLPI_to_teams.py        # Loop Bot do Teams
â”‚   â””â”€â”€ templates/
â”‚       â””â”€â”€ index.html          # Frontend Web
â”œâ”€â”€ docker-compose.yml          # Setup da Stack na OCI
â”œâ”€â”€ Dockerfile                  # Build base para python e deps OCI
â”œâ”€â”€ requirements.txt            # DependÃªncias unificadas Python
â”œâ”€â”€ .env.example                # Exemplo de configuraÃ§Ã£o unificada
â”œâ”€â”€ README.md                   # DocumentaÃ§Ã£o Unificada
â””â”€â”€ FILE_MAP.md                 # ðŸ—ºï¸ Mapa detalhado de contexto para IA e Devs
```

---

## ðŸ“Š Fluxo de Dados

```
Frontend (HTML/JS)
    â†“ (fetch /api/data?user=X)
Backend (Flask app.py)
    â†“ (passa parÃ¢metro user)
GLPIService (GLPI_service.py)
    â†“ (substitui currentUser() por 'user_name')
GLPI API
    â†“ (retorna issues)
Frontend (atualiza tabelas)
```

---

## ðŸ” Como Funciona o MultiusuÃ¡rio

O sistema substitui dinamicamente a funÃ§Ã£o `currentUser()` do GLPI pelo nome do usuÃ¡rio selecionado:

- **Sem parÃ¢metro:** `assignee = currentUser()` â†’ Mostra chamados do usuÃ¡rio logado no GLPI
- **Com parÃ¢metro:** `assignee = 'user_name'` â†’ Mostra chamados do usuÃ¡rio especÃ­fico

### Exemplos de Queries:

| Card | Query (simplificada) |
|------|-------|
| **Aguardando** | `assignee = 'user' AND project NOT IN (...) AND statusCategory != Done` |
| **SLA CrÃ­tico** | `assignee = 'user' AND "Tempo de resoluÃ§Ã£o" <= remaining("1h")` |
| **Sem InteraÃ§Ã£o** | `assignee = 'user' AND updatedDate <= "-3d"` |
| **Projetos Ativos** | `assignee = 'user' AND project IN (TIC, GPM)` |
| **Fila DBA** | `assignee IS EMPTY AND "Grupo Solucionador" = "DC - Banco de Dados"` |

---

## ðŸ› SoluÃ§Ã£o de Problemas

### **Web (Dashboard)**

**Erro: "Erro HTTP: 401 Unauthorized"**
- Verifique as credenciais no arquivo `.env`
- Teste se a autenticaÃ§Ã£o funciona: `http://GLPI.suaempresa.com.br/rest/api/3/myself`

**Erro: "Erro desconhecido ao carregar dados"**
- Verifique se o GLPI estÃ¡ acessÃ­vel
- Confira se as queries JQL sÃ£o vÃ¡lidas no seu GLPI
- Veja os logs no console do navegador (F12 â†’ Console)

**Dropdown nÃ£o atualiza dados**
- Verifique se o evento `change` estÃ¡ sendo disparado (console do navegador)
- Abra o DevTools (F12) e veja se hÃ¡ erros na rede

**Nada aparece na tela**
- Verifique se o GLPI estÃ¡ retornando dados
- Confirme se o usuÃ¡rio selecionado tem chamados atribuÃ­dos

### **Teams (Bot AutomÃ¡tico)**

**Nada Ã© disparado?**
- Verifique se as variÃ¡veis de integraÃ§Ã£o estÃ£o Ã­ntegras e salvas antes do run.
- Lembre-se do loop: Ele enviarÃ¡ as notificaÃ§Ãµes unicamente no minuto `59` de horas entre `07:00` e `17:00`, de **segunda a sexta-feira**. Aos finais de semana ou fora do horÃ¡rio, ele estarÃ¡ apensas hibernando.
- Tente `docker logs GLPI-notifier` e avalie possÃ­veis erros nos registros internos. Pode ter sido disparada alguma exceÃ§Ã£o tratada pelas try/excepts durante o Ãºltimo despertar.

---

## ðŸ“ Autor

Equipe ARGO

---

## ðŸ“ž Suporte

Para dÃºvidas ou problemas, verifique:

**Web:**
- Console do navegador (F12)
- Logs do servidor (se rodando em produÃ§Ã£o)
- Arquivo `.env` estÃ¡ configurado corretamente

**Teams:**
- Log do script: `services/teams/GLPI_to_teams.log`
- VariÃ¡veis de ambiente no `services/teams/.env`
- Webhook URL estÃ¡ ativa e correta

---

## ðŸ”„ Fluxo de Dados

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  GLPI API   â”‚
â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”˜
       â”‚
       â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
       â”‚                             â”‚
       â–¼                             â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”              â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  Web        â”‚              â”‚  Teams      â”‚
â”‚  Dashboard  â”‚              â”‚  Script     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜              â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```
