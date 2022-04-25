import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from pandas_datareader import DataReader
from datetime import datetime
import pandas as pd

app = dash.Dash()

app.layout = html.Div([
    html.H1('Stock Dashboard'),
    html.Div([html.H3('Enter a stock symbol:',
                      style={'paddingRight':'30px'}),
              dcc.Input(id='my_stock_picker',
                        value="GOOG",
                        style={'fontSize':24, 'width':75}
                        )],style={'display':'inline-block',
                                  'verticalAlign':'top'}),
    html.Div([html.H3('Select a start and end date:'),
              dcc.DatePickerRange(id='my_date_picker',
                                  min_date_allowed=datetime(2004,1,1),
                                  max_date_allowed=datetime.today(),
                                  start_date = datetime(2010,1,1),
                                  end_date = datetime.today())
              ],style={'display':'inline-block'}),
    html.Div([html.Button(id='submit-button',
                          n_clicks=0,
                          children='submit',
                          style={'fontSize':26,'marginLeft':'30px'})
              ],style={'display':'inline-block'}),
    dcc.Graph(id='my_graph',
              figure = {'data':[
                  {'x':[1,2],'y':[3,1]}],
                        'layout':{'title':'Default Title'}})
])




@app.callback(Output('my_graph','figure'),
              [Input('submit-button','n_clicks')],
              [State('my_stock_picker','value'),
               State('my_date_picker','start_date'),
               State('my_date_picker','end_date')])

def update_graph(n_clicks,my_stock_picker,start_date,end_date):
    start = datetime.strptime(start_date[:10],"%Y-%m-%d")
    end = datetime.strptime(end_date[:10],"%Y-%m-%d")
    df = DataReader(my_stock_picker,'yahoo', start ,end)
    fig = {'data':[{'x':df.index,'y':df['Adj Close']}],
    'layout':{'title':my_stock_picker}}
    return fig


if __name__ == '__main__':
    app.run_server()