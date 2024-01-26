from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials


app = Flask(__name__)

def save_to_google_sheets(df):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/adamjohnson/Documents/GoogleCloudService/gspread-api-394113-fcd586f615d5.json', scope)

    client = gspread.authorize(credentials)

    sheet =client.open_by_key('1_XjLk6Vrz7ht5twTK_jARrNf8pBkgVztr8ft5o8ADow')

    sheet_instance = sheet.get_worksheet(2)

    #for idx, row in enumerate(df.itertuples(index=True), start=1):
        # idx is row number, considering a header
        #sheet_instance.append_row([idx] + list(row))
    set_with_dataframe(sheet_instance,df,include_index=True)

# Create a DataFrame with tickers as index and 1 column for share values
stocks = pd.DataFrame(columns=['Shares'])

@app.route('/')
def home():
    return render_template('index.html', stocks=stocks)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    # Get stock information from form and add to DataFrame
    for i in range(1, 16):
        ticker = request.form.get(f'ticker{i}')
        shares = request.form.get(f'shares{i}')
        stocks.loc[ticker] = [shares]
    save_to_google_sheets(stocks)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)