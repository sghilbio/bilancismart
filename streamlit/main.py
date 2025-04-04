import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
import sys
import os

# Aggiungi la directory principale al path per importare i moduli
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa i moduli necessari
from parser import parse_excel, organize_data
from matching import apply_matching
from indici import calcola_indici_per_anni, indici_to_dataframe
from config import COLORS, MATCHING_TYPES, DESCRIZIONI_INDICI

# Configurazione della pagina
st.set_page_config(
    page_title="BilanciSmart - Analisi Finanziaria",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titolo dell'app
st.title("BilanciSmart")
st.markdown("### Analisi Finanziaria Automatica per PMI, Freelance e Consulenti")

# Sidebar
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
        
        # Selezione del tipo di matching
        matching_type = st.selectbox(
            "Tipo di Matching",
            MATCHING_TYPES,
            index=0,
            help="Seleziona il tipo di matching per standardizzare le voci di bilancio"
        )
        
        # Pulsante per eseguire l'analisi
        analyze_button = st.button("Analizza Bilancio", type="primary")

# Contenuto principale
if 'analyzed_data' not in st.session_state:
    st.session_state.analyzed_data = None
    st.session_state.raw_data = None
    st.session_state.matched_data = None
    st.session_state.indici = None
    st.session_state.stato_patrimoniale = None
    st.session_state.conto_economico = None

# Mostra le istruzioni iniziali se non ci sono dati analizzati
if st.session_state.analyzed_data is None and not (uploaded_file is not None and analyze_button):
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem; background-color: #f0f2f6; border-radius: 10px;">
            <h2 style="color: #1F3B73;">Benvenuto in BilanciSmart</h2>
            <p style="font-size: 1.2rem; margin-bottom: 2rem;">
                Carica il tuo file Excel di bilancio per iniziare l'analisi finanziaria automatica.
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
                <div style="background-color: white; padding: 1.5rem; border-radius: 8px; width: 200px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <h3 style="color: #1F3B73;">1. Carica</h3>
                    <p>Carica il tuo file Excel di bilancio dalla barra laterale</p>
                </div>
                <div style="background-color: white; padding: 1.5rem; border-radius: 8px; width: 200px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <h3 style="color: #1F3B73;">2. Analizza</h3>
                    <p>Seleziona le opzioni e clicca su "Analizza Bilancio"</p>
                </div>
                <div style="background-color: white; padding: 1.5rem; border-radius: 8px; width: 200px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <h3 style="color: #1F3B73;">3. Visualizza</h3>
                    <p>Esplora i risultati attraverso grafici e tabelle interattive</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Elaborazione dei dati quando viene premuto il pulsante di analisi
if uploaded_file is not None and analyze_button:
    with st.spinner("Analisi del bilancio in corso..."):
        try:
            # Parsing del file Excel
            raw_data = parse_excel(uploaded_file, sheet_name)
            st.session_state.raw_data = raw_data
            
            # Applicazione del matching
            matched_data = apply_matching(raw_data, matching_type)
            st.session_state.matched_data = matched_data
            
            # Organizzazione dei dati
            stato_patrimoniale, conto_economico = organize_data(matched_data)
            st.session_state.stato_patrimoniale = stato_patrimoniale
            st.session_state.conto_economico = conto_economico
            
            # Calcolo degli indici
            indici = calcola_indici_per_anni(stato_patrimoniale, conto_economico)
            st.session_state.indici = indici
            
            # Conversione degli indici in DataFrame
            df_indici = indici_to_dataframe(indici)
            st.session_state.analyzed_data = df_indici
            
            st.success("Analisi completata con successo!")
        except Exception as e:
            st.error(f"Errore durante l'analisi: {str(e)}")

# Visualizzazione dei risultati se disponibili
if st.session_state.analyzed_data is not None:
    # Tabs per organizzare i risultati
    tab1, tab2, tab3, tab4 = st.tabs(["Dati Grezzi", "Dati Standardizzati", "Indici Finanziari", "Grafici"])
    
    # Tab 1: Dati Grezzi
    with tab1:
        st.header("Dati Grezzi")
        st.dataframe(st.session_state.raw_data, use_container_width=True)
        
        # Opzione per scaricare i dati grezzi
        csv = st.session_state.raw_data.to_csv(index=False)
        st.download_button(
            label="Scarica CSV",
            data=csv,
            file_name="dati_grezzi.csv",
            mime="text/csv"
        )
    
    # Tab 2: Dati Standardizzati
    with tab2:
        st.header("Dati Standardizzati")
        st.dataframe(st.session_state.matched_data, use_container_width=True)
        
        # Opzione per scaricare i dati standardizzati
        csv = st.session_state.matched_data.to_csv(index=False)
        st.download_button(
            label="Scarica CSV",
            data=csv,
            file_name="dati_standardizzati.csv",
            mime="text/csv"
        )
    
    # Tab 3: Indici Finanziari
    with tab3:
        st.header("Indici Finanziari")
        
        # Filtro per anno
        anni_disponibili = sorted(st.session_state.analyzed_data["Anno"].unique())
        anno_selezionato = st.selectbox("Seleziona Anno", anni_disponibili)
        
        # Filtra i dati per l'anno selezionato
        df_indici_anno = st.session_state.analyzed_data[st.session_state.analyzed_data["Anno"] == anno_selezionato]
        
        # Visualizza la tabella degli indici
        st.dataframe(df_indici_anno, use_container_width=True)
        
        # Opzione per scaricare gli indici
        csv = st.session_state.analyzed_data.to_csv(index=False)
        st.download_button(
            label="Scarica CSV",
            data=csv,
            file_name="indici_finanziari.csv",
            mime="text/csv"
        )
    
    # Tab 4: Grafici
    with tab4:
        st.header("Grafici degli Indici")
        
        # Selezione degli indici da visualizzare
        indici_disponibili = sorted(st.session_state.analyzed_data["Indice"].unique())
        indici_selezionati = st.multiselect(
            "Seleziona Indici da Visualizzare",
            indici_disponibili,
            default=indici_disponibili[:3]  # Default ai primi 3 indici
        )
        
        if indici_selezionati:
            # Filtra i dati per gli indici selezionati
            df_indici_grafico = st.session_state.analyzed_data[st.session_state.analyzed_data["Indice"].isin(indici_selezionati)]
            
            # Crea il grafico
            fig = px.line(
                df_indici_grafico,
                x="Anno",
                y="Valore",
                color="Indice",
                title="Andamento degli Indici Finanziari",
                labels={"Valore": "Valore (%)", "Anno": "Anno"},
                markers=True
            )
            
            # Personalizza il layout
            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=12),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            # Mostra il grafico
            st.plotly_chart(fig, use_container_width=True)
            
            # Mostra le descrizioni degli indici
            st.subheader("Descrizioni degli Indici")
            for indice in indici_selezionati:
                if indice in DESCRIZIONI_INDICI:
                    st.markdown(f"**{indice}**: {DESCRIZIONI_INDICI[indice]}")
                else:
                    st.markdown(f"**{indice}**: Descrizione non disponibile")
            
            # Opzione per scaricare il grafico come PNG
            img_bytes = fig.to_image(format="png")
            st.download_button(
                label="Scarica Grafico (PNG)",
                data=img_bytes,
                file_name="grafico_indici.png",
                mime="image/png"
            ) 