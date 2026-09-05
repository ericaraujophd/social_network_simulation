#### FUNCTIONS INSIDE THE CLASS ON ibge.py


def get_people_lavras(self, all=True):
        people_df = pd.read_csv(self.ibge_mg_f / "Pessoa03_MG.csv", encoding="iso-8859-1", sep=";")
        people_df.drop(['Unnamed: 253'], axis=1, inplace=True)

        # Save data of people in the whole Lavras
        all_people_df = people_df[people_df.Cod_setor.isin(self.lavras_sectors)].reset_index(drop=True)
        urban_people_df = people_df[people_df.Cod_setor.isin(self.lavras_urban_sectors)].reset_index(drop=True)

        all_people_df.to_csv(self.ibge_lavras_f / "all_people_lavras.csv")
        urban_people_df.to_csv(self.ibge_lavras_f / "urban_people_lavras.csv")

        if all: 
            return all_people_df
        else:
            return urban_people_df


def get_age_lavras(self, all=True):
        """
        Get the age per region 
        """
        census_ages = {
                        'M':    {
                                    '5-6':   ['V087', 'V088', 'V089', 'V090', 'V091'],
                                    '7-9':   ['V092', 'V093', 'V094', 'V095', 'V096'],
                                    '10-14': ['V097', 'V098', 'V099', 'V100', 'V101'], 
                                    '15-19': ['V102', 'V103', 'V104', 'V105', 'V106'], 
                                    '15-17': ['V107', 'V108', 'V109', 'V110', 'V111'], 
                                    '18-19': ['V112', 'V113', 'V114', 'V115', 'V116'], 
                                    '20-24': ['V117', 'V118', 'V119', 'V120', 'V121'], 
                                    '25-29': ['V122', 'V123', 'V124', 'V125', 'V126'], 
                                    '30-34': ['V127', 'V128', 'V129', 'V130', 'V131'], 
                                    '35-39': ['V132', 'V133', 'V134', 'V135', 'V136'], 
                                    '40-44': ['V137', 'V138', 'V139', 'V140', 'V141'], 
                                    '45-49': ['V142', 'V143', 'V144', 'V145', 'V146'], 
                                    '50-54': ['V147', 'V148', 'V149', 'V150', 'V151'], 
                                    '55-59': ['V152', 'V153', 'V154', 'V155', 'V156'], 
                                    '60-69': ['V157', 'V158', 'V159', 'V160', 'V161'], 
                                    '70-XX':    ['V162', 'V163', 'V164', 'V165', 'V166'], 
                                },
                        'F':    {
                                    '5-6':   ['V167', 'V168', 'V169', 'V170', 'V171'],
                                    '7-9':   ['V172', 'V173', 'V174', 'V175', 'V176'],
                                    '10-14': ['V177', 'V178', 'V179', 'V180', 'V181'], 
                                    '15-19': ['V182', 'V183', 'V184', 'V185', 'V186'], 
                                    '15-17': ['V187', 'V188', 'V189', 'V190', 'V191'], 
                                    '18-19': ['V192', 'V193', 'V194', 'V195', 'V196'], 
                                    '20-24': ['V197', 'V198', 'V199', 'V200', 'V201'], 
                                    '25-29': ['V202', 'V203', 'V204', 'V205', 'V206'], 
                                    '30-34': ['V207', 'V208', 'V209', 'V210', 'V211'], 
                                    '35-39': ['V212', 'V213', 'V214', 'V215', 'V216'], 
                                    '40-44': ['V217', 'V218', 'V219', 'V220', 'V221'], 
                                    '45-49': ['V222', 'V223', 'V224', 'V225', 'V226'], 
                                    '50-54': ['V227', 'V228', 'V229', 'V230', 'V231'], 
                                    '55-59': ['V232', 'V233', 'V234', 'V235', 'V236'], 
                                    '60-69': ['V237', 'V238', 'V239', 'V240', 'V241'], 
                                    '70-XX':    ['V242', 'V243', 'V244', 'V245', 'V246'], 
                                },
                        }
    
        df_all = self.people_all_df.copy()
        df_urban = self.people_urban_df.copy()

        for key, values in census_ages.items():
            for k in values:
                field_list = census_ages[key][k]

                df_all[field_list] = df_all[field_list].apply(pd.to_numeric, errors='coerce')
                df_all[key+k] = df_all[field_list].sum(axis=1)

                df_urban[field_list] = df_urban[field_list].apply(pd.to_numeric, errors='coerce')
                df_urban[key+k] = df_urban[field_list].sum(axis=1)

        age_list = ['Cod_setor',
                    'M5-6', 'M7-9', 'M10-14', 'M15-17', 'M18-19', 'M20-24', 'M25-29', 'M30-34', 'M35-39', 'M40-44', 
                    'M45-49', 'M50-54', 'M55-59', 'M60-69', 'M70-XX',
                    'F5-6', 'F7-9', 'F10-14', 'F15-17', 'F18-19', 'F20-24', 'F25-29', 'F30-34', 'F35-39', 'F40-44',
                    'F45-49', 'F50-54', 'F55-59', 'F60-69', 'F70-XX'
                    ]
        
        df_all = df_all[age_list]
        df_urban = df_urban[age_list]

        df_all.to_csv(self.ibge_lavras_f / "age_all_lavras.csv")
        df_urban.to_csv(self.ibge_lavras_f / "age_urban_lavras.csv")
        
        self.age_all = df_all
        self.age_urban = df_urban
        if all: 
            return df_all
        else:
            return df_urban