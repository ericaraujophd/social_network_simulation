"""
Extracting only Lavras data from the Brazil dataset

This dataset was extracted from [INEP Census 2018](http://portal.inep.gov.br/web/guest/microdados#). 
The dataset contained the data from the southeast states of Brazil. This notebook extracts the data only for Lavras and saves in CSV format.


Programmer: Eric Araujo
Last update: 2020-05-17
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import pickle 
# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
from pathlib import Path

class INEP_Lavras:
    inep_lavras_f = Path("./data/INEP_LAVRAS_RAW/")
    destination_f = Path("./data/INEP_LAVRAS/")
    schools_df = None
    classes_df = None
    teachers_df = None
    students_df = None

    def __init__(self):
        schools_df = pd.read_csv(inep_lavras_f / 'schools_loc_qgis.csv')
        classes_df = pd.read_csv(inep_lavras_f / 'classes_Lavras.csv')
        teachers_df = pd.read_csv(inep_lavras_f / "teachers_Lavras.csv")[['ID_DOCENTE', 'NU_IDADE_REFERENCIA',
                                                                          'TP_SEXO', 'ID_TURMA'
                                                                         ]]

        self.schools_df = schools_df.copy()

        # 1 = Presencial 2 = Semipresencial 3 = EAD
        classes_df = classes_df[classes_df.TP_MEDIACAO_DIDATICO_PEDAGO == 1]

        classes_df = classes_df[['ID_TURMA',
                                 'TX_HR_INICIAL',
                                 'NU_DURACAO_TURMA', 
                                 'QT_MATRICULAS',
                                 'TP_ETAPA_ENSINO',
                                 'NU_DIAS_ATIVIDADE',
                                 'CO_ENTIDADE'
                                ]]
        # Drop classes with Nan TP_ETAPA_ENSINO (Grades) and at least 5 days
        classes_df = classes_df[(classes_df['TP_ETAPA_ENSINO'].notna()) & (classes_df.NU_DIAS_ATIVIDADE >= 5)]
        # Add geo information to classes
        classes_df = pd.merge(classes_df, schools_df[['Codigo_INEP', 'CD_GEOCODI']], 
                              left_on='CO_ENTIDADE', 
                              right_on='Codigo_INEP').drop('Codigo_INEP', axis=1)

        # Students
        students_df = pd.read_csv(inep_lavras_f / "registers_Lavras.csv")[['ID_ALUNO', 'ID_MATRICULA', 
                                                                           'NU_IDADE_REFERENCIA', 'TP_SEXO',
                                                                           'ID_TURMA'
                                                                          ]]

        self.students_df = students_df.copy()

        age_students_df = pd.DataFrame(students_df.groupby('ID_TURMA').mean()['NU_IDADE_REFERENCIA'])
        age_students_df.columns = ['AGE_AVG_STUDENTS']
        age_students_df['AGE_STD_STUDENTS'] = students_df.groupby('ID_TURMA').std()['NU_IDADE_REFERENCIA']
        age_students_df['ID_TURMA'] = age_students_df.index
        age_students_df.reset_index(drop=True, inplace=True)

        classes_df = pd.merge(classes_df, age_students_df, on='ID_TURMA')

        # Teachers
        teachers_df = teachers_df[teachers_df.ID_TURMA.isin(list(classes_df.ID_TURMA))]
        self.teachers_df = teachers_df

        teachers_info_df = pd.DataFrame(teachers_df.groupby('ID_TURMA').count()['ID_DOCENTE'])
        teachers_info_df.columns = ['NUM_TEACHERS']
        teachers_info_df['AGE_AVG_TEACHERS'] = teachers_df.groupby('ID_TURMA').mean()['NU_IDADE_REFERENCIA']
        teachers_info_df['AGE_STD_TEACHERS'] = teachers_df.groupby('ID_TURMA').std()['NU_IDADE_REFERENCIA'].fillna(0)
        teachers_info_df.reset_index(inplace=True)
        
        classes_df = pd.merge(classes_df, teachers_info_df, on='ID_TURMA').fillna(0)

        self.classes_df = classes_df.copy()

        teachers_df.to_csv(destination_f / "teachers.csv")
        classes_df.to_csv(destination_f / "classes.csv")

