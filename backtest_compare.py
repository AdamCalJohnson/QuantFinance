from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/adamjohnson/Documents/GoogleCloudService/gspread-api-394113-fcd586f615d5.json', scope)

client = gspread.authorize(credentials)

#sheet =client.open('Risk Parity Database')

sheet =client.open_by_key('1_XjLk6Vrz7ht5twTK_jARrNf8pBkgVztr8ft5o8ADow')

sheet_instance = sheet.get_worksheet(3)

data = sheet_instance.get_all_values()

portfolio = pd.DataFrame(data)

@app.route('/')
def display_dataframe():
    # Render an HTML template with the DataFrame
    return render_template('portfolio_compare.html', tables=[portfolio[1:].to_html(classes='data', header=False)], titles=portfolio.columns.values)

    #return render_template('dataframe.html', table=df[1:].to_html(classes='data'), titles=df.columns.values)


@app.route('/get_cvar_data', methods=['POST'])
def get_cvar_data():
    if request.method == 'POST':
        # Get the clicked column name from the request
        clicked_col = request.form.get('col')
        
        # You can now use 'clicked_col' to fetch the corresponding data
        # For demonstration, we'll just print it
        print(f"Clicked column: {clicked_col}")
        
        # You can redirect to another Flask route or perform other actions here
        # For example, you can render a new template based on 'clicked_col'
        
    return redirect(url_for('display_dataframe'))


if __name__ == '__main__':
    app.run(debug=True)
