---
name: ARGO glpi2teams Base Architecture
description: Regras intransigentes de UI/UX, arquitetura de cÃ³digo e release management para o monitor de filas do GLPI e notificador de Teams.
---

# 1. Regras ImutÃ¡veis de UI/UX
- **Design System ObrigatÃ³rio**: Abordagem "Glassmorphism" com suporte nativo a transiÃ§Ãµes fluidas e micro-animaÃ§Ãµes.
- **Dark Mode**: Modo Escuro Ã© obrigatÃ³rio e padrÃ£o para novas implementaÃ§Ãµes. NÃ£o crie componentes apenas na versÃ£o clara.
- **Acessibilidade e Layout**: 
  - Restringir barras de rolagem em excesso (ocultar nativas ou utilizar track customizada extra fina e transparente).
  - Responsividade Mobile-first (os cards devem empilhar graciosamente e nÃ£o causar scroll horizontal em tabelas ou eixos X locais).
- **Paleta de Cores**: 
  - Proibido usar red/blue genÃ©ricos de browser (ex: `red`); obrigatÃ³rio o uso de gradients definidos no `:root` (Ex: `var(--accent-blue)` e `var(--accent-purple)`).
  - Alertas CrÃ­ticos mantÃªm tons inspirados em `rgba(255,8,68,0.2)`.

# 2. Regras de CÃ³digo 
- **Frontend / Frameworks**: O padrÃ£o moderno, seguro e obrigatÃ³rio Ã© o **Tailwind CSS**. Utility-first classes devem ser usadas para todo o layout, garantindo consistÃªncia, performance e facilidade de manutenÃ§Ã£o. O uso de Bootstrap ou outros frameworks legados estÃ¡ proibido para novas implementaÃ§Ãµes e refatoraÃ§Ãµes.
- **Backend / Python**: Todo cÃ³digo backend deve possuir `try/catch` explÃ­citos e registrar as saÃ­das no sistema de logging base. 

# 3. Regras de Controle de VersÃ£o e Deployment
- **Changelog Strict**: Em prol da rastreabilidade (`CHANGELOG.md`), qualquer novo CSS, fix de syntax ou tela obriga um version bump seguindo SemVer. A versÃ£o inicial do produto de testes Ã© a `v0.1.0`. Apenas a versÃ£o de produÃ§Ã£o final atingirÃ¡ `v1.0.0`.
- **Global Footer Version**: A variÃ¡vel de versÃ£o **DEVE** estar ancorada no UI atual e visÃ­vel publicamente no rodapÃ© da aplicaÃ§Ã£o web.

