#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Iniciando setup do WAHA...${NC}"

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 não encontrado. Por favor, instale o Python primeiro.${NC}"
    exit 1
fi

# Instala dependências necessárias
echo -e "${YELLOW}Instalando dependências...${NC}"
pip install requests rich qrcode

# Verifica se o Docker está rodando
if ! docker ps &> /dev/null; then
    echo -e "${RED}Docker não está rodando. Iniciando containers...${NC}"
    docker-compose up -d
    sleep 5
fi

# Verifica se os serviços estão rodando
if ! curl -s http://localhost:3000/api/server/status > /dev/null; then
    echo -e "${RED}WAHA não está rodando. Execute ./start.sh primeiro.${NC}"
    exit 1
fi

# Executa o script de setup
python3 scripts/setup_waha.py

# Verifica se a execução foi bem sucedida
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Setup concluído com sucesso!${NC}"
else
    echo -e "${RED}Erro durante o setup.${NC}"
    exit 1
fi 