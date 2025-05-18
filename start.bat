@echo off
echo Iniciando a aplicacao WhatsApp AGI...

REM Verifica se o Docker esta instalado
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo Docker nao encontrado. Por favor, instale o Docker primeiro.
    pause
    exit /b
)

REM Verifica se o arquivo .env existe
if not exist .env (
    echo Arquivo .env nao encontrado. Criando a partir do exemplo...
    copy .env.example .env
    echo Por favor, configure suas variaveis no arquivo .env
)

REM Cria a pasta waha-data se nao existir
if not exist waha-data mkdir waha-data

REM Inicia os containers
echo Iniciando containers Docker...
docker-compose up --build

pause 