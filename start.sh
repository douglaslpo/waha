#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Iniciando serviços...${NC}"

# Verifica Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker não encontrado${NC}"
    exit 1
fi

# Cria diretórios necessários
mkdir -p waha-data data

# Para containers existentes
docker-compose down

# Inicia containers
docker-compose up -d

# Aguarda o WAHA iniciar
echo -e "${YELLOW}Aguardando WAHA iniciar...${NC}"
sleep 5

# Cria a sessão default
echo -e "${YELLOW}Criando sessão WhatsApp...${NC}"
curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"name": "default"}' \
    http://localhost:3000/api/sessions/start

# Instruções para o usuário
echo -e "\n${GREEN}Serviços iniciados!${NC}"
echo -e "${YELLOW}Para conectar o WhatsApp:${NC}"
echo -e "1. Acesse: http://localhost:3000"
echo -e "2. Escaneie o QR Code com seu WhatsApp"
echo -e "3. Aguarde a conexão ser estabelecida"
echo -e "\n${GREEN}Outros serviços:${NC}"
echo -e "API Docs: http://localhost:8000/docs"

# Exibe os logs para acompanhar a conexão
echo -e "\n${YELLOW}Exibindo logs do WAHA...${NC}"
docker-compose logs -f waha 