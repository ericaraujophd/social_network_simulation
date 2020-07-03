
"""
Programmer: Eric Araujo
Last changes: 2020-07-03

Code for fakenews simulation analysis 

These functions are used in the notebook Results_Notebook.ipynb
"""

import pandas as pd
import glob

column_change_names = {
    '[run number]': 'run',
    'fakenews-rate' : 'fakenews_rate', 
    'public-groups?': 'public_groups', 
    'num-users': 'num_users', 
    'graphics?': 'graphics',
    'perc-public-groups': 'perc_pub_groups', 
    '[step]': 'step', 
    'count posts': 'total_posts',
    'count posts with [shared?]': 'shared_posts',
    'count posts with [fakenews? and not shared?]': 'fakenews_posts',
    'count posts with [fakenews? and shared?]': 'fakenews_shared',
    'count users with [public-group?]': 'pub_group_users', 
    'count users with [id-group = 0]': 'group0_users',
    'count users with [id-group = 1]': 'group1_users', 
    'count users with [id-group = 2]': 'group2_users',
    'mean [num-posts] of users': 'avg_posts_per_user', 
    'db': 'db',
}





# GET DATA
class Results:
    f_results = './results/run1/'
    all_df = None

    def __init__(self):
        self.all_df = self.get_results_df()

    def get_results_df(self):
        """
        Read all csv files containing the results and set a dataframe
        """
        # Get all tables with results
        files_results = glob.glob(self.f_results + '*table.csv')

        df = pd.DataFrame()

        c_db = 0
        for f in files_results:
            if df.empty:
                df = pd.read_csv(f, skiprows=6).drop(columns=['debug?'])
                df.rename(columns=column_change_names, inplace=True)
                df['db'] = c_db
                c_db = c_db + 1
                run_index = len(set(df.run))
            else:
                temp_df = pd.read_csv(f, skiprows=6).drop(columns=['debug?'])
                temp_df.rename(columns=column_change_names, inplace=True)
                temp_df.run = temp_df.run + run_index
                temp_df['db'] = c_db
                # Merge
                df = pd.concat([df, temp_df]).reset_index(drop=True)
                
                c_db = c_db + 1
                run_index = len(set(df.run))        
        return df


    # OTHER FUNCTIONS
    def get_scenarios_step (self):
        """
        Get the DataFrame of the results for all betas and sigmas creating one column for each combination
        """
        
        # scenarios = (public_groups, perc_pub_groups)
        scenarios_list = [(True, 8),
                          (True, 22),
                          (False, '_')
                         ]

        f_df = pd.DataFrame()
        
        # if public_groups is false, ignore the perc_pub_groups
        for public_groups, perc_pub_groups in scenarios_list:
            if public_groups:
                f_df['({},{})'.format(public_groups,perc_pub_groups)] = \
                        pd.Series(list(self.all_df[(self.all_df.public_groups == public_groups) &
                                      (self.all_df.perc_pub_groups == perc_pub_groups)].step))
            else:
                f_df['({},{})'.format(public_groups,perc_pub_groups)] = \
                        pd.Series(list(self.all_df[(self.all_df.public_groups == public_groups)].step))
        
        return f_df


def get_opinions (df):
    beta_list = [0.1, 0.3, 0.5, 0.7, 0.9]
    sigma_list = [1, 5, 10]
    
    f_df = pd.DataFrame()
    
    for beta, sigma in [(x,y) for x in beta_list for y in sigma_list]:
        f_df['({},{})'.format(beta,sigma)] = pd.Series(list(df[(df.beta == beta) & (df.sigma == sigma)].opinion_avg))

    return f_df

def get_perc_lockdown (df):
    beta_list = [0.1, 0.3, 0.5, 0.7, 0.9]
    sigma_list = [1, 5, 10]
    
    f_df = pd.DataFrame()
    
    for beta, sigma in [(x,y) for x in beta_list for y in sigma_list]:
        f_df['({},{})'.format(beta,sigma)] = pd.Series(list(df[(df.beta == beta) & (df.sigma == sigma)].num_lockdown))

    return f_df


