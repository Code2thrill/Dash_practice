import dash
from dash import html
from dash import dcc
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_extensions as de
from datetime import datetime
from pandas_datareader import DataReader

page = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
df = page[0]
# print(df)
# print(df.head())
# print(df.info())
# print(df.columns)
# print(df['Security']) #eg. get the first row of the name column

app = dash.Dash()

options = []
for element in df.index:
    options.append({'label':df['Security'][element], #get every row of the 'Name' column as key:label
                    'value':df['Symbol'][element]}) #get every row of the 'Symbol' column as key:value

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.H2('Select a stock'),
    dcc.Dropdown(id='dropdown',
              options = options,#the dictionary we created above with lable and value keys to match the dash options format
              value= ['GOOG'],#default value is 'GOOG'
              multi=True),#user can select multiple values
    html.Div([
        html.H2('Select Date'),
        dcc.DatePickerRange(id='datepicker',
                            min_date_allowed= datetime(2010,1,1),
                            max_date_allowed= datetime.today(),
                            start_date=datetime(2020,1,1),
                            end_date = datetime.today()
                            )
    ]),
    html.Div([
        html.Button(
            id = 'submit-button',
            n_clicks= 0,
            children='Submit',
            style={'fontSize':24,'width': '15%', 'height': '50px'}
        )
    ]),
    dcc.Graph(id='stock-graph')
])



@app.callback(Output('stock-graph','figure'),
              [Input('submit-button','n_clicks')],
              [State('dropdown','value'),
               State('datepicker','start_date'),
               State('datepicker','end_date')])
def update_graph(number_of_clicks,stocks,start_date,end_date):
    start = datetime.strptime(start_date[:10],"%Y-%m-%d")
    end = datetime.strptime(end_date[:10],"%Y-%m-%d")
    data = []
    for stock in stocks:
        stock_df = DataReader(stock,'yahoo',start,end)
        dates = []
        for row in range(len(stock_df)):
            new_date = str(stock_df.index[row])[0:10]
        #yahoo df dates are index as int so covers them to str and choice [0:10]
        #then creates a new column called Date from dates list
            dates.append(new_date)
        stock_df['Date'] = dates
        data.append({
            'x':stock_df['Date'],
            'y':stock_df['Adj Close'],
            'name': stock
        })
    figure = {
        'data':data,
        'layout':{
            'title':'Stock Closing Prices'
        }
    }
    return figure


if __name__=='__main__':
    app.run_server(debug=True)