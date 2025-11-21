# Pandas library for data manipulation
# Documentation: https://pandas.pydata.org/docs/
# Version: 2.1.4
import pandas as pd

# Python standard library hashlib for SHA-256 hashing
# Documentation: https://docs.python.org/3/library/hashlib.html
import hashlib
import os

def load_and_anonymize_data(filepath: str) -> pd.DataFrame:
    """
    Laddar data och anonymiserar idrottarnas namn med SHA256-hash
    
    Krav: Anonymisera kolumnen med idrottarnas namn med hashfunktionen
    Detta följer GDPR-principer för personuppgiftshantering.
    
    Args:
        filepath (str): Sökväg till CSV-filen
        
    Returns:
        pd.DataFrame: DataFrame med anonymiserade namn (hashade)
        
    Raises:
        FileNotFoundError: Om filen inte hittas
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Filen hittades inte: {filepath}")

    df = pd.read_csv(filepath)
    
    # Anonymisera namn - UNIK HASH FÖR VARJE NAMN
    # Använder SHA256 för säker hashning, tar första 16 tecken för läsbarhet
    # SHA-256 hashing for GDPR-compliant anonymization
    # Reference: Python hashlib documentation - https://docs.python.org/3/library/hashlib.html
    df['Name_hash'] = df['Name'].apply(
        lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]
    )
    
    # Ta bort originalnamn för GDPR-säkerhet
    df = df.drop(columns=['Name'])
    
    return df


def get_country_stats(df: pd.DataFrame, country_code: str = 'CAN') -> pd.DataFrame:
    """
    Extraherar statistik för ett specifikt land
    
    Args:
        df (pd.DataFrame): DataFrame med olympisk data
        country_code (str): NOC-kod för landet (t.ex. 'SWE', 'USA')
        
    Returns:
        pd.DataFrame: Filtrerad DataFrame för det valda landet
    """
    return df[df['NOC'] == country_code]

