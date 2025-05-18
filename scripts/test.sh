#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Verificando dependências para teste...${NC}"

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 não encontrado. Por favor, instale o Python primeiro.${NC}"
    exit 1
fi

# Instala dependências necessárias
echo -e "${YELLOW}Instalando dependências de teste...${NC}"
pip install requests rich

# Verifica se os serviços estão rodando
if ! curl -s http://localhost:3000/api/health > /dev/null; then
    echo -e "${RED}WAHA não está rodando. Execute ./start.sh primeiro.${NC}"
    exit 1
fi

if ! curl -s http://localhost:8000/docs > /dev/null; then
    echo -e "${RED}API não está rodando. Execute ./start.sh primeiro.${NC}"
    exit 1
fi

# Executa os testes
echo -e "${GREEN}Iniciando testes de envio...${NC}"
python3 scripts/test_messages.py

# Verifica se a execução foi bem sucedida
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Testes concluídos com sucesso!${NC}"
else
    echo -e "${RED}Erro durante os testes.${NC}"
    exit 1
fi 