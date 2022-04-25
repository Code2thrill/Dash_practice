import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
from pandas_datareader import DataReader
from datetime import datetime
import plotly.graph_objs as go
import pandas as pd
import numpy
import plotly.express as px
import plotly.offline as pyo
app = dash.Dash()
page = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
wiki_df = page[0]
options = []
for element in wiki_df.index:
    options.append({'label':wiki_df['Security'][element], #get every row of the 'Name' column as key:label
                    'value':wiki_df['Symbol'][element]})

app.layout = html.Div([html.H2('Monte Carlo Analysis'),
                       html.Div([html.H3('Select a stock'),
                           dcc.Dropdown(id='dropdownV2',
                                             options = options,
                                             value = ['GOOG'])],
                                style={'display':'inline-block'}),
                       html.Div([dcc.Input(id='start_price',
                                           value=0,
                                           style={'fontSize':24, 'width':75}
                                           )],style={'display':'inline-block',
                                                     'verticalAlign':'top'}),
                       html.Div([html.Button(id='submit-button2',
                                             n_clicks=0,
                                             children='submit',
                                             style={'fontSize':26,'marginLeft':'30px'})
                                 ],style={'display':'inline-block'}),
                       dcc.Graph(id='monte_carlo_analysis')])


@app.callback(Output('monte_carlo_analysis','figure'),
              [Input('submit-button2','n_clicks')],
              [State('dropdownV2','value'),
               State('start_price','value')])
def update_monte_graph(number_of_clicks,stock,start_price):
    start_price = 100
    stock = 'MMM'
    days = 365
    dt = 1/days
    start = datetime(datetime.now().year-1,datetime.now().month,datetime.now().day)
    end = datetime.now()
    close_df = DataReader(stock,'yahoo', start ,end)['Adj Close']
    stock_returns = close_df.pct_change()
    sigma = stock_returns.std()
    mu = stock_returns.mean()
    def monte_carlo_analysis(start_price,days,mu,sigma):
        price = numpy.zeros(days)
        price[0]=start_price
        shock = numpy.zeros(days)
        drift = numpy.zeros(days)
        for day in range(1,days):
            shock[day]= numpy.random.normal(
                loc = mu * dt,
                scale = sigma * numpy.sqrt(dt))
            drift[day]= mu * dt
            price[day]=price[day-1]+(price[day-1]*(drift[day]+shock[day]))
        return price
    annual_prices =[]
    for run in range(100):
        price = monte_carlo_analysis(start_price, days, mu, sigma)
        annual_prices.append(price)
    numpy_array = numpy.array(annual_prices)
    df_test = pd.DataFrame(numpy_array)
    data = [go.Scatter(x=df_test.columns,y=df_test.loc[a],mode='lines')for a in df_test.index]
    fig = {'data':data,
           'layout':{'title':'Expected Price'}}
    return fig


# data = []
# import matplotlib.pyplot as pyplot
# for trace in range(100):#生成100条线
#     price = monte_carlo_analysis(start_price, days, mu, sigma)
#     trace = go.Scatter(x=days,y=price,mode='lines',name='markers')
# data = [go.Scatter(x=(days,),y=(price,),mode='lines',name='markers') for price in range(10) ]
# print(data)
# return {'data':data,'layout':{'title':'monte_carlo_analysis'}}

if __name__ == '__main__':
    app.run_server()