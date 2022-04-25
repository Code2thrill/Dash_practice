import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np

app = dash.Dash()

#creating data
np.random.seed(42)
random_x =np.random.randint(1,101,100)
random_y =np.random.randint(1,101,100)

#id= will be used as a reference,名字可以随便取
#app.layout 可不是个一般的variable,应该是固定搭配
#html.Div() takes a list which is [dcc.Graph()]
#put 'data' and 'layout' as keys into the figure dictionary and they are match with the plotly formate
app.layout = html.Div([dcc.Graph(id='scatterplot',
                    figure = {'data':[
                            go.Scatter(
                            x=random_x,
                            y=random_y,
                            mode='markers',
                            marker = {
                                'size':12,
                                'color': 'rgb(51,204,153)',
                                'symbol':'pentagon',
                                'line':{'width':2}
                            }
                            )],
                    'layout':go.Layout(title='My Scatterplot',
                                        xaxis = {'title':'Some X title'})}
                    ),
                    dcc.Graph(id='scatterplot2',
                                        figure = {'data':[
                                                go.Scatter(
                                                x=random_x,
                                                y=random_y,
                                                mode='markers',
                                                marker = {
                                                    'size':12,
                                                    'color': 'rgb(200,204,53)',
                                                    'symbol':'pentagon',
                                                    'line':{'width':2}
                                                }
                                                )],
                                        'layout':go.Layout(title='Second Plot',
                                                            xaxis = {'title':'Some X title'})}
                                        )])

if __name__ == '__main__':
    app.run_server()
