import pandas as pd
import itertools
import typing as T
from input_variables import COMPANY_BETS


def get_favorite_bets(bookmakers_data: pd.DataFrame, 
                      cut_off: float)-> T.Dict:
    """A function that gets all games betting odds data and finds bets that the probability of one outcome (H, A, D) is more than a cutoff

    Args:
        bookmakers_data (pd.DataFrame): betting odds data
        cut_off (float): the threshold for finding favorite bets should be < 1

    Returns:
        T.Dict: favorite bets:
        {'game_id': `{company}{bet}`}
    """
    favorites = {}
    
    for cb in COMPANY_BETS:
        cb_probs = 1/bookmakers_data[cb]
        selected_bets = cb_probs[cb_probs > cut_off]
        for bet in selected_bets.index:
            favorites[bet] = cb
    
    return favorites


def get_longshot_bets(bookmakers_data: pd.DataFrame, 
                      cut_off: float)-> T.Dict:
    """A function that gets all games betting odds data and finds bets that the probability of one outcome (H, A, D) is less than a cutoff

    Args:
        bookmakers_data (pd.DataFrame): betting odds data
        cut_off (float): the threshold for finding longshot bets should be < 1

    Returns:
        T.Dict: favorite bets:
        {'game_id': `{company}{bet}`}
    """
    longshots = {}
    for cb in COMPANY_BETS:
        cb_probs = 1/bookmakers_data[cb]
        selected_bets = cb_probs[cb_probs < cut_off]
        
        for bet in selected_bets.index:
            longshots[bet] = cb
    
    return longshots