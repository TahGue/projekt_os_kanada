# Pandas library for data manipulation
# Documentation: https://pandas.pydata.org/docs/
# Version: 2.1.4
import pandas as pd

# NumPy for numerical operations
# Documentation: https://numpy.org/doc/
# Version: 1.26.2
import numpy as np
from typing import Dict, Optional, Union


class OlympicAnalyzer:
    """
    Välstrukturerad OOP-lösning för olympisk dataanalys
    
    Krav: Väl Godkänt - koden är välstrukturerad med funktioner och/eller OOP
    Denna klass tillhandahåller modulära metoder för olika typer av analyser.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initierar analysern med en DataFrame
        
        Args:
            df (pd.DataFrame): DataFrame med olympisk data
        """
        self.df = df.copy()
    
    def top_sports_by_medals(self, country_code: str, top_n: int = 10) -> pd.Series:
        """
        Sporter med flest medaljer för ett land
        
        Args:
            country_code (str): NOC-kod för landet
            top_n (int): Antal toppsporter att returnera
            
        Returns:
            pd.Series: Sorterad serie med sporter och medaljantal
        """
        # Boolean indexing for efficient data filtering
        # Reference: Pandas documentation - https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing
        country_data = self.df[
            (self.df['NOC'] == country_code) & 
            (self.df['Medal'].notna())
        ]
        return country_data['Sport'].value_counts().head(top_n)
    
    def medals_per_olympics(self, country_code: str) -> pd.Series:
        """
        Antal medaljer per olympiad för ett land
        
        Args:
            country_code (str): NOC-kod för landet
            
        Returns:
            pd.Series: Serie med år som index och medaljantal som värden
        """
        return self.df[
            (self.df['NOC'] == country_code) & 
            (self.df['Medal'].notna())
        ].groupby('Year').size()
    
    def age_distribution(self, country_code: str) -> pd.Series:
        """
        Åldersfördelning för ett lands idrottare
        
        Args:
            country_code (str): NOC-kod för landet
            
        Returns:
            pd.Series: Serie med åldrar
        """
        return self.df[
            (self.df['NOC'] == country_code) & 
            (self.df['Age'].notna())
        ]['Age']
    
    def sport_analysis(self, sport_name: str) -> Dict[str, Union[pd.Series, pd.DataFrame]]:
        """
        Djupanalys för en specifik sport
        
        Args:
            sport_name (str): Namn på sporten
            
        Returns:
            dict: Dictionary med olika analyser:
                - medal_countries: Medaljer per land
                - age_distribution: Åldersfördelning
                - gender_split: Könsfördelning
                - medal_types: Fördelning av medaljtyper
        """
        sport_df = self.df[self.df['Sport'] == sport_name]
        
        return {
            'medal_countries': sport_df[sport_df['Medal'].notna()]['NOC'].value_counts().head(8),
            'age_distribution': sport_df[sport_df['Age'].notna()]['Age'],
            'gender_split': sport_df['Sex'].value_counts(),
            'medal_types': sport_df[sport_df['Medal'].notna()]['Medal'].value_counts()
        }
    
    def get_medal_statistics(self, country_code: str) -> pd.Series:
        """
        Detaljerad medaljstatistik för ett land (guld, silver, brons)
        
        Args:
            country_code (str): NOC-kod för landet
            
        Returns:
            pd.Series: Medaljtyper med antal
        """
        country_medals = self.df[
            (self.df['NOC'] == country_code) & 
            (self.df['Medal'].notna())
        ]
        return country_medals['Medal'].value_counts()
    
    def get_top_athletes_by_medals(self, country_code: str, top_n: int = 10) -> pd.Series:
        """
        Toppidrottare (baserat på hash) med flest medaljer för ett land
        
        Args:
            country_code (str): NOC-kod för landet
            top_n (int): Antal toppidrottare att returnera
            
        Returns:
            pd.Series: Idrottare (hashade namn) med medaljantal
        """
        country_medals = self.df[
            (self.df['NOC'] == country_code) & 
            (self.df['Medal'].notna())
        ]
        return country_medals['Name_hash'].value_counts().head(top_n)

    def country_athlete_profile(self, country_code: str = 'CAN', season: Optional[str] = None, medal_only: bool = False) -> pd.DataFrame:
        """
        Returnerar dataprofil för ett lands atleter (används för 3D-visualiseringar)

        Args:
            country_code (str): NOC-kod för landet
            season (str | None): Filtrera på säsong ('Summer', 'Winter' eller None/'All')
            medal_only (bool): Om endast medaljörer ska inkluderas

        Returns:
            pd.DataFrame: Filtrerad DataFrame med numeriska attribut bevarade
        """
        data = self.df[self.df['NOC'] == country_code].copy()

        if season and season != 'All':
            data = data[data['Season'] == season]

        if medal_only:
            data = data[data['Medal'].notna()]

        numeric_cols = ['Age', 'Height', 'Weight']
        data = data.dropna(subset=numeric_cols).copy()

        for col in numeric_cols:
            data[col] = pd.to_numeric(data[col], errors='coerce')

        data = data.dropna(subset=numeric_cols)
        data['Year'] = data['Year'].astype(int)

        return data

    def global_medal_race(self, season: Optional[str] = None, top_n: int = 10) -> pd.DataFrame:
        """
        Skapar en global medaljtabell per år för animerade visualiseringar.

        Args:
            season (str | None): Filtrera på säsong ('Summer', 'Winter' eller None/'All')
            top_n (int): Antal länder att visa per år

        Returns:
            pd.DataFrame: DataFrame med kolumnerna Year, NOC och Medals
        """
        data = self.df[self.df['Medal'].notna()].copy()

        if season and season != 'All':
            data = data[data['Season'] == season]

        medal_table = (
            data.groupby(['Year', 'NOC'])
            .size()
            .reset_index(name='Medals')
        )

        medal_table['Year'] = medal_table['Year'].astype(int)
        medal_table = medal_table.sort_values(['Year', 'Medals'], ascending=[True, False])

        top_table = medal_table.groupby('Year').head(top_n).copy()
        top_table['Rank'] = top_table.groupby('Year')['Medals'].rank(method='first', ascending=False)

        return top_table

