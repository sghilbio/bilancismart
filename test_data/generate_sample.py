import pandas as pd
import numpy as np
import os

# Crea un DataFrame per lo Stato Patrimoniale
def create_balance_sheet():
    # Anni
    years = [2020, 2021, 2022, 2023]
    
    # Voci dello Stato Patrimoniale
    sp_items = [
        "Immobilizzazioni",
        "Attivo Circolante",
        "Disponibilità Liquide",
        "Crediti",
        "Rimanenze",
        "Totale Attivo",
        "Patrimonio Netto",
        "Passività Correnti",
        "Passività Consolidate",
        "Totale Passivo"
    ]
    
    # Crea un DataFrame vuoto
    df_sp = pd.DataFrame(index=sp_items, columns=years)
    
    # Popola con valori casuali ma realistici
    # Immobilizzazioni (crescono lentamente)
    df_sp.loc["Immobilizzazioni", 2020] = 500000
    for i in range(1, len(years)):
        df_sp.loc["Immobilizzazioni", years[i]] = df_sp.loc["Immobilizzazioni", years[i-1]] * (1 + np.random.uniform(0.02, 0.05))
    
    # Attivo Circolante (cresce con l'azienda)
    df_sp.loc["Attivo Circolante", 2020] = 300000
    for i in range(1, len(years)):
        df_sp.loc["Attivo Circolante", years[i]] = df_sp.loc["Attivo Circolante", years[i-1]] * (1 + np.random.uniform(0.05, 0.10))
    
    # Disponibilità Liquide (varia)
    df_sp.loc["Disponibilità Liquide", 2020] = 100000
    for i in range(1, len(years)):
        df_sp.loc["Disponibilità Liquide", years[i]] = df_sp.loc["Disponibilità Liquide", years[i-1]] * (1 + np.random.uniform(-0.05, 0.15))
    
    # Crediti (crescono con i ricavi)
    df_sp.loc["Crediti", 2020] = 150000
    for i in range(1, len(years)):
        df_sp.loc["Crediti", years[i]] = df_sp.loc["Crediti", years[i-1]] * (1 + np.random.uniform(0.03, 0.08))
    
    # Rimanenze (variano)
    df_sp.loc["Rimanenze", 2020] = 50000
    for i in range(1, len(years)):
        df_sp.loc["Rimanenze", years[i]] = df_sp.loc["Rimanenze", years[i-1]] * (1 + np.random.uniform(-0.02, 0.10))
    
    # Totale Attivo
    df_sp.loc["Totale Attivo"] = df_sp.loc["Immobilizzazioni"] + df_sp.loc["Attivo Circolante"]
    
    # Patrimonio Netto (cresce con l'utile)
    df_sp.loc["Patrimonio Netto", 2020] = 400000
    for i in range(1, len(years)):
        df_sp.loc["Patrimonio Netto", years[i]] = df_sp.loc["Patrimonio Netto", years[i-1]] * (1 + np.random.uniform(0.03, 0.07))
    
    # Passività Correnti (variano)
    df_sp.loc["Passività Correnti", 2020] = 200000
    for i in range(1, len(years)):
        df_sp.loc["Passività Correnti", years[i]] = df_sp.loc["Passività Correnti", years[i-1]] * (1 + np.random.uniform(-0.05, 0.10))
    
    # Passività Consolidate (diminuiscono lentamente)
    df_sp.loc["Passività Consolidate", 2020] = 250000
    for i in range(1, len(years)):
        df_sp.loc["Passività Consolidate", years[i]] = df_sp.loc["Passività Consolidate", years[i-1]] * (1 - np.random.uniform(0.01, 0.05))
    
    # Totale Passivo
    df_sp.loc["Totale Passivo"] = df_sp.loc["Patrimonio Netto"] + df_sp.loc["Passività Correnti"] + df_sp.loc["Passività Consolidate"]
    
    return df_sp

# Crea un DataFrame per il Conto Economico
def create_income_statement():
    # Anni
    years = [2020, 2021, 2022, 2023]
    
    # Voci del Conto Economico
    ce_items = [
        "Ricavi",
        "Costi della Produzione",
        "EBITDA",
        "Ammortamenti e Svalutazioni",
        "EBIT",
        "Oneri Finanziari",
        "Utile Ante Imposte",
        "Imposte",
        "Utile Netto"
    ]
    
    # Crea un DataFrame vuoto
    df_ce = pd.DataFrame(index=ce_items, columns=years)
    
    # Popola con valori casuali ma realistici
    # Ricavi (crescono)
    df_ce.loc["Ricavi", 2020] = 1000000
    for i in range(1, len(years)):
        df_ce.loc["Ricavi", years[i]] = df_ce.loc["Ricavi", years[i-1]] * (1 + np.random.uniform(0.05, 0.12))
    
    # Costi della Produzione (percentuale dei ricavi)
    for year in years:
        df_ce.loc["Costi della Produzione", year] = df_ce.loc["Ricavi", year] * np.random.uniform(0.60, 0.70)
    
    # EBITDA (percentuale dei ricavi)
    for year in years:
        df_ce.loc["EBITDA", year] = df_ce.loc["Ricavi", year] - df_ce.loc["Costi della Produzione", year]
    
    # Ammortamenti e Svalutazioni (percentuale fissa)
    for year in years:
        df_ce.loc["Ammortamenti e Svalutazioni", year] = df_ce.loc["Ricavi", year] * np.random.uniform(0.03, 0.05)
    
    # EBIT
    for year in years:
        df_ce.loc["EBIT", year] = df_ce.loc["EBITDA", year] - df_ce.loc["Ammortamenti e Svalutazioni", year]
    
    # Oneri Finanziari (percentuale fissa)
    for year in years:
        df_ce.loc["Oneri Finanziari", year] = df_ce.loc["Ricavi", year] * np.random.uniform(0.01, 0.03)
    
    # Utile Ante Imposte
    for year in years:
        df_ce.loc["Utile Ante Imposte", year] = df_ce.loc["EBIT", year] - df_ce.loc["Oneri Finanziari", year]
    
    # Imposte (percentuale dell'utile ante imposte)
    for year in years:
        df_ce.loc["Imposte", year] = df_ce.loc["Utile Ante Imposte", year] * np.random.uniform(0.20, 0.25)
    
    # Utile Netto
    for year in years:
        df_ce.loc["Utile Netto", year] = df_ce.loc["Utile Ante Imposte", year] - df_ce.loc["Imposte", year]
    
    return df_ce

# Crea un file Excel con entrambi i fogli
def create_sample_excel():
    # Crea i DataFrame
    df_sp = create_balance_sheet()
    df_ce = create_income_statement()
    
    # Arrotonda i valori a 2 decimali
    df_sp = df_sp.round(2)
    df_ce = df_ce.round(2)
    
    # Crea il file Excel
    output_file = "sample_bilancio.xlsx"
    with pd.ExcelWriter(output_file) as writer:
        df_sp.to_excel(writer, sheet_name="Stato Patrimoniale")
        df_ce.to_excel(writer, sheet_name="Conto Economico")
    
    print(f"File Excel di esempio creato: {output_file}")
    return output_file

if __name__ == "__main__":
    create_sample_excel() 