import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List
import streamlit as st
from config import COLORS, DESCRIZIONI_INDICI

def format_currency(value):
    """Formatta un valore come valuta"""
    if pd.isna(value):
        return "N/D"
    return f"€ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_percentage(value):
    """Formatta un valore come percentuale"""
    if pd.isna(value):
        return "N/D"
    return f"{value:.2f}%"

def format_ratio(value):
    """Formatta un valore come rapporto"""
    if pd.isna(value):
        return "N/D"
    return f"{value:.2f}"

def get_formatter(indice):
    """Restituisce la funzione di formattazione appropriata per l'indice"""
    if indice in ["ROE", "ROI", "ROS", "EBITDA Margin", "Indice di Autonomia Finanziaria"]:
        return format_percentage
    elif indice in ["Indice di Liquidità", "Indice di Indebitamento", 
                   "Rotazione Capitale Investito", "Indice di Copertura delle Immobilizzazioni"]:
        return format_ratio
    else:
        return format_currency

def create_indici_chart(df_indici, indice):
    """Crea un grafico per un indice specifico"""
    df_filtered = df_indici[df_indici["Indice"] == indice]
    
    # Determina il colore in base al tipo di indice
    if indice in ["ROE", "ROI", "ROS", "EBITDA Margin", "Indice di Autonomia Finanziaria", 
                 "Indice di Liquidità", "Indice di Copertura delle Immobilizzazioni"]:
        # Indici dove valori più alti sono generalmente migliori
        color = COLORS["secondary"]
    else:
        # Indici dove valori più bassi sono generalmente migliori
        color = COLORS["accent"]
    
    fig = px.bar(
        df_filtered, 
        x="Anno", 
        y="Valore",
        title=indice,
        color_discrete_sequence=[color]
    )
    
    # Aggiungi linea di tendenza
    if len(df_filtered) > 1:
        fig.add_trace(
            go.Scatter(
                x=df_filtered["Anno"],
                y=df_filtered["Valore"],
                mode="lines+markers",
                name="Trend",
                line=dict(color=COLORS["primary"], width=2)
            )
        )
    
    # Formatta l'asse y in base al tipo di indice
    formatter = get_formatter(indice)
    if formatter == format_percentage:
        fig.update_layout(yaxis_ticksuffix="%")
    
    # Personalizza il layout
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="",
            gridcolor="rgba(0,0,0,0.1)"
        ),
        yaxis=dict(
            title="",
            gridcolor="rgba(0,0,0,0.1)"
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_comparison_chart(df_indici, indici_selezionati, anno=None):
    """Crea un grafico di confronto tra diversi indici per un anno specifico o tra anni"""
    if anno:
        # Confronto tra indici per un anno specifico
        df_filtered = df_indici[(df_indici["Anno"] == anno) & (df_indici["Indice"].isin(indici_selezionati))]
        
        fig = px.bar(
            df_filtered,
            x="Indice",
            y="Valore",
            title=f"Confronto Indici - Anno {anno}",
            color="Indice",
            color_discrete_sequence=[COLORS["primary"], COLORS["secondary"], COLORS["accent"]]
        )
    else:
        # Confronto di un indice tra anni
        df_filtered = df_indici[df_indici["Indice"].isin(indici_selezionati)]
        
        fig = px.line(
            df_filtered,
            x="Anno",
            y="Valore",
            color="Indice",
            title="Confronto Indici nel Tempo",
            markers=True,
            color_discrete_sequence=[COLORS["primary"], COLORS["secondary"], COLORS["accent"]]
        )
    
    # Personalizza il layout
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            title="",
            gridcolor="rgba(0,0,0,0.1)"
        ),
        yaxis=dict(
            title="",
            gridcolor="rgba(0,0,0,0.1)"
        ),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def display_indici_table(df_indici):
    """Visualizza una tabella formattata con gli indici di bilancio"""
    # Pivot della tabella per avere gli indici come righe e gli anni come colonne
    df_pivot = df_indici.pivot(index="Indice", columns="Anno", values="Valore")
    
    # Crea una tabella HTML formattata
    html = "<table class='indici-table'>"
    
    # Intestazione
    html += "<tr><th>Indice</th>"
    for anno in df_pivot.columns:
        html += f"<th>{anno}</th>"
    html += "<th>Descrizione</th></tr>"
    
    # Righe
    for indice in df_pivot.index:
        html += f"<tr><td>{indice}</td>"
        
        formatter = get_formatter(indice)
        for anno in df_pivot.columns:
            valore = df_pivot.loc[indice, anno]
            html += f"<td>{formatter(valore)}</td>"
        
        # Aggiungi descrizione
        descrizione = DESCRIZIONI_INDICI.get(indice, "")
        html += f"<td class='descrizione'>{descrizione}</td></tr>"
    
    html += "</table>"
    
    # Stile CSS per la tabella
    st.markdown(
        f"""
        <style>
        .indici-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .indici-table th, .indici-table td {{
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid {COLORS["muted"]};
        }}
        .indici-table th {{
            background-color: {COLORS["primary"]};
            color: white;
        }}
        .indici-table tr:nth-child(even) {{
            background-color: {COLORS["cardMuted"]};
        }}
        .indici-table .descrizione {{
            font-size: 12px;
            color: {COLORS["muted"]};
            max-width: 300px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(html, unsafe_allow_html=True)

def create_dashboard_summary(df_indici, anno_corrente, anno_precedente=None):
    """Crea un riepilogo dashboard con i principali indicatori"""
    # Filtra per l'anno corrente
    df_current = df_indici[df_indici["Anno"] == anno_corrente]
    
    # Crea un dizionario degli indici
    indici_current = {row["Indice"]: row["Valore"] for _, row in df_current.iterrows()}
    
    # Se c'è un anno precedente, calcola le variazioni
    variazioni = {}
    if anno_precedente:
        df_prev = df_indici[df_indici["Anno"] == anno_precedente]
        indici_prev = {row["Indice"]: row["Valore"] for _, row in df_prev.iterrows()}
        
        for indice, valore in indici_current.items():
            if indice in indici_prev and not pd.isna(valore) and not pd.isna(indici_prev[indice]) and indici_prev[indice] != 0:
                variazioni[indice] = ((valore / indici_prev[indice]) - 1) * 100
            else:
                variazioni[indice] = np.nan
    
    # Crea il layout della dashboard
    cols = st.columns(3)
    
    # Indici principali da mostrare
    indici_principali = ["ROE", "ROI", "Indice di Liquidità"]
    
    for i, indice in enumerate(indici_principali):
        with cols[i]:
            valore = indici_current.get(indice, np.nan)
            formatter = get_formatter(indice)
            
            # Determina il colore in base alla variazione
            if indice in variazioni and not pd.isna(variazioni[indice]):
                var = variazioni[indice]
                # Per alcuni indici, valori più bassi sono migliori
                if indice in ["Indice di Indebitamento"]:
                    var = -var
                
                if var > 0:
                    color = COLORS["secondary"]
                    icon = "↑"
                elif var < 0:
                    color = COLORS["accent"]
                    icon = "↓"
                else:
                    color = COLORS["muted"]
                    icon = "→"
                
                var_text = f"{icon} {var:.1f}%"
            else:
                color = COLORS["muted"]
                var_text = ""
            
            st.markdown(
                f"""
                <div style="text-align: center; padding: 15px; background-color: {COLORS['card']}; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <h3 style="margin: 0; color: {COLORS['primary']};">{indice}</h3>
                    <p style="font-size: 24px; font-weight: bold; margin: 10px 0; color: {COLORS['foreground']};">{formatter(valore)}</p>
                    <p style="margin: 0; color: {color};">{var_text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )