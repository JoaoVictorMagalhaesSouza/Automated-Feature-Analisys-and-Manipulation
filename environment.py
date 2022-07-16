import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import io
from dash import dash_table

def init_app(server):
    app = dash.Dash(
        __name__, 
        suppress_callback_exceptions=True,
        server=server,
        external_stylesheets=[dbc.themes.MATERIA]
    )
    
    server = app.server
    # styling the sidebar
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    # padding for the page content
    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }
    sidebar = html.Div(
    [
        #html.H2("Bem vindo!", className="display-4"),
        #html.Img(src='data:image/png;base64,{}'.format(test_base64), style={'height':'10%',}),
        html.Hr(),
        # html.P(
        #     "Barra de Navegação", className="lead"
        # ),
        dbc.Nav(
            [
                dbc.NavLink("Apresentation", href="/", active="exact"),
                dbc.NavLink("Load Data", href="/load", active="exact"),
                dbc.NavLink("Exploration Analisys", href="/exploration", active="exact"),
                dbc.NavLink("Correlation Analisys", href='/correlation', active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
    )
    
    content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

    app.layout = html.Div([
        dcc.Location(id="url"),
        dcc.Store(id='input_data'),
        sidebar,
        content,       
        
    ])
    def parse_contents(contents, filename, date):
        content_type, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        return html.Div([
            html.H5(filename),

            dash_table.DataTable(
                df.to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns]
            ),

            html.Hr(),  # horizontal line

            
        ])
    @app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            content = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
        else:
            content = None
        return content
    
    
    
    @app.callback(
    Output("page-content", "children"),
    Input("url","pathname")
    )
    def render_page_content(pathname):
        if pathname == "/load":
            return [
                html.Div([
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            html.A('Select '),
                            'or drag the input dataset here (only .csv)',
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'font-weight': 'bold',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=True
                    ),
                    html.Div(id='output-data-upload'),
                ])

            ]
            


    return app
    