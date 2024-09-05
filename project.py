import datetime
import requests
import pandas as pd
import csv
import yfinance as yahooFinance
import sys
import time
from tabulate import tabulate
import inflect
import math


def main(input_function=input, output_function=print):

    total_funds = collect_user_input(input_function)
    fund_list = load_fund_list()
    fund_names = validate_funds(total_funds, fund_list, input_function)
    new_investments = get_fund_information(fund_names)
    new_investments = get_historical_data(new_investments)
    total_money, years, each_investment = get_investment_info(
        new_investments, input_function
    )
    dataframe_ROR_m = calculate_stock_ROR(each_investment)
    dataframe_ROR_m = analysis(dataframe_ROR_m, years)
    results = final_results(
        fund_names, total_money, years, new_investments, dataframe_ROR_m
    )
    results_output(results, input_function, output_function)


def accept_number(
    prompt="Fund Numbers: ", min_value=0, max_value=float("inf"), input_function=input
):
    """
    Asks the user for a number and checks it
    """
    while True:

        try:

            number = float(input_function((prompt)))
            if min_value <= number <= max_value:
                return number

            else:
                print(f"\nPlease enter a number between {min_value} and {max_value}\n")

        except ValueError:
            print("\nPlease Enter a Valid Number \n")


def collect_user_input(input_function):
    """
    Collects the number of stocks that the user will invest in
    """

    total_funds = accept_number(
        "\nHow many Stocks or Funds will you Invest in? \n \n",
        min_value=1,
        max_value=5,
        input_function=input_function,
    )
    return total_funds


def load_fund_list():
    """
    Gets all the stock/etf/crypto/mutual fund names from all the CSV files
    """

    # set data type to remove an repeated symbols
    fund_list = set()

    for file_name in ["listing_status.csv", "funds.csv", "cryptos.csv"]:
        with open(file_name) as file:
            reader = csv.reader(file)
            for row in reader:
                fund_list.add(row[0])  # adding symbols

    return fund_list


def validate_funds(total_funds, fund_list, input_function=input):
    """
    Asking user for the fund names and validating it against the existing funds in CSV files
    """

    valid_funds = set()

    while len(valid_funds) < total_funds:

        fund = (
            input_function("\nWhich Fund/Stock? \n \n").upper().strip()
        )  # getting the fund/stock
        if fund in fund_list and fund not in valid_funds:
            valid_funds.add(fund)
        else:
            print("\nPlease Enter a Valid Name \n")

    return valid_funds


def get_fund_information(fund_names):
    """
    Get the stockmarket information of the validated funds using Yahoo Finance module
    """

    new_investments = []
    funds_to_remove = set()

    for fund in fund_names:
        try:
            get_info = yahooFinance.Ticker(fund)  # to fetch the data from the fund
            time = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
            info = get_info.info

            investment = {
                "Time & Date": time,
                "Symbol": info.get("symbol", fund),
                "Name": info.get("longName", "N/A"),
                "Quote Type": info.get("quoteType", "N/A"),
                "Price": get_price(info),
                "Currency": info.get("currency", "N/A"),
            }

            if investment["Price"] is not None:
                new_investments.append(investment)

            else:
                print(f"\nDue to Limited Data, {fund} is not available\n")
                funds_to_remove.add(fund)

        except Exception as e:
            print(f"\nAn error occurred while fetching data for {fund}: {e}\n")

    fund_names.difference_update(funds_to_remove)

    new_investments = sorted(
        new_investments, key=lambda investment: investment["Symbol"]
    )
    print(
        f"\n{tabulate(new_investments, headers = 'keys', tablefmt = 'outline', numalign = 'right', floatfmt = '.2f')}\n"
    )
    return new_investments


def get_price(info):
    """
    Get price for the required fund for ETFs, Stocks, Mutual Funds and Crypto
    """

    for key in ["currentPrice", "navPrice", "previousClose", "regularMarketPrice"]:
        if key in info:
            return info[key]
    return None


def get_historical_data(new_investments):
    """
    Getting the historical data for an investment using Alpha Vantage
    """

    API_key = "YT7DHM1KJ0857LUH"  # Personalised Key from AlphaVantage website
    functions = "TIME_SERIES_MONTHLY_ADJUSTED"

    try:
        with open(
            "results.csv", "w", newline=""
        ) as file1:  # To write down the historical prices
            writer = csv.writer(file1)
            writer.writerow(["Fund", "Date", "Close Price"])
            # due to limited database, these funds will be removed from portfolio
            funds_to_remove = []

            for new_investment in new_investments:
                symbol = new_investment["Symbol"]
                url = f"https://www.alphavantage.co/query?function={functions}&symbol={symbol}&apikey={API_key}"
                r = requests.get(url)
                data = r.json()
                time.sleep(10)  # waiting for 10 secs between requests

                if "Monthly Adjusted Time Series" in data:
                    monthly_data = data["Monthly Adjusted Time Series"]
                    for date, price in monthly_data.items():
                        close_price = price["5. adjusted close"]
                        writer.writerow([symbol, date, close_price])

                else:
                    print(f"\nDue to limited database, {symbol} is not available\n")
                    funds_to_remove.append(new_investment)

            initial_number = len(new_investments)

            for fund in funds_to_remove:
                new_investments.remove(fund)

            if not new_investments:
                sys.exit(f"\nThe portfolio consists of no funds\n")
            elif len(new_investment) < initial_number:
                print(
                    "\nDue to limited data, some funds were removed. Proceeding with remaining funds\n"
                )
        return new_investments

    except requests.exceptions.RequestException as e:
        sys.exit("\nAn unexpected error has occured, Please try again later\n")

    except Exception as f:
        sys.exit("\nPlease Wait for a few minutes as the API limit is exceeded\n")


def get_investment_info(new_investments, input_function=input):
    """
    Getting investment details from  the user for each fund
    """

    total_money = accept_number(
        "\nHow much $ will you be investing in total per month? \n",
        input_function=input_function,
    )
    years = math.trunc(
        accept_number(
            "\nFor how many years will you invest? \n", input_function=input_function
        )
    )  # to ignore decimal input

    each_investment = []

    while True:

        each_investment = []

        for new_investment in new_investments:
            each = accept_number(
                f"\nHow much will you invest in {new_investment['Symbol']}: ",
                input_function=input_function,
            )
            each_investment.append(each)
            new_investment["Monthly Investment"] = each

        if sum(each_investment) == total_money:
            break

        else:
            print(
                f"\nThe sum of each investment was {sum(each_investment)}, and it does not equate to the total investment of {total_money} \n"
            )

    return total_money, years, each_investment


def calculate_stock_ROR(each_investment):
    """
    To calculate the Stock ROR of each fund from the data obtained using Alpha Vantage
    """

    data = pd.read_csv("results.csv")

    # converting date into datetime series
    data["Date"] = pd.to_datetime(data["Date"])

    # Sorting out the data
    sorted_data = data.sort_values(by=["Fund", "Date"])

    # group the same fund together, and calculate the diff in monthly ror
    sorted_data["Monthly ROR"] = sorted_data.groupby("Fund")["Close Price"].pct_change()

    # to remove NaN values
    sorted_data.dropna(subset=["Monthly ROR"], inplace=True)

    avg_monthly_ROR = sorted_data.groupby("Fund")["Monthly ROR"].mean()
    dataframe_ROR_m = avg_monthly_ROR.reset_index()  # converting series to df
    dataframe_ROR_m.columns = ["Fund", "Average Monthly ROR"]
    dataframe_ROR_m["Each Fund Contribution"] = each_investment

    return dataframe_ROR_m


def analysis(dataframe_ROR_m, years):
    """
    Based on the previous data, analyse the final returns for each fund
    """

    monthly_returns = []

    for i in range(len(dataframe_ROR_m)):
        monthly_ROR = dataframe_ROR_m["Average Monthly ROR"][i]
        months = int(years * 12)
        pv = dataframe_ROR_m["Each Fund Contribution"][i]
        fv = pv * ((1 + monthly_ROR) ** months - 1) / monthly_ROR
        monthly_returns.append(fv)

    dataframe_ROR_m["Each Fund Returns"] = monthly_returns

    return dataframe_ROR_m


def final_results(fund_names, total_money, years, new_investments, dataframe_ROR_m):
    """
    The final results layout
    """

    p = inflect.engine()

    results = (
        f"\nThe portfolio of {p.join(sorted(fund_names))} with a monthly total contribution of {total_money} for {years} years would result in \n"
        f"\n{tabulate(new_investments, headers='keys', tablefmt='outline', numalign='right', floatfmt='.2f')}\n"
        f"\nThe average ROR from each fund will be as follow\n"
        f"\n{tabulate(dataframe_ROR_m, headers = 'keys', tablefmt='outline', numalign='right', floatfmt='.2f', showindex = False)}\n"
    )

    results = (
        results
        + f"\nTherefore, the total returns from this portfolio after {years} years would be : ${dataframe_ROR_m['Each Fund Returns'].sum():,.2f}\n"
    )
    return results


def results_output(results, input_function=input, output_function=print):
    """
    User to get an option whether to save the output in another file or not
    """
    while True:
        saving_file = (
            input_function("Would you like to save the results? (Y/N) \n")
            .strip()
            .capitalize()
        )

        if saving_file == "N":
            output_function(results)
            break

        elif saving_file == "Y":

            try:
                file_name = (
                    input("Please insert the file name: \n").strip().capitalize()
                ) + ".txt"
                with open(file_name, "w") as file_2:
                    file_2.write(results)
                    break

            except ValueError:
                print("Please try again \n")

        else:
            print("Please enter a valid response i.e. Y or N \n")


if __name__ == "__main__":
    main()
