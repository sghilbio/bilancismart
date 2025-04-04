#!/bin/bash

# Colori per i messaggi
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== BilanciSmart Deployment Script ===${NC}"
echo "Questo script ti aiuterà a deployare BilanciSmart su Vercel e Render."
echo ""

# Verifica che Git sia installato
if ! command -v git &> /dev/null; then
    echo -e "${RED}Git non è installato. Installa Git e riprova.${NC}"
    exit 1
fi

# Verifica che Node.js sia installato
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js non è installato. Installa Node.js e riprova.${NC}"
    exit 1
fi

# Verifica che npm sia installato
if ! command -v npm &> /dev/null; then
    echo -e "${RED}npm non è installato. Installa npm e riprova.${NC}"
    exit 1
fi

# Verifica che Python sia installato
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 non è installato. Installa Python 3 e riprova.${NC}"
    exit 1
fi

# Verifica che pip sia installato
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 non è installato. Installa pip3 e riprova.${NC}"
    exit 1
fi

# Verifica che il repository sia inizializzato
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Inizializzazione del repository Git...${NC}"
    git init
    git add .
    git commit -m "Initial commit"
fi

# Verifica che il repository sia collegato a GitHub
if ! git remote | grep -q "origin"; then
    echo -e "${YELLOW}Il repository non è collegato a GitHub.${NC}"
    echo "Per favore, crea un repository su GitHub e collega il repository locale."
    echo "Puoi farlo con i seguenti comandi:"
    echo "git remote add origin <URL_DEL_REPOSITORY>"
    echo "git push -u origin main"
    exit 1
fi

# Verifica che il frontend sia configurato correttamente
if [ ! -f "frontend/.env.local" ]; then
    echo -e "${YELLOW}Creazione del file .env.local per il frontend...${NC}"
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > frontend/.env.local
fi

# Verifica che il backend sia configurato correttamente
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}Creazione del file .env per il backend...${NC}"
    echo "PROJECT_NAME=BilanciSmart API" > backend/.env
    echo "VERSION=1.0.0" >> backend/.env
    echo "API_V1_STR=/api/v1" >> backend/.env
    echo "BACKEND_CORS_ORIGINS=[\"http://localhost:3000\",\"https://bilancismart.vercel.app\"]" >> backend/.env
fi

# Installa le dipendenze del frontend
echo -e "${YELLOW}Installazione delle dipendenze del frontend...${NC}"
cd frontend
npm install
cd ..

# Installa le dipendenze del backend
echo -e "${YELLOW}Installazione delle dipendenze del backend...${NC}"
cd backend
pip install -r requirements.txt
cd ..

echo -e "${GREEN}Setup completato!${NC}"
echo ""
echo -e "${YELLOW}Per deployare su Vercel:${NC}"
echo "1. Crea un account su Vercel (https://vercel.com)"
echo "2. Importa il repository GitHub"
echo "3. Configura le variabili d'ambiente:"
echo "   - NEXT_PUBLIC_API_URL: URL del backend (es. https://bilancismart-api.onrender.com)"
echo "4. Deploy"
echo ""
echo -e "${YELLOW}Per deployare su Render:${NC}"
echo "1. Crea un account su Render (https://render.com)"
echo "2. Crea un nuovo Web Service"
echo "3. Connetti il repository GitHub"
echo "4. Configura le variabili d'ambiente:"
echo "   - DATABASE_URL: URL del database PostgreSQL"
echo "   - SECRET_KEY: Chiave segreta per JWT"
echo "   - BACKEND_CORS_ORIGINS: Lista degli origini consentiti per CORS"
echo "5. Deploy"
echo ""
echo -e "${GREEN}Buon deploy!${NC}" 