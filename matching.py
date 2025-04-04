from typing import Dict, List, Tuple
import pandas as pd
import numpy as np
from rapidfuzz import fuzz, process
from config import VOCI_STATO_PATRIMONIALE, VOCI_CONTO_ECONOMICO

def fuzzy_match(voci_bilancio: List[str], voci_standard: List[str], threshold: int = 80) -> Dict[str, str]:
    """
    Esegue un matching fuzzy tra le voci del bilancio e le voci standard.
    
    Args:
        voci_bilancio: Lista delle voci presenti nel bilancio
        voci_standard: Lista delle voci standard da mappare
        threshold: Soglia minima di somiglianza (0-100)
        
    Returns:
        Dizionario con mapping {voce_bilancio: voce_standard}
    """
    mapping = {}
    
    for voce in voci_bilancio:
        # Trova la migliore corrispondenza
        match, score = process.extractOne(voce, voci_standard)
        
        # Applica solo se supera la soglia
        if score >= threshold:
            mapping[voce] = match
    
    return mapping

def embedding_match(voci_bilancio: List[str], voci_standard: List[str]) -> Dict[str, str]:
    """
    Esegue un matching semantico usando embedding con MiniLM.
    Questa è una versione semplificata che simula il comportamento.
    
    Args:
        voci_bilancio: Lista delle voci presenti nel bilancio
        voci_standard: Lista delle voci standard da mappare
        
    Returns:
        Dizionario con mapping {voce_bilancio: voce_standard}
    """
    # Placeholder per la versione completa che userebbe sentence-transformers
    # In una implementazione reale, qui si userebbero gli embedding di MiniLM
    
    # Per ora, usiamo un fuzzy match con soglia più bassa come simulazione
    return fuzzy_match(voci_bilancio, voci_standard, threshold=70)

def gpt_match(voci_bilancio: List[str], voci_standard: List[str]) -> Dict[str, str]:
    """
    Placeholder per il matching con GPT API.
    
    Args:
        voci_bilancio: Lista delle voci presenti nel bilancio
        voci_standard: Lista delle voci standard da mappare
        
    Returns:
        Dizionario con mapping {voce_bilancio: voce_standard}
    """
    # Questa è solo una simulazione, in una versione reale si userebbe l'API di OpenAI
    return fuzzy_match(voci_bilancio, voci_standard, threshold=60)

def apply_matching(df: pd.DataFrame, matching_type: str) -> pd.DataFrame:
    """
    Applica il matching selezionato al DataFrame.
    
    Args:
        df: DataFrame con i dati di bilancio
        matching_type: Tipo di matching da applicare
        
    Returns:
        DataFrame con le voci standardizzate
    """
    # Estrai le voci uniche dal DataFrame
    voci_bilancio = df["Voce"].unique().tolist()
    
    # Combina le voci standard
    voci_standard = VOCI_STATO_PATRIMONIALE + VOCI_CONTO_ECONOMICO
    
    # Seleziona il metodo di matching
    if "Fuzzy" in matching_type:
        mapping = fuzzy_match(voci_bilancio, voci_standard)
    elif "Embedding" in matching_type:
        mapping = embedding_match(voci_bilancio, voci_standard)
    elif "GPT" in matching_type:
        mapping = gpt_match(voci_bilancio, voci_standard)
    else:
        mapping = {}
    
    # Crea una copia del DataFrame
    df_matched = df.copy()
    
    # Aggiungi una colonna con le voci standardizzate
    df_matched["Voce_Standard"] = df_matched["Voce"].map(mapping)
    
    # Se una voce non ha corrispondenza, mantieni l'originale
    df_matched["Voce_Standard"].fillna(df_matched["Voce"], inplace=True)
    
    return df_matched