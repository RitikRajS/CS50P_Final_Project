import pandas as pd
from project import (accept_number, collect_user_input, validate_funds,
                     load_fund_list, get_fund_information, get_price, get_historical_data,
                     get_investment_info, calculate_stock_ROR, analysis, final_results)
from unittest.mock import patch

# Due to limited API calls, functions associated with API calls were not tested along with
# functions with file I/O

def test_accept_number():
    assert accept_number("Total Fund", 0, 5, lambda _ : 1) == 1

    assert accept_number("Total Fund", 0, 10, lambda _ : 10) == 10

    assert accept_number("Total Fund", 0, float('inf'), lambda _ : 512542424343) == 512542424343

def test_collect_user_input():
    assert collect_user_input(lambda _ : 3) == 3

    assert collect_user_input(lambda _ : 4) == 4

    assert collect_user_input(lambda _ : 2) == 2

    assert collect_user_input(lambda _ : 5) == 5


def test_load_fund_list():

    isinstance(load_fund_list(), set)
    assert load_fund_list() is not None

    names1 = iter(["TSLA", "NVDA", "AAPL", "AMZN"])
    assert next(names1)  in load_fund_list()

    names2 = iter(["CUT-CAD", "SOL1-GBP", "UNI3-CNY"])
    assert next(names2)  in load_fund_list()

    names3 = iter(["VV", "VUSA", "MVPA", "PRMN"])
    assert next(names3)  in load_fund_list()

    names4 = iter(["FLAAX", "LGMNX", "CGEMJX", "SSGHX"])
    assert next(names4)  in load_fund_list()

def test_validate_funds():

    mock_funds = {"TSLA", "NVDA", "AAPL", "AMZN"}
    assert validate_funds(1, mock_funds, input_function= lambda _:"TSLA") == {"TSLA"}

    input1= iter(["TSLA", "NVDA","AMZN"])
    assert validate_funds(3, mock_funds, input_function= lambda _: next(input1)) == {"TSLA", "NVDA","AMZN"}

    input2= iter(["TSLA", "NVDA","AMZN", "AAPL"])
    assert validate_funds(4, mock_funds, input_function= lambda _:next(input2)) == {"TSLA", "NVDA","AMZN", "AAPL"}

    input3= iter(["TSLA", "AAPL"])
    assert validate_funds(2, mock_funds, input_function= lambda _:next(input3)) == {"TSLA", "AAPL"}


def test_get_fund_information(): # API Call
    ...

def test_get_price_1():
    mock_information1 = {'currentPrice' : 100}
    assert get_price(mock_information1) == 100

    mock_information2 = {'navPrice' : 150}
    assert get_price(mock_information2) == 150

    mock_information3 = {'previousClose' : 200}
    assert get_price(mock_information3) == 200

    mock_information4 = {'regularMarketPrice' : 10}
    assert get_price(mock_information4) == 10

    mock_information4 = {}
    assert get_price(mock_information4) == None

def test_get_historical_data(): # API Call
    ...

def test_get_investment_info():
    mock_investments = [{"Symbol" : "NVDA"}, {"Symbol" : "TSLA"}]
    # total money invested, years, investments in each fund respectively
    mock_inputs = iter([200, 20, 100, 100])

    def mock_input(_):
        return (next(mock_inputs))

    assert get_investment_info(mock_investments, input_function = mock_input) == (200, 20, [100, 100])


    mock_investments1 = [{"Symbol" : "AAPL"}, {"Symbol" : "GOOGL"}, {"Symbol" : "META"}]
    # total money invested, years, investments in each fund respectively
    mock_inputs1 = iter([3000, 50, 1000, 1000, 1000])

    def mock_input(_):
        return (next(mock_inputs1))

    assert get_investment_info(mock_investments1, input_function = mock_input) == (3000, 50, [1000, 1000, 1000])

# focus here was not to check the file reading, but the logic
def test_calculate_stock_ROR():
    mock_data = pd.DataFrame({
        'Fund' : ['NVDA', 'NVDA'],
        'Date' : ['2024-06-01', '2024-05-01'],
        'Close Price' : [128, 138]
    })

    # replacing the results.csv with mock_data
    with patch ('pandas.read_csv', return_value = mock_data):
        results = calculate_stock_ROR([250])

    assert 'Average Monthly ROR' in results.columns
    assert 'Each Fund Contribution' in results.columns
    assert list(results['Each Fund Contribution']) == [250]


    mock_data1 = pd.DataFrame({
        'Fund' : ['NVDA', 'NVDA', 'TSLA', 'TSLA'],
        'Date' : ['2024-06-01', '2024-05-01', '2023-06-01', '2023-05-01'],
        'Close Price' : [128, 138, 260, 270]
    })

    with patch ('pandas.read_csv', return_value = mock_data1):
        results1 = calculate_stock_ROR([500, 500])

    assert 'Average Monthly ROR' in results1.columns
    assert 'Each Fund Contribution' in results1.columns
    assert list(results1['Each Fund Contribution']) == [500, 500]

def test_analysis():
    mock_dataframe = pd.DataFrame({
        'Fund' : ['NVDA', 'TSLA'],
        'Average Monthly ROR' : [0.03, 0.025],
        'Each Fund Contribution' : [100, 100]
    })

    results = analysis(mock_dataframe, 5)

    # ensure that the df consists of each funds returns containing the calculated returns
    assert 'Each Fund Returns' in results.columns

def test_final_results(): #File I/O
    ...

def test_results_output(): #File I/O
    ...
