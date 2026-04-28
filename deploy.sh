#!/bin/bash

# Cores para o terminal
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}==============================================${NC}"
echo -e "${YELLOW}    Iniciando Deploy do ARGO GLPI2Teams   ${NC}"
echo -e "${YELLOW}==============================================${NC}"

# 1. Checagem de ferramentas
if ! command -v git &> /dev/null; then
    echo -e "${RED}[Erro] git nÃ£o encontrado. No Oracle Linux, vocÃª pode instalÃ¡-lo com:${NC}"
    echo -e "${YELLOW}sudo yum install git -y${NC}"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo -e "${RED}[Erro] docker nÃ£o encontrado no servidor. No Oracle Linux, instale o service com:${NC}"
    echo -e "${YELLOW}sudo yum install docker -y${NC}"
    echo -e "${YELLOW}sudo systemctl start docker && sudo systemctl enable docker${NC}"
    exit 1
fi

COMPOSE_CMD="docker-compose"
if ! command -v docker-compose &> /dev/null; then
    if docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
    else
        echo -e "${RED}[Erro] docker-compose nÃ£o encontrado. Instale o plugin com:${NC}"
        echo -e "${YELLOW}sudo yum install docker-compose-plugin -y${NC}"
        echo -e "${RED}Ou caso queira o script binÃ¡rio avulso:${NC}"
        echo -e "${YELLOW}sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-Linux-aarch64\" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose${NC}"
        exit 1
    fi
fi

# VariÃ¡veis do Projeto
PROJECT_DIR="${HOME}/ARGO_glpi2teams"
REPO_URL="https://github.com/escti/ARGO_glpi2teams.git"

# 2. Atualizar cÃ³digo via Git
echo -e "\n${GREEN}[Passo 1/4] Preparando cÃ³digo fonte via Git...${NC}"

if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo -e "${YELLOW}RepositÃ³rio nÃ£o detectado em $PROJECT_DIR.${NC}"
    echo -e "${YELLOW}Realizando a primeira clonagem (git clone)...${NC}"
    git clone "$REPO_URL" "$PROJECT_DIR"
    if [ $? -ne 0 ]; then
        echo -e "${RED}[Erro] Falha ao clonar o projeto. Verifique o acesso do Github.${NC}"
        exit 1
    fi
    cd "$PROJECT_DIR"
else
    echo -e "${YELLOW}RepositÃ³rio jÃ¡ existente em $PROJECT_DIR. Sincronizando...${NC}"
    cd "$PROJECT_DIR"
    # ForÃ§a o branch principal a sincronizar ignorando eventuais conflitos locais
    git fetch origin
    git reset --hard origin/main
    git clean -fd
fi

echo -e "${GREEN}CÃ³digo devidamente posicionado e sincronizado!${NC}"

# 3. Validar arquivo .env
echo -e "\n${GREEN}[Passo 2/4] Validando variÃ¡veis de ambiente...${NC}"
if [ ! -f .env ]; then
    echo -e "${YELLOW}[Aviso] O arquivo .env nÃ£o foi encontrado. Copiando do .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}------------------------------------------------------------${NC}"
    echo -e "${RED}[AÃ§Ã£o NecessÃ¡ria] Por favor, edite o arquivo .env (ex: nano .env)${NC}"
    echo -e "${RED}preencha as URLs e senhas, e rode o ./deploy.sh novamente.${NC}"
    echo -e "${RED}------------------------------------------------------------${NC}"
    exit 1
else
    echo -e "${GREEN}Arquivo .env encontrado e vÃ¡lido.${NC}"
fi

# 4. Rebuild no Docker Compose
echo -e "\n${GREEN}[Passo 3/4] Reconstruindo containers...${NC}"
$COMPOSE_CMD down
$COMPOSE_CMD up -d --build

# Remove os lixos de build (camadas dangling) silenciosamente
docker image prune -f >/dev/null

# 5. Status
echo -e "\n${GREEN}[Passo 4/4] Verificando status dos serviÃ§os...${NC}"
sleep 3
$COMPOSE_CMD ps

echo -e "\n${YELLOW}==============================================${NC}"
echo -e "${GREEN} Deploy Finalizado com Sucesso! ${NC}"
echo -e "${YELLOW}==============================================${NC}"

