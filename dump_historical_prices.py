import sys
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def dump_prices(ticker = 'BTC-USD', start_date = '2021-01-01'):
    # Check existing data
    existing = False
    try:
        df = pd.read_csv('BTC_daily.csv', index_col=0)
        start_date = (datetime.fromisoformat(df.index.to_list()[-1]) + timedelta(days=1)).date().isoformat()
        print(f'Start date set at {start_date}')
        existing = True
    except Exception as e:
        print('Error in reading existing data')
        print(e)


    # Set the date range
    if not existing:
        start_date = "2021-02-01"

    end_date = datetime.today().date().isoformat()

    if start_date == end_date:
        print(f'Start date  same as end date. start_date = {start_date}, end_date = {end_date}.')
        return

    # Retrieve the historical prices
    new_df = yf.download(ticker, start=start_date, end=end_date)
    print(f'Size of new data: {new_df.shape}')

    new_rows = new_df[~new_df.index.isin(df.index)]
    
    if not new_rows.shape[0]:
        print('No new data')
        return
    
    # Append the new rows to the existing dataframe
    updated_df = df.append(new_rows)

    # Write the updated dataframe to the CSV file
    updated_df.to_csv('BTC_daily.csv')
    print('Data dump complete')
    
    return

if __name__ == "__main__":
    dump_prices(ticker = 'BTC-USD')
    