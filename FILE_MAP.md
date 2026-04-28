# ðŸ—ºï¸ Mapa de Arquivos (Context Map)

> **âš ï¸ AVISO CRÃTICO PARA IA:** Antes de iniciar qualquer tarefa de codificaÃ§Ã£o, refatoraÃ§Ã£o ou planejamento neste repositÃ³rio, **VOCÃŠ DEVE OBRIGATORIAMENTE LER O ARQUIVO `SKILL.md` COMO SUA BÃBLIA ABSOLUTA**. LÃ¡ estÃ£o as regras intransigentes de arquitetura, UI/UX e controle de versÃ£o (SemVer) que nÃ£o podem ser violadas sob nenhuma hipÃ³tese.

Este documento serve como um guia rÃ¡pido detalhado da estrutura interna do projeto **ARGO glpi2teams**. Seu objetivo principal Ã© fornecer contexto tÃ©cnico imediato para a IA e desenvolvedores, evitando a necessidade de ler todos os arquivos para entender a arquitetura.

---

## ðŸ–¥ï¸ Backend (Python)

### `src/app.py`
- **DescriÃ§Ã£o:** Servidor web principal baseado em Flask. ResponsÃ¡vel por hospedar a interface web e servir os dados via API.
- **Rotas:**
  - `/`: Renderiza o `index.html`. Extrai inteligentemente o prefixo do `GLPI_USERNAME` para nÃ£o forÃ§ar o usuÃ¡rio a digitar na primeira carga.
  - `/api/data`: Endpoint consumido pelo frontend para buscar os chamados atualizados via `GLPI_service.py`.

### `src/GLPI_service.py`
- **DescriÃ§Ã£o:** Classe de integraÃ§Ã£o e inteligÃªncia (`GLPIClient`) que faz as chamadas HTTP para a API v3 do GLPI Cloud.
- **LÃ³gica Principal:**
  - `run_jql_query()`: Executa queries (tenta endpoint primÃ¡rio e fallback) com tratamento de erro e logs de auditoria no terminal.
  - `get_dashboard_data()`: Centraliza as 6 queries JQL principais do sistema (SustentaÃ§Ã£o, SLA, Finalizados, Sem InteraÃ§Ã£o, DBA e Projetos Ativos) e agora injeta o "statusCategory" dinamicamente no retorno.
  - **Mapeamento de UsuÃ¡rio:** O sistema agora Ã© dinÃ¢mico, recebendo e-mails inteiros (ex: `thiago.albuquerque`) do input de texto para mapear o `assignee` com precisÃ£o, ao invÃ©s de usar dropdowns estÃ¡ticos.

### `src/GLPI_to_teams.py`
- **DescriÃ§Ã£o:** Script autÃ´nomo (daemon) para envio de notificaÃ§Ãµes ativas para o Microsoft Teams.
- **LÃ³gica Principal:**
  - Possui um loop infinito (`while True`) restrito a rodar apenas no **minuto 59** de cada hora, entre as **07h e 17h**, de **Segunda a Sexta-feira**.
  - Consome o mesmo mÃ©todo `GLPI.get_dashboard_data()` da web para garantir paridade de dados e envia as informaÃ§Ãµes formatadas em formato `MessageCard` via webhook.

---

## ðŸŽ¨ Frontend

### `src/templates/index.html`
- **DescriÃ§Ã£o:** Single Page Application (SPA) do Dashboard Web.
- **Tecnologias:** HTML5, Tailwind CSS (via CDN) e Vanilla JavaScript. Sem uso de bibliotecas legadas.
- **Design e UI/UX:** 
  - Segue estritamente as regras de UI/UX do `SKILL.md` (Glassmorphism, Dark Mode obrigatÃ³rio, tipografia moderna).
  - Possui um inovador **Sistema de Abas (Tabs)** dinÃ¢micas e Layout **Masonry** via CSS Columns, evitando que o empilhamento vertical prejudique o layout.
  - Apresenta interaÃ§Ãµes inteligentes como contadores em tempo real e tags de status nativamente coloridas de acordo com as chaves do GLPI.
- **LÃ³gica JS:** Faz pooling via `fetch` para a rota `/api/data`, controla auto-refresh dinÃ¢mico (5 a 60min) e gerencia os estados de carregamento.

---

## âš™ï¸ ConfiguraÃ§Ã£o e Infraestrutura

### `.env` / `.env.example`
- **DescriÃ§Ã£o:** ConfiguraÃ§Ã£o de credenciais crÃ­ticas e parÃ¢metros do sistema.
- **VariÃ¡veis Principais:** `GLPI_SERVER`, `GLPI_USERNAME`, `GLPI_PASSWORD` (Token de API), `TEAMS_WEBHOOK_URL`, `GLPI_DASHBOARD_USERS`.

### `docker-compose.yml` e `Dockerfile`
- **DescriÃ§Ã£o:** OrquestraÃ§Ã£o de infraestrutura como cÃ³digo (IaC).
- **ServiÃ§os:** Levanta o container Web (Flask na porta 5000) e o serviÃ§o `GLPI-notifier` que roda em background isolado no container.

### `deploy.sh`
- **DescriÃ§Ã£o:** Script bash utilitÃ¡rio focado em automaÃ§Ã£o de deploy, planejado para instÃ¢ncias Oracle Linux 8 na nuvem (OCI). Gerencia pulls, builds e monitoramento da stack.

---

## ðŸ“œ GovernanÃ§a e Regras

### `SKILL.md`
- **DescriÃ§Ã£o:** A "ConstituiÃ§Ã£o" arquitetural do projeto. Define regras rÃ­gidas sobre design (Tailwind CSS obrigatÃ³rio), seguranÃ§a (tratamento de erros) e padronizaÃ§Ãµes para qualquer futura atualizaÃ§Ã£o do cÃ³digo.

### `CHANGELOG.md`
- **DescriÃ§Ã£o:** Registro de alteraÃ§Ãµes aderente ao Semantic Versioning (SemVer). Rastreia todas as versÃµes em produÃ§Ã£o.

### `README.md`
- **DescriÃ§Ã£o:** DocumentaÃ§Ã£o oficial do projeto voltada para a instalaÃ§Ã£o, parametrizaÃ§Ã£o e uso geral da ferramenta pelos analistas.

