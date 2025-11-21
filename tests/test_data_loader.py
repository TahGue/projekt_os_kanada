import pytest
import pandas as pd
import os
from src.data_loader import load_and_anonymize_data, get_country_stats

def test_load_and_anonymize_data(sample_csv):
    df = load_and_anonymize_data(sample_csv)
    
    assert isinstance(df, pd.DataFrame)
    assert 'Name' not in df.columns
    assert 'Name_hash' in df.columns
    assert len(df) == 5
    
    # Verify hashing is consistent
    assert df.iloc[0]['Name_hash'] == df.iloc[0]['Name_hash']

def test_load_data_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_and_anonymize_data("non_existent_file.csv")

def test_get_country_stats(sample_data):
    can_stats = get_country_stats(sample_data, 'CAN')
    assert len(can_stats) == 2
    assert all(can_stats['NOC'] == 'CAN')
    
    usa_stats = get_country_stats(sample_data, 'USA')
    assert len(usa_stats) == 2
    assert all(usa_stats['NOC'] == 'USA')
