from typing import Dict, List, Tuple
import pandas as pd
import numpy as np

def calcola_indici(stato_patrimoniale: Dict[str, float], conto_economico: Dict[str, float]) -> Dict[str, float]:
    """
    Calcola gli indici di bilancio a partire dai dati di Stato Patrimoniale e Conto Economico.
    
    Args:
        stato_patrimoniale: Dizionario con le voci dello Stato Patrimoniale
        conto_economico: Dizionario con le voci del Conto Economico
        
    Returns:
        Dizionario con gli indici calcolati
    """
    indici = {}
    
    # Estrai i valori necessari con gestione dei casi in cui mancano
    # Stato Patrimoniale
    totale_attivo = stato_patrimoniale.get("Totale Attivo", 0)
    patrimonio_netto = stato_patrimoniale.get("Patrimonio Netto", 0)
    attivo_circolante = stato_patrimoniale.get("Attivo Circolante", 0)
    immobilizzazioni = stato_patrimoniale.get("Immobilizzazioni", 0)
    passivita_correnti = stato_patrimoniale.get("Passività Correnti", 0)
    passivita_consolidate = stato_patrimoniale.get("Passività Consolidate", 0)
    disponibilita_liquide = stato_patrimoniale.get("Disponibilità Liquide", 0)
    crediti = stato_patrimoniale.get("Crediti", 0)
    
    # Conto Economico
    ricavi = conto_economico.get("Ricavi", 0)
    ebitda = conto_economico.get("EBITDA", 0)
    ebit = conto_economico.get("EBIT", 0)
    utile_netto = conto_economico.get("Utile Netto", 0)
    
    # Calcolo degli indici
    # ROE (Return on Equity)
    if patrimonio_netto != 0:
        indici["ROE"] = (utile_netto / patrimonio_netto) * 100
    else:
        indici["ROE"] = np.nan
    
    # ROI (Return on Investment)
    if totale_attivo != 0:
        indici["ROI"] = (ebit / totale_attivo) * 100
    else:
        indici["ROI"] = np.nan
    
    # ROS (Return on Sales)
    if ricavi != 0:
        indici["ROS"] = (ebit / ricavi) * 100
    else:
        indici["ROS"] = np.nan
    
    # Indice di Liquidità
    if passivita_correnti != 0:
        indici["Indice di Liquidità"] = (disponibilita_liquide + crediti) / passivita_correnti
    else:
        indici["Indice di Liquidità"] = np.nan
    
    # Indice di Indebitamento
    if patrimonio_netto != 0:
        indici["Indice di Indebitamento"] = (passivita_correnti + passivita_consolidate) / patrimonio_netto
    else:
        indici["Indice di Indebitamento"] = np.nan
    
    # EBITDA Margin
    if ricavi != 0:
        indici["EBITDA Margin"] = (ebitda / ricavi) * 100
    else:
        indici["EBITDA Margin"] = np.nan
    
    # Rotazione Capitale Investito
    if totale_attivo != 0:
        indici["Rotazione Capitale Investito"] = ricavi / totale_attivo
    else:
        indici["Rotazione Capitale Investito"] = np.nan
    
    # Indice di Copertura delle Immobilizzazioni
    if immobilizzazioni != 0:
        indici["Indice di Copertura delle Immobilizzazioni"] = patrimonio_netto / immobilizzazioni
    else:
        indici["Indice di Copertura delle Immobilizzazioni"] = np.nan
    
    # Indice di Autonomia Finanziaria
    if totale_attivo != 0:
        indici["Indice di Autonomia Finanziaria"] = (patrimonio_netto / totale_attivo) * 100
    else:
        indici["Indice di Autonomia Finanziaria"] = np.nan
    
    return indici

def calcola_indici_per_anni(stato_patrimoniale_anni: Dict[int, Dict[str, float]], 
                           conto_economico_anni: Dict[int, Dict[str, float]]) -> Dict[int, Dict[str, float]]:
    """
    Calcola gli indici di bilancio per tutti gli anni disponibili.
    
    Args:
        stato_patrimoniale_anni: Dizionario con i dati dello Stato Patrimoniale per ogni anno
        conto_economico_anni: Dizionario con i dati del Conto Economico per ogni anno
        
    Returns:
        Dizionario con gli indici calcolati per ogni anno
    """
    indici_anni = {}
    
    # Calcola gli indici per ogni anno
    for anno in stato_patrimoniale_anni.keys():
        if anno in conto_economico_anni:
            indici_anni[anno] = calcola_indici(
                stato_patrimoniale_anni[anno],
                conto_economico_anni[anno]
            )
    
    return indici_anni

def indici_to_dataframe(indici_anni: Dict[int, Dict[str, float]]) -> pd.DataFrame:
    """
    Converte il dizionario degli indici in un DataFrame.
    
    Args:
        indici_anni: Dizionario con gli indici calcolati per ogni anno
        
    Returns:
        DataFrame con gli indici
    """
    # Crea una lista di dizionari per ogni anno
    data = []
    for anno, indici in indici_anni.items():
        for indice, valore in indici.items():
            data.append({
                "Anno": anno,
                "Indice": indice,
                "Valore": valore
            })
    
    # Crea il DataFrame
    df = pd.DataFrame(data)
    
    return df