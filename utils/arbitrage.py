import pandas as pd
import itertools
import typing as T
from input_variables import CATEGORIES

def get_bet_weights(h: float, 
                    a: float, 
                    d: float) -> T.Dict:
    """A function for calculating correct weights when we found an arbitrage bet for more 
    information look at the https://en.wikipedia.org/wiki/Arbitrage_betting

    Args:
        h (float): the betting odd for winning HomeTeam 
        a (float): the betting odd for winning AwayTeam 
        d (float): the betting odd for Draw 

    Returns:
        T.Dict: weights for H, A and D
    """
    wa = 1/(1 + (a/d) + (a/h))
    wd = 1/(1 + (d/a) + (d/h))
    wh = 1/(1 + (h/d) + (h/a))
    return {'H': wh,
            'A': wa,
            'D': wd}

def get_arbitrage_bets(bookmakers_data: pd.DataFrame, 
                       cut_off: float)-> T.Dict:
    """A function that gets all games betting odds data and finds bets with arbitrage opportunity 

    Args:
        bookmakers_data (pd.DataFrame): betting odds data
        cut_off (float): the threshold for finding arbitrage opportunity should be < 1

    Returns:
        T.Dict: all arbitrage bets:
        {'game_id': [companies we place the bet for each outcome, 
                     weights we place the bet for each outcome]}
    """
    valid_combinations = {}

    for cat in itertools.product(CATEGORIES['H'], CATEGORIES['A'], CATEGORIES['D']):
        category_combination = list(cat)
        selected_set = bookmakers_data[category_combination]
        selected_set['sum_of_probs_values'] = 0
        for c in category_combination:
            selected_set['sum_of_probs_values'] = selected_set['sum_of_probs_values'] + 1/bookmakers_data[c]
        valid_bets = selected_set[selected_set['sum_of_probs_values'] < cut_off]
        
        for id in valid_bets.index:
            bet_weights = get_bet_weights(valid_bets.loc[id, category_combination[0]], 
                                          valid_bets.loc[id, category_combination[1]], 
                                          valid_bets.loc[id, category_combination[2]])
            
            valid_combinations[id] = [category_combination, bet_weights]
    return valid_combinations