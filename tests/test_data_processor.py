import pytest
import pandas as pd
from src.data_processor import OlympicAnalyzer

@pytest.fixture
def analyzer(sample_data):
    return OlympicAnalyzer(sample_data)

def test_top_sports_by_medals(analyzer):
    top_sports = analyzer.top_sports_by_medals('CAN')
    assert isinstance(top_sports, pd.Series)
    assert 'Swimming' in top_sports.index
    assert top_sports['Swimming'] == 2 # Gold and Bronze

def test_medals_per_olympics(analyzer):
    medals = analyzer.medals_per_olympics('CAN')
    assert 2020 in medals.index
    assert medals[2020] == 1
    assert 2016 in medals.index
    assert medals[2016] == 1

def test_age_distribution(analyzer):
    ages = analyzer.age_distribution('CAN')
    assert len(ages) == 2
    assert 25 in ages.values
    assert 22 in ages.values

def test_gender_distribution(analyzer):
    gender_dist = analyzer.gender_distribution('CAN')
    assert gender_dist['M'] == 1
    assert gender_dist['F'] == 1

def test_sport_analysis(analyzer):
    analysis = analyzer.sport_analysis('Swimming')
    assert isinstance(analysis, dict)
    assert 'medal_countries' in analysis
    assert 'age_distribution' in analysis
    assert 'gender_split' in analysis
    assert 'medal_types' in analysis
    
    assert analysis['medal_countries']['CAN'] == 2

def test_get_medal_statistics(analyzer):
    medals = analyzer.get_medal_statistics('CAN')
    assert medals['Gold'] == 1
    assert medals['Bronze'] == 1

def test_country_athlete_profile(analyzer):
    profile = analyzer.country_athlete_profile('CAN')
    assert len(profile) == 2
    assert all(profile['NOC'] == 'CAN')
    
    # Test season filter
    summer_profile = analyzer.country_athlete_profile('CAN', season='Summer')
    assert len(summer_profile) == 2
    
    winter_profile = analyzer.country_athlete_profile('CAN', season='Winter')
    assert len(winter_profile) == 0

def test_global_medal_race(analyzer):
    race = analyzer.global_medal_race()
    assert isinstance(race, pd.DataFrame)
    assert 'Year' in race.columns
    assert 'NOC' in race.columns
    assert 'Medals' in race.columns
    assert 'Rank' in race.columns
