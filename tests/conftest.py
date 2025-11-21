import pytest
import pandas as pd
import numpy as np

@pytest.fixture
def sample_data():
    data = {
        'ID': [1, 2, 3, 4, 5],
        'Name': ['Athlete One', 'Athlete Two', 'Athlete Three', 'Athlete Four', 'Athlete Five'],
        'Sex': ['M', 'F', 'M', 'F', 'M'],
        'Age': [25, 30, 22, 28, 24],
        'Height': [180, 170, 175, 165, 185],
        'Weight': [80, 60, 70, 55, 85],
        'Team': ['Team A', 'Team B', 'Team A', 'Team B', 'Team A'],
        'NOC': ['CAN', 'USA', 'CAN', 'USA', 'SWE'],
        'Games': ['2020 Summer', '2020 Summer', '2016 Summer', '2016 Summer', '2022 Winter'],
        'Year': [2020, 2020, 2016, 2016, 2022],
        'Season': ['Summer', 'Summer', 'Summer', 'Summer', 'Winter'],
        'City': ['Tokyo', 'Tokyo', 'Rio', 'Rio', 'Beijing'],
        'Sport': ['Swimming', 'Athletics', 'Swimming', 'Athletics', 'Hockey'],
        'Event': ['100m Freestyle', '100m Sprint', '200m Freestyle', '200m Sprint', 'Ice Hockey'],
        'Medal': ['Gold', 'Silver', 'Bronze', None, 'Gold']
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_csv(tmp_path, sample_data):
    filepath = tmp_path / "test_data.csv"
    sample_data.to_csv(filepath, index=False)
    return str(filepath)
