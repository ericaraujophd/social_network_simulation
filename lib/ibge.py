"""
Extracting only Lavras data from the Brazil dataset

This dataset was extracted from [IBGE Census 2010](https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html). The dataset contained the data from the state of Minas Gerais. This notebook extracts the data only for Lavras and saves in CSV format.

Due to the size of the files, this process might take a few minutes.

Programmer: Eric Araujo
Last update: 2020-05-15
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import pickle 
# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
from pathlib import Path

class IBGE_Lavras:
    ibge_mg_f = Path("./data/IBGE_MG/CSV/")
    ibge_lavras_f = Path("./data/IBGE_LAVRAS")
    # SECTORS
    lavras_sectors = None
    lavras_urban_sectors = None 
    # HOUSEHOLDS
    basic_all_df = None
    basic_urban_df = None
    # AGE
    age_men_all_df = None
    age_men_urban_df = None 
    age_women_all_df = None
    age_women_urban_df = None 

    #people_all_df = None
    #people_urban_df = None
    #age_all = None
    #age_urban = None
    

    def __init__(self, all=True):
        # Basic data
        self.basic_all_df = self.get_basic_lavras(all=True)
        self.basic_urban_df = self.get_basic_lavras(all=False)

        #self.people_all_df = self.get_people_lavras(all=True)
        # Set urban area data
        
        #self.people_urban_df = self.get_people_lavras(all=False)
        #self.age_all = self.get_age_lavras(all=True)
        #self.age_urban = self.get_age_lavras(all=False)
        
        self.get_age()
        
        

    def get_basic_lavras(self, all=True):
        """
        This function reads the MG table for Basic information from census and returns selected data from Lavras city
        """
        # Basic Data dictionary
        basic_names_dict = {
            'V001': 'households',
            'V002': 'population',
            'V003': 'avg_occupants', # V002/V001
            'V004': 'std_occupants',
            'V005': 'avg_income_all', 
            'V006': 'std_income_all',
            'V007': 'avg_income_workers',
            'V008': 'std_income_workers',
            'V009': 'avg_income_all_10_plus', 
            'V010': 'std_income_all_10_plus',
            'V011': 'avg_income_workers_10_plus',
            'V012': 'std_income_workers_10_plus'
        }

        basic_df = pd.read_csv(str(self.ibge_mg_f / "Basico_MG.csv"), encoding="iso-8859-1", sep=";")
        basic_df.rename(columns=basic_names_dict, inplace=True)

        basic_df.drop(['Unnamed: 33', 'Cod_UF', 'Nome_do_distrito', 'Cod_Grandes Regiões', 'Nome_da_meso',
                       'Nome_Grande_Regiao', 'Nome_da_UF ', 'Nome_da_RM', 'Cod_RM', 'Cod_meso', 'Cod_micro',
                       'Nome_da_micro', 'Nome_do_bairro'
                      ], axis=1, inplace=True)

        # Remove areas with less than 5 houses
        basic_df = basic_df[basic_df.households >= 5]

        basic_df = basic_df[basic_df.Cod_municipio == 3138203].reset_index(drop=True)

        

        basic_df['avg_occupants'] = basic_df['avg_occupants'].str.replace(',', '.').astype(float)
        basic_df['std_occupants'] = basic_df['std_occupants'].str.replace(',', '.').astype(float)
        basic_df['avg_income_all'] = basic_df['avg_income_all'].str.replace(',', '.').astype(float)
        basic_df['std_income_all'] = basic_df['std_income_all'].str.replace(',', '.').astype(float)
        basic_df['avg_income_workers'] = basic_df['avg_income_workers'].str.replace(',', '.').astype(float)
        basic_df['std_income_workers'] = basic_df['std_income_workers'].str.replace(',', '.').astype(float)
        basic_df['avg_income_all_10_plus'] = basic_df['avg_income_all_10_plus'].str.replace(',', '.').astype(float)
        basic_df['std_income_all_10_plus'] = basic_df['std_income_all_10_plus'].str.replace(',', '.').astype(float)
        basic_df['avg_income_workers_10_plus'] = basic_df['avg_income_workers_10_plus'].str.replace(',', '.').astype(float)
        basic_df['std_income_workers_10_plus'] = basic_df['std_income_workers_10_plus'].str.replace(',', '.').astype(float)

        # Save the list of sectors from Lavras
        self.lavras_sectors = list(basic_df.Cod_setor)
        pickle.dump(self.lavras_sectors, open(self.ibge_lavras_f / "list_lavras.pickle", "wb" ) )

        urban_basic_df = basic_df[(basic_df.Situacao_setor == 1) | (basic_df.Situacao_setor == 2)]
    
        # List of urban sectors of Lavras
        self.lavras_urban_sectors = list(urban_basic_df.Cod_setor)
        pickle.dump(self.lavras_urban_sectors, open(self.ibge_lavras_f / "list_urban.pickle", "wb" ) )

        basic_df.to_csv(self.ibge_lavras_f / "basic_lavras.csv")
        urban_basic_df.to_csv(self.ibge_lavras_f / "basic_urban.csv")

        basic_df[['Cod_setor', 'households', 'population']].to_csv(self.ibge_lavras_f / "households_lavras.csv")
        urban_basic_df[['Cod_setor', 'households', 'population']].to_csv(self.ibge_lavras_f / "households_urban.csv")

        if all:
            return basic_df
        else:
            return urban_basic_df

    

    def get_age(self, gender=None, all=True):

        # Create the dictionary for ages
        keys = [i + 1 for i in range(100)]
        values = [['V'+"{:03}".format(i+35)] for i in range(100)]

        census_ages_dict = dict(zip(keys,values))
        census_ages_dict[0] = ['V022']

        census_ages_dict = { key: value for (key, value) in sorted(census_ages_dict.items()) }
        
        # Load data
        age_men_lavras_df = pd.read_csv(str(self.ibge_mg_f / "Pessoa11_MG.csv"), encoding="iso-8859-1", sep=";")
        age_women_lavras_df = pd.read_csv(str(self.ibge_mg_f / "Pessoa12_MG.csv"), encoding="iso-8859-1", sep=";")

        men_lavras_df = age_men_lavras_df[age_men_lavras_df.Cod_setor.isin(self.lavras_sectors)].reset_index(drop=True)
        men_urban_df = age_men_lavras_df[age_men_lavras_df.Cod_setor.isin(self.lavras_urban_sectors)].reset_index(drop=True)

        women_lavras_df = age_women_lavras_df[age_women_lavras_df.Cod_setor.isin(self.lavras_sectors)].reset_index(drop=True)
        women_urban_df = age_women_lavras_df[age_women_lavras_df.Cod_setor.isin(self.lavras_urban_sectors)].reset_index(drop=True)

        for key, values in census_ages_dict.items():
            men_lavras_df[values] = men_lavras_df[values].apply(pd.to_numeric, errors='coerce')
            men_urban_df[values] = men_urban_df[values].apply(pd.to_numeric, errors='coerce')

            women_lavras_df[values] = women_lavras_df[values].apply(pd.to_numeric, errors='coerce')
            women_urban_df[values] = women_urban_df[values].apply(pd.to_numeric, errors='coerce')
            
            men_lavras_df[key] = men_lavras_df[values].sum(axis=1)
            men_urban_df[key] = men_urban_df[values].sum(axis=1)

            women_lavras_df[key] = women_lavras_df[values].sum(axis=1)
            women_urban_df[key] = women_urban_df[values].sum(axis=1)

        men_lavras_df[['Cod_setor'] + list(range(101))].to_csv(self.ibge_lavras_f / "age_men_lavras.csv")
        men_urban_df[['Cod_setor'] + list(range(101))].to_csv(self.ibge_lavras_f / "age_men_urban.csv")

        women_lavras_df[['Cod_setor'] + list(range(101))].to_csv(self.ibge_lavras_f / "age_women_lavras.csv")
        women_urban_df[['Cod_setor'] + list(range(101))].to_csv(self.ibge_lavras_f / "age_women_urban.csv")

        self.age_men_all_df = men_lavras_df[['Cod_setor'] + list(range(101))]
        self.age_men_urban_df =  men_urban_df[['Cod_setor'] + list(range(101))]

        self.age_women_all_df = women_lavras_df[['Cod_setor'] + list(range(101))]
        self.age_women_urban_df =  women_urban_df[['Cod_setor'] + list(range(101))]




