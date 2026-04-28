# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-04-27
### Changed
- **ReestruturaÃ§Ã£o Arquitetural**: CÃ³digo-fonte migrado para a pasta `src/` e arquivos legados movidos para `docs/`, seguindo as melhores prÃ¡ticas do ecossistema Python.
- AtualizaÃ§Ã£o do `Dockerfile` e `docker-compose.yml` para mapear os novos caminhos do backend.
- SimplificaÃ§Ã£o da esteira de deploy no `README.md` (One-liner install).
- ReforÃ§o do prompt de IA no `FILE_MAP.md` exigindo o cumprimento estrito do `SKILL.md`.

## [0.4.2] - 2026-04-27
### Fixed
- ReordenaÃ§Ã£o da "Fila DBA Urgente" para priorizar os tickets pelo Tempo de ResoluÃ§Ã£o (SLA), do mais crÃ­tico (menor tempo) para o menos crÃ­tico.

## [0.4.1] - 2026-04-27
### Fixed
- CorreÃ§Ã£o de sobreposiÃ§Ã£o na fila "Aguardando Atendimento" com a exclusÃ£o explÃ­cita do status `PENDENTE EXTERNO`.
- Ajuste na fila "SLA CrÃ­tico (< 1h)" limitando o escopo estritamente aos status `Em atendimento` e `Aguardando atendimento`.
- PadronizaÃ§Ã£o da ordenaÃ§Ã£o das filas ("Aguardando Atendimento", "Sem InteraÃ§Ã£o" e "Projetos Ativos") para `Status`, `Tempo de resoluÃ§Ã£o` (SLA) e Data de AtualizaÃ§Ã£o (`updated`).

## [0.4.0] - 2026-04-19
### Added
- SeparaÃ§Ã£o de Projetos: Criada uma query especÃ­fica para projetos (TIC e GPM), excluindo-os nativamente das filas de sustentaÃ§Ã£o diÃ¡ria via JQL `project IN`.
- Novo Layout UX via Sistema de Abas (Tabs): As filas foram divididas em 3 abas (SustentaÃ§Ã£o & DBA, Projetos Ativos, Finalizados).
- Layout Masonry (Colunas Fluidas): A Aba de SustentaÃ§Ã£o teve sua grid ajustada para colunas independentes para evitar buracos verticais no agrupamento dos cards.
- Status DinÃ¢mico e Colorido: ExtraÃ§Ã£o do `statusCategory` do GLPI (new, indeterminate, done) renderizando cores dinÃ¢micas para o badge do status do chamado na tela.
- Contadores dinÃ¢micos ao lado do tÃ­tulo de cada aba mostrando a contagem de tickets daquela fila em tempo real.

### Changed
- RefatoraÃ§Ã£o do campo de UsuÃ¡rio (GLPI User): O sistema agora recorta apenas a extensÃ£o (domÃ­nio) e carrega o nome do usuÃ¡rio completo automaticamente ao abrir.
- O card de "Fila DBA Urgente" perdeu sua coluna lateral fixa e foi internalizado na primeira posiÃ§Ã£o da Aba SustentaÃ§Ã£o.

## [0.3.0] - 2026-04-19
### Added
- Colapsabilidade nos agrupamentos de chamados (Cards) via clique no tÃ­tulo com transiÃ§Ã£o de Ã­cones (chevron).
- Textos orientativos (helper texts/tooltips) adicionados aos botÃµes de sincronia e auto-refresh.
- Dropdown dinÃ¢mico para controle do tempo de Auto-refresh (5m, 10m, 15m, 30m, 60m).
- 5Âº Card: "Chamados Finalizados (Este MÃªs)".

### Changed
- RefatoraÃ§Ã£o do dropdown de SeleÃ§Ã£o de UsuÃ¡rio (VisÃ£o) para um input de texto livre e dinÃ¢mico, suportando atÃ© 50 caracteres para e-mails longos corporativos.
- Queries JQL atualizadas para alinhar com os "Custom Fields" legados do GLPI Corporativo.

## [0.2.0] - 2026-04-13
### Changed
- RefatoraÃ§Ã£o completa da UI: SubstituiÃ§Ã£o total do Bootstrap 5 pelo **Tailwind CSS**.
- ImplementaÃ§Ã£o de Dark Mode nativo do Tailwind.
- Melhoria na performance de carregamento via otimizaÃ§Ã£o de CSS utilitÃ¡rio.
- AtualizaÃ§Ã£o do sistema de Grid e Componentes para maior flexibilidade responsiva.

## [0.1.0] - 2026-04-13
### Added
- InicializaÃ§Ã£o do sistema sob nova arquitetura de Controle de Qualidade (`SKILL.md`) e Controle de VersÃ£o (`CHANGELOG.md`).
- ImplementaÃ§Ã£o unificada do rodapÃ© (Footer) no Dashboard WEB contendo a respectiva versÃ£o semÃ¢ntica de interface.
- ConsolidaÃ§Ã£o do backend para validaÃ§Ã£o das chaves do GLPI com suporte visual a Dark Theme reativo.

