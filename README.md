# STOCK MARKET PORTFOLIO ANALYSER

#### Video Demo:  <[URL HERE](https://youtu.be/liAA2IgPy60)>
---
## Description:

 **Stock Market Portfolio Analyser** aims to predict how a portfolio would perform using the Future Value Model. It prompts the user to create a portfolio of up til 5 different investments, validates them, acquires the financial data of respective investments and analyses the returns from the portfolio over time. This is based on user ***monthly total contribution***, ***each investment contribution*** and ***time frame***. The portfolio could include **Stocks**, **ETF**, **Mutual Funds**, and **Crypto**.

---
## Libraries:

Folowing libraries were employed

* ***Datetime*** - To convert strings into datetime objects
* ***Requests*** - To make an HTTP request to the AlphaVantage module
* ***Pandas*** - To convert data into data frame and manipulate and analyse
* ***CSV*** - To read and write CSV files
* ***yahooFinance*** - To access stock market data
* ***sys*** - To prematurely exit the code if conditions are not met
* ***tabulate*** - To display data in tabular form
* ***inflect*** - To convert numbers into words
* ***math*** - To perform mathematical operations

---
## Functionalities:


 The project follows the following logic for the user's convenience.

* Getting investment information from the user

  * First, prompt the user to select the number of investments to invest between **1 and 5**.
  * Loads all the investment tickers from CSV files within a set, and validates it against the ticker symbol entered by the user. P.S - ***CSV files were used to limit the number of API calls made.***

* Fetching the financial data of the selected investments

  * Once the investments were validated, yahoofinance module was used to get the basic information about the symbol such as current price, full name, quote type, and currency.
  * To avoid exceeding the limited API calls, the AlphaVantage module was used in conjunction with yahoofinance, aimed to collect the historical prices for analysis.

* Getting further details from the user

  * Details such as total money invested per month, time, and investment towards each investment.

* Analysis

  * Manipulating the obtained historical data using pandas and calculating the rate of return from each investment.
  * Using ***Future Value Model*** to calculate the future returns from each fund.

* Results

  * Based on user choice, the output/results of the script would either be saved to a file or displayed directly in the terminal.
  * The final results would contain details of the portfolio such as name, symbol, and returns from each investment

---
## Installation

The project can be cloned by

```bash
git clone https://github.com/RitikRajS/Stock-Market-Portfolio-Analyser.git
```

The packages that were listed in the requirements.txt file can be installed by

```bash
pip install -r requirements. txt
```

The libraries can be installed by

```bash
pip install datetime requests pandas csv yfinance sys tabulate inflect math
```

 The script comes along with three additional CSV files that the user would be required to have without any changes to the file names and save in the same directory before running the program. The files are **crypto.csv**, **funds.csv**, and **list_status.csv**. Each CSV file consists of a list of crypto, mutual funds, ETF/stocks symbols or tickers and its respective company names, respectively. ***In case of a change, please refer to the configuration section.***

 To save the file in the same directory, the user can simply drag the file from a local folder into the VS code directory.

 These CSV files can be downloaded from the following links

 a . **crypto.csv** - [Link here](https://github.com/JerBouma/FinanceDatabase/blob/main/database/cryptos.csv)

[![Crypto-Screenshot.png](https://i.postimg.cc/0QB89MSL/Crypto-Screenshot.png)](https://postimg.cc/wyDKVB0V)

 b. **funds.csv** - [Link here](https://github.com/JerBouma/FinanceDatabase/blob/main/database/funds.csv)

 [![Funds-Screenshot.png](https://i.postimg.cc/ZqqnZhgv/Funds-Screenshot.png)](https://postimg.cc/pmgRY3PP)

 c. **list_status.csv** - [Link here](https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo)

**It is worth noting that the crypto and funds CSV files were further edited on Microsoft excel to remove the raw data i.e. the summary, exchange and market columns. However, if the user chooses not to do so, the program will still work without any issues**

---
## Usage

1. Run the main Script

```bash
python project.py
```

2. Enter the number of Investments between 1-5.

3. Enter the investment symbol of interest.

4. Enter the total money that will be invested per month, the number of years that the investment will continue and the contribution towards each investment

5. Will have an option to save the results in another file
---
## Configuration

The script can be configured using following methods

* AlphaVantage API Key

    ```bash
    API_key = 'PERSONALISED_ALPHA_VANTAGE_API_KEY'
    ```

    The API key would be required to replace with your own personalised API key, which can be found [here](https://www.alphavantage.co/support/#api-key).

* API call

    To avoid exceeding the call limit for AlphaVantage free tier subscription, the script required a delay in between the calls, which could be adjusted.

    ```bash
    time.sleep(10)
    ```

* CSV files

    The three CSV files are required to be in the same directory as the script, and in case of a change in name, the script would need to be updated

    ```bash
        for file_name in ["listing_status.csv", "funds.csv", "cryptos.csv"]:
        with open(file_name) as file:
            reader = csv.reader(file)
            for row in reader:
                fund_list.add(row[0]) # adding symbols
    ```

---
## Improvements

* The script could include a section to directly access the CSV files from the Github repository without the need for the user to download the CSV files separately, and make changes in an Excel before running the script.

* Use of a paid subscription for AlphaVantage or yahooFinance would increase the reliability and limitation of the available investment options. It will also increase the limited API call from 5 API calls per min to 25 calls per min.

* Use of a more sophisticated prediction model such as a linear regression model would provide more accurate prediction.

* The inclusion of a graphical representation in the final results would aid in a better understanding of portfolio performance.
