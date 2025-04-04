from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import Dict, List, Any
import pandas as pd
import io
import sys
import os

# Add the parent directory to the path to import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../..")))

from parser import parse_excel, organize_data
from matching import apply_matching
from indici import calcola_indici_per_anni, indici_to_dataframe

router = APIRouter()

@router.post("/", status_code=status.HTTP_200_OK)
async def analyze_balance(
    file: UploadFile = File(...),
    matching_type: str = Form("fuzzy")
):
    """
    Analizza un file Excel di bilancio e restituisce i dati grezzi, standardizzati e gli indici finanziari.
    
    Args:
        file: File Excel di bilancio
        matching_type: Tipo di matching da applicare (fuzzy, embedding, gpt)
        
    Returns:
        Dizionario con i dati grezzi, standardizzati e gli indici finanziari
    """
    try:
        # Leggi il file Excel
        contents = await file.read()
        excel_file = io.BytesIO(contents)
        
        # Parsing del file Excel
        df_raw = parse_excel(excel_file)
        
        # Organizzazione dei dati per anno
        stato_patrimoniale_anni, conto_economico_anni = organize_data(df_raw)
        
        # Applicazione del matching
        df_standardized = apply_matching(df_raw, matching_type)
        
        # Calcolo degli indici finanziari
        indici_anni = calcola_indici_per_anni(stato_patrimoniale_anni, conto_economico_anni)
        
        # Conversione degli indici in formato JSON-friendly
        indici_json = {str(year): indices for year, indices in indici_anni.items()}
        
        # Conversione dei DataFrame in liste di dizionari
        raw_data = df_raw.to_dict(orient="records")
        standardized_data = df_standardized.to_dict(orient="records")
        
        return {
            "raw_data": raw_data,
            "standardized_data": standardized_data,
            "financial_indices": indici_json
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Errore durante l'analisi del bilancio: {str(e)}"
        ) 