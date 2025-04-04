# Configurazione colori (convertiti da Tailwind per Streamlit)
COLORS = {
    "primary": "#1F3B73",      # Blu Navy – affidabile, professionale
    "secondary": "#88B04B",    # Verde Salvia – crescita, positività
    "accent": "#E57373",       # Rosso Soft – per warning, negativi
    "background": "#F5F6FA",   # Grigio chiaro – sfondo neutro
    "foreground": "#2C3E50",   # Grigio scuro – testi principali
    "muted": "#AAB2BD",        # Grigio medio – testi secondari
    "card": "#FFFFFF",         # Bianco – card e contenuti
    "cardMuted": "#FDF6EC",    # Beige sabbia – per sezioni soft
}

# Voci di bilancio standard per il matching
VOCI_STATO_PATRIMONIALE = [
    "Totale Attivo", "Attivo Circolante", "Immobilizzazioni", "Patrimonio Netto", 
    "Passività Correnti", "Passività Consolidate", "Totale Passivo", 
    "Disponibilità Liquide", "Crediti", "Rimanenze", "Debiti a Breve", "Debiti a Lungo"
]

VOCI_CONTO_ECONOMICO = [
    "Ricavi", "Costi della Produzione", "EBITDA", "Ammortamenti e Svalutazioni", 
    "EBIT", "Oneri Finanziari", "Utile Ante Imposte", "Imposte", "Utile Netto"
]

# Descrizioni degli indici di bilancio
DESCRIZIONI_INDICI = {
    "ROE": "Return on Equity: misura la redditività del capitale proprio",
    "ROI": "Return on Investment: misura la redditività del capitale investito",
    "ROS": "Return on Sales: misura la redditività delle vendite",
    "Indice di Liquidità": "Misura la capacità dell'azienda di far fronte agli impegni a breve termine",
    "Indice di Indebitamento": "Misura il rapporto tra capitale di terzi e capitale proprio",
    "EBITDA Margin": "Misura la redditività operativa lorda in percentuale sui ricavi",
    "Rotazione Capitale Investito": "Misura l'efficienza nell'utilizzo del capitale investito",
    "Indice di Copertura delle Immobilizzazioni": "Misura la capacità dell'azienda di finanziare le immobilizzazioni con capitale proprio",
    "Indice di Autonomia Finanziaria": "Misura il grado di indipendenza finanziaria dell'azienda"
}

# Tipi di matching disponibili
MATCHING_TYPES = ["Fuzzy (Base)", "Embedding Semantico (Intermedio)", "GPT API (Premium)"]