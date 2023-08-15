import pandas as pd
import typing as T

Bet_Balance = T.Literal['Balanced', 'Unbalanced']


def get_avg_margin(bookmaker: pd.DataFrame, 
                   company_name: str,
                   col_name: str = 'return_on_game') -> pd.DataFrame:
    """gets a bookmakers data and calulcates the average yearly margin og bookmaker over different leagues

    Args:
        bookmaker (pd.DataFramem): bookmakers data should include `Div`,`Date`, `return_on_game`
        company_name (str): bookmaker's name
        col_name (str, optional): column name for bookmaker's margin Defaults to 'return_on_game'.

    Returns:
        pd.DataFrame: average yearly margin og bookmaker over different leagues
    """
    bookmaker['Date'] = pd.to_datetime(bookmaker['Date'])
    bookmaker['Year'] = bookmaker['Date'].dt.year
    avg_margin_div_yearly = bookmaker.groupby(['Div', 'Year']).apply(lambda r: r[col_name].mean())
    avg_margin_div_yearly = avg_margin_div_yearly.reset_index()
    avg_margin_div_yearly['Bookmaker'] = company_name
    avg_margin_div_yearly.columns = ['Div', 'Year', 'average_margin', 'Bookmaker']
    return avg_margin_div_yearly


def get_avg_ballanced_unbalanced_margin(bookmaker: pd.DataFrame, 
                                        company_name: str,
                                        balanced_bet: Bet_Balance,
                                        threshold: float,
                                        col_name: str = 'return_on_game') -> pd.DataFrame:
    """gets a bookmakers data and calulcates the average yearly margin og bookmaker over different leagues conditional on balanced bet or not
    balanced bet is that none of the probabilities are above a threshold and unbalanced bet is opposite of that

    Args:
        bookmaker (pd.DataFrame): bookmakers data should include `Div`,`Date`,`ProbH`,`ProbD`,`ProbA` and `return_on_game`
        company_name (str): bookmaker's name
        balanced_bet (Bet_Balance): do we want average margin of balanced or onbalanced bets
        threshold (float): threshold for defining balance in bet probabilities
        col_name (str, optional): column name for bookmaker's margin. Defaults to 'return_on_game'.

    Returns:
        pd.DataFrame: average yearly margin of bookmaker's balanced(unbalanced) bets over different leagues
    """
    
    bookmaker['Date'] = pd.to_datetime(bookmaker['Date'])
    bookmaker['Year'] = bookmaker['Date'].dt.year
    if balanced_bet == 'Balanced':
        bookmaker = bookmaker[(bookmaker['ProbH'] <= threshold) & (bookmaker['ProbA'] <= threshold) & (bookmaker['ProbD'] <= threshold)]
    elif balanced_bet == 'Unbalanced':
        bookmaker = bookmaker[(bookmaker['ProbH'] > threshold) | (bookmaker['ProbA'] > threshold) | (bookmaker['ProbD'] <= threshold)]
    
    avg_margin_div_yearly = bookmaker.groupby(['Div', 'Year']).apply(lambda r: r[col_name].mean())
    avg_margin_div_yearly = avg_margin_div_yearly.reset_index()
    avg_margin_div_yearly['Bookmaker'] = company_name
    avg_margin_div_yearly.columns = ['Div', 'Year', 'average_margin', 'Bookmaker']
    return avg_margin_div_yearly