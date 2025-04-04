import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import re

def parse_excel(file, sheet_name=0) -> pd.DataFrame:
    """
    Legge un file Excel e lo converte in un formato tabellare standard.
    
    Args:
        file: File Excel caricato
        sheet_name: Nome o indice del foglio da leggere
        
    Returns:
        DataFrame con colonne: Voce, Anno, Valore
    """
    try:
        # Leggi il file Excel
        df_raw = pd.read_excel(file, sheet_name=sheet_name)
        
        # Rimuovi righe e colonne completamente vuote
        df_raw = df_raw.dropna(how='all').dropna(axis=1, how='all')
        
        # Identifica la prima colonna come quella delle voci
        voci_col = df_raw.columns[0]
        
        # Identifica le colonne degli anni (assumiamo che siano numeri o stringhe che contengono anni)
        anni_cols = []
        for col in df_raw.columns[1:]:
            # Cerca un pattern di anno (4 cifre) nel nome della colonna
            if isinstance(col, str) and re.search(r'\b20\d{2}\b', col):
                anni_cols.append(col)
            # Se la colonna è un numero intero tra 2000 e 2100
            elif isinstance(col, (int, float)) and 2000 <= col <= 2100:
                anni_cols.append(col)
        
        # Se non abbiamo trovato colonne di anni, prendiamo tutte le colonne numeriche
        if not anni_cols:
            anni_cols = [col for col in df_raw.columns[1:] if pd.api.types.is_numeric_dtype(df_raw[col])]
        
        # Converti in formato lungo (Voce, Anno, Valore)
        result_data = []
        for _, row in df_raw.iterrows():
            voce = row[voci_col]
            if pd.isna(voce) or not isinstance(voce, str):
                continue
                
            for anno_col in anni_cols:
                valore = row[anno_col]
                if pd.notna(valore):
                    # Estrai l'anno dalla colonna se è una stringa
                    if isinstance(anno_col, str):
                        match = re.search(r'\b(20\d{2})\b', anno_col)
                        anno = match.group(1) if match else anno_col
                    else:
                        anno = int(anno_col)
                    
                    result_data.append({
                        "Voce": voce.strip(),
                        "Anno": anno,
                        "Valore": float(valore)
                    })
        
        # Crea il DataFrame risultante
        result_df = pd.DataFrame(result_data)
        
        return result_df
    
    except Exception as e:
        raise Exception(f"Errore nel parsing del file Excel: {str(e)}")

def identify_statement_type(voce: str) -> str:
    """
    Identifica se una voce appartiene allo Stato Patrimoniale o al Conto Economico.
    
    Args:
        voce: Nome della voce di bilancio
        
    Returns:
        "SP" per Stato Patrimoniale, "CE" per Conto Economico
    """
    # Parole chiave per identificare lo Stato Patrimoniale
    sp_keywords = [
        "attivo", "passivo", "patrimonio", "immobilizzazioni", "circolante", 
        "disponibilità", "crediti", "debiti", "rimanenze", "tfr", "fondi"
    ]
    
    # Parole chiave per identificare il Conto Economico
    ce_keywords = [
        "ricavi", "vendite", "costi", "ebitda", "ebit", "ammortamenti", 
        "svalutazioni", "oneri", "proventi", "imposte", "utile", "perdita"
    ]
    
    voce_lower = voce.lower()
    
    # Conta quante parole chiave di ciascun tipo sono presenti nella voce
    sp_count = sum(1 for kw in sp_keywords if kw in voce_lower)
    ce_count = sum(1 for kw in ce_keywords if kw in voce_lower)
    
    # Determina il tipo in base al conteggio
    if sp_count > ce_count:
        return "SP"
    elif ce_count > sp_count:
        return "CE"
    else:
        # Se non è chiaro, prova a indovinare in base ad altre caratteristiche
        if any(kw in voce_lower for kw in ["totale attivo", "totale passivo", "patrimonio netto"]):
            return "SP"
        elif any(kw in voce_lower for kw in ["risultato", "utile netto", "ricavi totali"]):
            return "CE"
        else:
            # Default a Stato Patrimoniale se non è chiaro
            return "SP"

def organize_data(df: pd.DataFrame) -> Tuple[Dict[int, Dict[str, float]], Dict[int, Dict[str, float]]]:
    """
    Organizza i dati in dizionari separati per Stato Patrimoniale e Conto Economico.
    
    Args:
        df: DataFrame con i dati di bilancio
        
    Returns:
        Tuple di dizionari (stato_patrimoniale, conto_economico)
    """
    stato_patrimoniale = {}
    conto_economico = {}
    
    # Raggruppa per Anno
    for anno, group in df.groupby("Anno"):
        sp_dict = {}
        ce_dict = {}
        
        for _, row in group.iterrows():
            voce = row["Voce"]
            valore = row["Valore"]
            
            # Identifica il tipo di voce
            tipo = identify_statement_type(voce)
            
            if tipo == "SP":
                sp_dict[voce] = valore
            else:
                ce_dict[voce] = valore
        
        stato_patrimoniale[anno] = sp_dict
        conto_economico[anno] = ce_dict
    
    return stato_patrimoniale, conto_economico