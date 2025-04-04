from sqlalchemy import text
from .base import Base, engine

def init_db():
    """Inizializza il database creando tutte le tabelle."""
    try:
        # Verifica la connessione al database
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Connessione al database stabilita con successo")
        
        # Crea tutte le tabelle
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelle create con successo")
        
    except Exception as e:
        print(f"❌ Errore durante l'inizializzazione del database: {str(e)}")
        raise

if __name__ == "__main__":
    init_db() 