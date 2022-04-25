import dash
from dash import dcc
from dash import html
import altair
import io
from vega_datasets import data
from dash.dependencies import Input, Output

cars = data.cars()

app = dash.Dash(__name__)

COLUMNS = [
    "Miles_per_Gallon",
    "Acceleration",
    "Displacement",
    "Cylinders",
    "Weight_in_lbs"
]
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label("x-axis"),
            dcc.Dropdown(
                id="x_axis",
                options=[{
                    "label": feature,
                    "value": feature
                }
                    for feature in COLUMNS
                ],
                value="Miles_per_Gallon"
            )
        ]),
        html.Div([
            html.Label("y-axis"),
            dcc.Dropdown(
                id="y_axis",
                options=[{
                    "label": feature,
                    "value": feature
                }
                    for feature in COLUMNS
                ],
                value="Acceleration"
            )
        ])
    ]),
    html.Iframe(
        id="plot",
        height="400",
        width="700",
        sandbox="allow-scripts"
    )

])

@app.callback(
    Output("plot", "srcDoc"),
    [
        Input("x_axis", "value"),
        Input("y_axis", "value")
    ]
)

def make_figure(x_axis, y_axis):

    brush = altair.selection_interval()

    base  = altair.Chart(cars)

    scatter = (
        base.mark_point()
            .encode(x = x_axis,
                    y = y_axis,
                    color = "Origin:N")
            .properties(width     = 300,
                        height    = 300,
                        selection = brush)
    )

    histogram = (
        base.mark_bar()
            .encode(x = altair.X("Horsepower:Q",
                                 bin = True),
                    y = "count()",
                    color = "Origin:N")
            .transform_filter(brush.ref())
    ).properties(height = 300)

    chart = altair.hconcat(scatter, histogram)

    cars_html = io.StringIO()

    chart.save(cars_html, "html")

    return cars_html.getvalue()
if __name__ == '__main__':
    app.run_server(debug=True)