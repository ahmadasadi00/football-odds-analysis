import typing as T
import pandas as pd
import os
os.chdir(r'D:\Projects\football-odds-analysis')

Bet = T.Literal["H", "D", "A"]
Bookmaker = T.Literal['Bet365', 'Bet&Win', 'Interwetten', 'William_Hill', 'VC_Bet']

companies = {'Bet365': 'B365',
             'Bet&Win': 'BW',
             'Interwetten': 'IW',
             'William_Hill': 'WH',
             'VC_Bet': 'VC',
             'AVG': 'Avg'}

def get_bet_results(
    bookmakers_data: pd.DataFrame,
    game_id: str, 
    bet: Bet , 
    bookmaker: Bookmaker,
    amount: float) -> float:
    """A function that calculates a bet payout based on full time results of the match

    Args:
        bookmakers_data (DataFrame): the complete data of different bookmakers and games
        game_id (str): unique game id that assigned to each game
        bet (Bet): HomeTeam Win (H), Draw (D) or AwayTeam Win (A)
        bookmaker (Bookmaker): the bookmaker that the bet is placed
        amount (float): the dollar amount of bet placed

    Returns:
        float: the payout of the bet
    """
    bm_data = bookmakers_data[bookmaker]
    game_row = bm_data[bm_data['Unique_ID'] == game_id]
    co_code = companies[bookmaker]
    
    if game_row.FTR == bet:
        payout = game_row[f'{co_code}{bet}']*amount
    else:
        payout = 0
    
    return payout

