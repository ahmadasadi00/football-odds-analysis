import pandas as pd
import warnings
import pickle
import typing as T
warnings.filterwarnings('ignore')

# companies
# Bet365
# Bet&Win
# Interwetten
# William Hill
# VC Bet

def cal_prob(df: pd.DataFrame, 
             companycode: str, 
             prefix: str = '') -> pd.DataFrame:
    """calculates the probability of each outcome based on betting odds

    Args:
        df (pd.DataFrame): dataframe of games should have 3 columns of 
        `companycode`H (HomeTeam Winnig Odds), `companycode`D (Draw Odds) and `companycode`A (AwayTeam Winning Odds)
        companycode (str): betting companycode i.e. for Bet&Win is bw
        prefix (str, optional): prefix for column name of output Defaults to ''.

    Returns:
        pd.DataFrame: the odds input dataframe that now include probabality of each outcome based on odds i.e. 1/odd
    """
    df[prefix + 'ProbH'] = 1/df[f'{companycode}H']
    df[prefix + 'ProbA'] = 1/df[f'{companycode}A']
    df[prefix + 'ProbD'] = 1/df[f'{companycode}D']
    return df


def calc_bookmakers_margin(df: pd.DataFrame, 
                           companycode: str,
                           prefix: str = '') -> pd.DataFrame:
    """adds a column to betting odds dataframe as the bookmaker's margin

    Args:
        df (pd.DataFrame): betting odds dataframe
        companycode (str): companycode
        prefix (str, optional): column prefix Defaults to ''.

    Returns:
        pd.DataFrame: betting odds dataframe
    """
    
    df[prefix + 'return_on_game'] = (1 / df[f'{companycode}H']) + (1 / df[f'{companycode}D']) + (1 / df[f'{companycode}A']) - 1
    return df


def preprocess_pipeline(odds_data_address: str) -> T.Dict:
    """gets address of betting odds csv file address and preprocess the data, 
       raw data source https://www.football-data.co.uk/data.php
    Args:
        odds_data_address (str): address to betting odds csv file for download the data please refer to https://www.kaggle.com/datasets/ahmadasadi00/football-betting-odds

    Returns:
        T.Dict:  dictionary which keys are the bookmaker's names and contains each bookmakers odds and probabilities and margins
    """
    data = pd.read_csv(odds_data_address, index_col=0)
    main_cols = ['Unique_ID', 'Div', 'Date', 'HomeTeam' ,'AwayTeam', 'FTR']
    avg_cols = ['AvgH', 'AvgD', 'AvgA','AvgProbH','AvgProbA','AvgProbD', 'Avg_return_on_game']
    avg_df = data[main_cols]

    cols_b365 = ['Unique_ID', 'Div','Date', 'HomeTeam' ,'AwayTeam', 'FTR', 'B365H', 'B365D', 'B365A']
    cols_bw = ['Unique_ID', 'Div','Date', 'HomeTeam' ,'AwayTeam', 'FTR', 'BWH', 'BWD', 'BWA']
    cols_iw = ['Unique_ID', 'Div','Date', 'HomeTeam' ,'AwayTeam', 'FTR', 'IWH', 'IWD', 'IWA']
    cols_wh = ['Unique_ID', 'Div','Date', 'HomeTeam' ,'AwayTeam', 'FTR', 'WHH', 'WHD', 'WHA']
    cols_vc = ['Unique_ID', 'Div','Date', 'HomeTeam' ,'AwayTeam', 'FTR', 'VCH', 'VCD', 'VCA']

    b365_df = data[cols_b365]
    bw_df = data[cols_bw]
    iw_df = data[cols_iw]
    wh_df = data[cols_wh]
    vc_df = data[cols_vc]

    avg_df['AvgH'] = data[['BWH','IWH','WHH','VCH']].mean(axis=1)
    avg_df['AvgD'] = data[['BWD','IWD','WHD','VCD']].mean(axis=1)
    avg_df['AvgA'] = data[['BWA','IWA','WHA','VCA']].mean(axis=1)

    b365_df = cal_prob(b365_df, 'B365')
    bw_df = cal_prob(bw_df, 'BW')
    iw_df = cal_prob(iw_df, 'IW')
    wh_df = cal_prob(wh_df, 'WH')
    vc_df = cal_prob(vc_df, 'VC')
    avg_df = cal_prob(avg_df, 'Avg', 'Avg')

    b365_df = calc_bookmakers_margin(b365_df, 'B365')
    bw_df = calc_bookmakers_margin(bw_df, 'BW')
    iw_df = calc_bookmakers_margin(iw_df, 'IW')
    wh_df = calc_bookmakers_margin(wh_df, 'WH')
    vc_df = calc_bookmakers_margin(vc_df, 'VC')
    avg_df = calc_bookmakers_margin(avg_df, 'Avg', 'Avg_')

    b365_df = pd.concat([b365_df, avg_df[avg_cols]], axis=1)
    bw_df = pd.concat([bw_df, avg_df[avg_cols]], axis=1)
    iw_df = pd.concat([iw_df, avg_df[avg_cols]], axis=1)
    wh_df = pd.concat([wh_df, avg_df[avg_cols]], axis=1)
    vc_df = pd.concat([vc_df, avg_df[avg_cols]], axis=1)

    betting_odds_clean_data = {'Bet365': b365_df,
                               'Bet&Win': bw_df,
                               'Interwetten': iw_df,
                               'William_Hill': wh_df,
                               'VC_Bet': vc_df,
                               'AVG': avg_df}
    
    return betting_odds_clean_data


def preprocess_odds_results(odds_data_address: str) -> T.Dict:
    data = pd.read_csv(odds_data_address, index_col=0)
    odds = data[['B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA', 'IWH',
                                  'IWD', 'IWA', 'WHH', 'WHD', 'WHA', 'VCH', 'VCD', 'VCA',]]
    
    odds['Unique_ID'] = data['Unique_ID']
    odds['Date'] = data['Date']
    odds.set_index('Unique_ID', drop=True, inplace=True)
    
    results = data[['Unique_ID', 'Date', 'FTR']]
    results.set_index('Unique_ID', drop=True, inplace=True)
    
    odds_results = {'Odds': odds,
                    'Results': results}
    return odds_results