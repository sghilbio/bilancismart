# BilanciSmart

BilanciSmart è un'applicazione web per l'analisi finanziaria e il business planning, che permette di caricare bilanci in formato Excel, standardizzare i dati e calcolare indici finanziari.

## 🚀 Funzionalità

- Parsing automatico di file Excel di bilancio
- Calcolo indici finanziari
- Business Plan automatico
- Valutazione impresa
- Analisi SWOT
- Check revisore
- Dossier aziendale
- Sistema di inviti e onboarding
- Integrazione con Stripe per i pagamenti

## 🛠 Tecnologie

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React, TypeScript, Material-UI
- **Analisi Dati**: Pandas, NumPy, Plotly
- **UI Alternativa**: Streamlit
- **Container**: Docker, Docker Compose
- **Pagamenti**: Stripe

## 📦 Struttura del Progetto

Il progetto è diviso in due parti principali:

1. **Frontend**: Applicazione Next.js con Material-UI
2. **Backend**: API FastAPI con PostgreSQL

## 🚀 Getting Started

### Prerequisiti

- Docker e Docker Compose
- Node.js (per sviluppo frontend)
- Python 3.11+ (per sviluppo backend/streamlit)

### Installazione

1. Clona il repository:
   ```bash
   git clone https://github.com/yourusername/bilancismart.git
   cd bilancismart
   ```

2. Crea i file .env necessari:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   ```

3. Avvia i container:
   ```bash
   docker-compose up -d
   ```

4. Accedi alle applicazioni:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Streamlit: http://localhost:8501

### Sviluppo

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 📝 API Documentation

La documentazione dell'API è disponibile all'indirizzo:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contribuire

1. Fai un fork del progetto
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Committa le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Pusha sul branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è sotto licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

## Deploy

### Frontend (Vercel)

1. Crea un account su [Vercel](https://vercel.com)
2. Importa il repository GitHub
3. Configura le variabili d'ambiente:
   - `NEXT_PUBLIC_API_URL`: URL del backend (es. https://bilancismart-api.onrender.com)
4. Deploy

### Backend (Render)

1. Crea un account su [Render](https://render.com)
2. Crea un nuovo Web Service
3. Connetti il repository GitHub
4. Configura le variabili d'ambiente:
   - `DATABASE_URL`: URL del database PostgreSQL
   - `SECRET_KEY`: Chiave segreta per JWT
   - `BACKEND_CORS_ORIGINS`: Lista degli origini consentiti per CORS
5. Deploy

## Sviluppo Locale

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API

L'API è documentata all'indirizzo `/api/v1/docs` quando il backend è in esecuzione. 