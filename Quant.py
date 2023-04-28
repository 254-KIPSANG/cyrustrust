import pandas as pd
import numpy as np
import yfinance as yf

# Load CSV file containing the list of tickers
tickers_df = pd.read_csv("projectb.csv")
# Extract the tickers from the dataframe and store them in a list
tickers = tickers_df['Ticker'].tolist()

# Define function to calculate Modified Altman Z-Score for a given year


def calculate_mz_score(year, assets, liabilities, current_assets, current_liabilities, retained_earnings, ebit):
    A = (current_assets - current_liabilities) / assets
    B = retained_earnings / assets
    C = ebit / assets
    D = assets - liabilities
    mz_score = 3.25 + 6.56*A + 3.26*B + 6.72*C + 1.05*D
    return mz_score

# Define function to calculate M2B ratio for a given year


def calculate_m2b_ratio(year, market_cap, book_value):
    m2b_ratio = market_cap / book_value
    return m2b_ratio


def create_portfolio(tickers_list, year, num_stocks):
    # Retrieve data for the given year
    data_dict = {}
    for ticker in tickers_list:
        try:
            # Retrieve accounting data from yfinance
            ticker_data = yf.Ticker(ticker)
            balance_sheet = ticker_data.balance_sheet
            income_statement = ticker_data.financials
            info = ticker_data.info

            # Calculate ratios for the given year
            assets = balance_sheet.loc[f'Total Assets {year}'].values[0]
            liabilities = balance_sheet.loc[f'Total Liab {year}'].values[0]
            current_assets = balance_sheet.loc[f'Total Current Assets {year}'].values[0]
            current_liabilities = balance_sheet.loc[
                f'Total Current Liabilities {year}'].values[0]
            retained_earnings = income_statement.loc[f'Retained Earnings {year}'].values[0]
            ebit = income_statement.loc[f'Operating Income or Loss {year}'].values[0]
            market_cap = info['marketCap']
            book_value = balance_sheet.loc[f'Total Stockholder Equity {year}'].values[0]

            mz_score = calculate_mz_score(
                year, assets, liabilities, current_assets, current_liabilities, retained_earnings, ebit)
            m2b_ratio = calculate_m2b_ratio(year, market_cap, book_value)

            # Add data to dictionary
            data_dict[ticker] = {'M-Z Score': mz_score, 'M2B Ratio': m2b_ratio}

        except:
            pass

    # Convert dictionary to dataframe and sort by M-Z Score and M2B Ratio
    data_df = pd.DataFrame.from_dict(data_dict, orient='index')
    data_df.sort_values(by=['M-Z Score', 'M2B Ratio'],
                        inplace=True, ascending=[False, True])

    # Convert dictionary to dataframe and sort by M-Z Score and M2B Ratio
    data_df = pd.DataFrame.from_dict(data_dict, orient='index')
    data_df.sort_values(by=['M-Z Score', 'M2B Ratio'], inplace=True, ascending=[False, True])

    # Create investment portfolio
    portfolio_df = pd.DataFrame(columns=['Ticker', 'Market Value'])
    mz_score_cutoff = data_df['M-Z Score'].mean()
    m2b_ratio_cutoff = data_df['M2B Ratio'].mean()
    for i in range(num_stocks):
        if data_df.iloc[i]['M-Z Score'] > mz_score_cutoff:
            mv = 10000 / num_stocks / data_df.iloc[i]['M-Z Score']
            portfolio_df = portfolio_df.append({'Ticker': data_df.index[i], 'Market Value': mv}, ignore_index=True)
        elif data_df.iloc[i]['M2B Ratio'] > m2b_ratio_cutoff:
            mv = 10000 / num_stocks / data_df.iloc[i]['M2B Ratio']
            portfolio_df = portfolio_df.append({'Ticker': data_df.index[i], 'Market Value': mv}, ignore_index=True)
            
    return (portfolio_df)
portfolio = create_portfolio(tickers, 2020, 5)
print(portfolio)
