import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from parser import parse_excel, organize_data
from matching import apply_matching
from indici import calcola_indici_per_anni, indici_to_dataframe
from utils import (
    create_indici_chart, 
    create_comparison_chart, 
    display_indici_table, 
    create_dashboard_summary
)
from config import COLORS, MATCHING_TYPES

# Configurazione della pagina
st.set_page_config(
    page_title="BilanciSmart - Analisi Finanziaria per PMI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stile CSS personalizzato
st.markdown(
    f"""
    <style>
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {COLORS["primary"]};
    }}
    .stButton button {{
        background-color: {COLORS["primary"]};
        color: white;
    }}
    .stButton button:hover {{
        background-color: {COLORS["primary"]};
        opacity: 0.8;
    }}
    .sidebar .sidebar-content {{
        background-color: {COLORS["background"]};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Titolo dell'app
st.title("BilanciSmart")
st.markdown("### Analisi Finanziaria Automatica per PMI, Freelance e Consulenti")

# Sidebar per il caricamento del file e le opzioni
with st.sidebar:
    st.header("Carica il tuo bilancio")
    
    uploaded_file = st.file_uploader("Seleziona un file Excel (.xlsx)", type=["xlsx"])
    
    if uploaded_file is not None:
        st.success("File caricato con successo!")
        
        # Opzioni di analisi
        st.header("Opzioni di Analisi")
        
        # Selezione del foglio Excel
        sheet_name = st.text_input("Nome del foglio Excel (lascia vuoto per il primo foglio)", "")
        if sheet_name == "":
            sheet_name = 0
        
        # Tipo di matching
        matching_type = st.selectbox(
            "Metodo di matching delle voci",
            MATCHING_TYPES
        )
        
        # Pulsante per eseguire l'analisi
        analyze_button = st.button("Analizza Bilancio", type="primary")
        
        # Informazioni aggiuntive
        st.markdown("---")
        st.markdown("### Informazioni")
        st.markdown("""
        **BilanciSmart** analizza automaticamente i tuoi bilanci aziendali e calcola i principali indici finanziari.
        
        Carica un file Excel contenente:
        - Stato Patrimoniale
        - Conto Economico
        
        Per più anni (es. 2023, 2024)
        """)

# Contenuto principale
if 'analyzed_data' not in st.session_state:
    st.session_state.analyzed_data = None

# Se il pulsante di analisi è stato premuto
if 'uploaded_file' in locals() and uploaded_file is not None and 'analyze_button' in locals() and analyze_button:
    try:
        with st.spinner("Analisi in corso..."):
            # Parsing del file Excel
            df = parse_excel(uploaded_file, sheet_name)
            
            # Applicazione del matching
            df_matched = apply_matching(df, matching_type)
            
            # Organizzazione dei dati
            stato_patrimoniale, conto_economico = organize_data(df_matched)
            
            # Calcolo degli indici
            indici_anni = calcola_indici_per_anni(stato_patrimoniale, conto_economico)
            
            # Conversione in DataFrame
            df_indici = indici_to_dataframe(indici_anni)
            
            # Salva i risultati nella session state
            st.session_state.analyzed_data = {
                "df_raw": df,
                "df_matched": df_matched,
                "stato_patrimoniale": stato_patrimoniale,
                "conto_economico": conto_economico,
                "indici_anni": indici_anni,
                "df_indici": df_indici
            }
            
            st.success("Analisi completata con successo!")
    
    except Exception as e:
        st.error(f"Si è verificato un errore durante l'analisi: {str(e)}")

# Se ci sono dati analizzati, mostra i risultati
if st.session_state.analyzed_data is not None:
    data = st.session_state.analyzed_data
    df_indici = data["df_indici"]
    
    # Ottieni gli anni disponibili
    anni_disponibili = sorted(df_indici["Anno"].unique())
    
    if len(anni_disponibili) > 0:
        # Dashboard principale
        st.header("Dashboard")
        
        # Anno corrente e precedente per il riepilogo
        anno_corrente = max(anni_disponibili)
        anno_precedente = anno_corrente - 1 if anno_corrente - 1 in anni_disponibili else None
        
        # Mostra il riepilogo della dashboard
        create_dashboard_summary(df_indici, anno_corrente, anno_precedente)
        
        # Tabs per le diverse visualizzazioni
        tab1, tab2, tab3, tab4 = st.tabs(["Indici Principali", "Confronto Indici", "Tabella Completa", "Dati Grezzi"])
        
        with tab1:
            st.subheader("Indici Principali")
            
            # Seleziona l'indice da visualizzare
            indici_disponibili = sorted(df_indici["Indice"].unique())
            indice_selezionato = st.selectbox("Seleziona un indice", indici_disponibili)
            
            # Crea il grafico
            fig = create_indici_chart(df_indici, indice_selezionato)
            st.plotly_chart(fig, use_container_width=True)
            
            # Descrizione dell'indice
            from config import DESCRIZIONI_INDICI
            st.info(DESCRIZIONI_INDICI.get(indice_selezionato, ""))
        
        with tab2:
            st.subheader("Confronto Indici")
            
            # Seleziona gli indici da confrontare
            indici_selezionati = st.multiselect(
                "Seleziona gli indici da confrontare",
                indici_disponibili,
                default=indici_disponibili[:3] if len(indici_disponibili) >= 3 else indici_disponibili
            )
            
            if indici_selezionati:
                # Crea il grafico di confronto
                fig = create_comparison_chart(df_indici, indici_selezionati)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.subheader("Tabella Completa degli Indici")
            
            # Visualizza la tabella formattata
            display_indici_table(df_indici)
        
        with tab4:
            st.subheader("Dati Grezzi")
            
            # Mostra i dati originali
            st.markdown("### Dati Originali")
            st.dataframe(data["df_raw"])
            
            # Mostra i dati dopo il matching
            st.markdown("### Dati dopo il Matching")
            st.dataframe(data["df_matched"])
    else:
        st.warning("Non sono stati trovati dati validi per calcolare gli indici di bilancio.")
else:
    # Mostra le istruzioni iniziali
    st.markdown(
        f"""
        <div style="text-align: center; padding: 2rem; background-color: {COLORS['cardMuted']}; border-radius: 10px;">
            <h2 style="color: {COLORS['primary']};">Benvenuto in BilanciSmart</h2>
            <p style="font-size: 1.2rem; margin-bottom: 2rem;">
                Carica il tuo file Excel di bilancio per iniziare l'analisi finanziaria automatica.
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                <div style="background-color: white; padding: 1.5rem; border-radius: 8px; width: 200px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <h3 style="color: {COLORS['primary']};">1. Carica</h3>
                    <p>Carica il tuo file Excel di bilancio dalla barra laterale</p>
                </div>
                <div style="background-color: white; padding: 1.5rem; border-radius: 8px; width: 200px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <h3 style="color: {COLORS['primary']};">2. Analizza</h3>
                    <p>Seleziona le opzioni e clicca su "Analizza Bilancio"</p>
                </div>
                <div style="background-color: white; padding: 1.5rem; border-radius: 8px; width: 200px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <h3 style="color: {COLORS['primary']};">3. Visualizza</h3>
                    <p>Esplora i risultati attraverso grafici e tabelle interattive</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Mostra esempi di indici
    st.markdown("### Indici di Bilancio Calcolati")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div style="background-color: {COLORS['card']}; padding: 1rem; border-radius: 8px; height: 100%;">
                <h4 style="color: {COLORS['primary']};">Indici di Redditività</h4>
                <ul>
                    <li>ROE (Return on Equity)</li>
                    <li>ROI (Return on Investment)</li>
                    <li>ROS (Return on Sales)</li>
                    <li>EBITDA Margin</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div style="background-color: {COLORS['card']}; padding: 1rem; border-radius: 8px; height: 100%;">
                <h4 style="color: {COLORS['primary']};">Indici di Liquidità</h4>
                <ul>
                    <li>Indice di Liquidità</li>
                    <li>Indice di Indebitamento</li>
                    <li>Indice di Autonomia Finanziaria</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="background-color: {COLORS['card']}; padding: 1rem; border-radius: 8px; height: 100%;">
                <h4 style="color: {COLORS['primary']};">Indici di Efficienza</h4>
                <ul>
                    <li>Rotazione Capitale Investito</li>
                    <li>Indice di Copertura delle Immobilizzazioni</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )