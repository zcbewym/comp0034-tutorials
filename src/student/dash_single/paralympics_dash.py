import dash_bootstrap_components as dbc
from dash import Dash, html, dcc
from dash import Input, Output
from dash_single.line_chart import line_chart
from dash_single.bar_chart import bar_gender
from dash_single.scatter_map import scatter_geo

# Define a variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Define a variable that contains the meta tags
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

line_fig = line_chart("sports")
bar_fig = bar_gender("summer")
map = scatter_geo()

row_one = dbc.Row([
    dbc.Col(['App name and text']),
])

row_two = dbc.Row([
    dbc.Col(children=[ 
                dbc.Select(
                    options=[
                        {"label": "Events", "value": "events"},  # The value is in the format of the column heading in the data
                        {"label": "Sports", "value": "sports"},
                        {"label": "Countries", "value": "countries"},
                        {"label": "Athletes", "value": "participants"},

                    ],
                    value="countries",  # The default selection
                    id="dropdown-input",  # id uniquely identifies the element, will be needed later for callbacks
                        ),
                dcc.Graph(id="line-chart", figure=line_fig)
                
                    ],
            width=4),

    dbc.Col(children=[
        html.Div(
            [
                dbc.Label("Select the Paralympic Games type"),
                dbc.Checklist(
                    options=[
                        {"label": "Summer", "value": "summer"},
                        {"label": "Winter", "value": "winter"},
                    ],
                    value=["summer"],  # Values is a list as you can select 1 AND 2
                    id="checklist-input",
                            ),
                dcc.Graph(id="bar-chart", figure=bar_fig)
            ],
                )
                    ],
            width={"size": 4, "offset": 2}),
    # 2 'empty' columns between this and the previous column
])

row_three = dbc.Row([
    dbc.Col(children=['line chart'], width=6),
    dbc.Col(children=['bar chart'], width=6),
])

row_four = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="scatter-map", figure=map)
    ], width=8),
    dbc.Col(children=[
            # Column 2 children
                dbc.Card([
                    dbc.CardImg(src=app.get_asset_url("logos/2022_Beijing.png"), top=True),
                    dbc.CardBody([
                        html.H4("Beijing 2022", className="card-title"),
                        html.P("Number of athletes: XX", className="card-text", ),
                        html.P("Number of events: XX", className="card-text", ),
                        html.P("Number of countries: XX", className="card-text", ),
                        html.P("Number of sports: XX", className="card-text", ),
                                ]),
                        ],
                            style={"width": "18rem"},
                        )
    ], width=4),
    # 2 'empty' columns between this and the previous column
])

app.layout = dbc.Container([
    html.H1("Paralympics Data Analytics"),
    html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent congue luctus elit nec gravida."),
    row_one,
    row_two,
    row_three,
    row_four
])


@app.callback(
    Output(component_id='line-chart', component_property='figure'),
    Input(component_id='dropdown-input', component_property='value')
)
def update_line_chart(feature):
    figure = line_chart(feature)
    return figure

@app.callback(
    Output(component_id='bar-chart', component_property='figure'),
    Input(component_id='checklist-input', component_property='value')
)
def update_bar_chart(feature):
    figure = bar_gender(feature)
    return figure

if __name__ == '__main__':
    app.run(debug=True)