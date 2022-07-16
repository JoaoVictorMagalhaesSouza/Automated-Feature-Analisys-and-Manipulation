import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import io,os,sys
from dash import dash_table

dir_import = os.getcwd()
dir_base = f'{dir_import}/..'
sys.path.insert(0, dir_base)

from exploration_analisys import distribuition_graphs, dispersive_statistics

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
                dbc.NavLink("Data Manipulation", href='/manipulation', active="exact"),
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
            
    def read_file(filename):
        return pd.read_csv(filename)

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

            
        ]), df
    @app.callback(
              Output('output-data-upload', 'children'),
              Output('input_data', "data"),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:
            result = parse_contents(list_of_contents[0], list_of_names[0], list_of_dates[0])
            content = [
                result[0]]
            df = result[1]


            return content, df.to_json(date_format='iso')
            
        else:
            return None, None
        
    # @app.callback(
    #     Output('dropdown-exploration', 'options'),
    #     Input('dropdown-exploration-parent', "n_clicks"),
    #     State('input_data','data')
    # )  
    # def change_dropdown_options(n_clicks,data):
    #     if n_clicks is None:
    #         raise dash.exceptions.PreventUpdate
        
    #     options = pd.read_json(data, dtype=dict(TS='datetime64[ns]')).columns
    #     return options
    
    @app.callback(
        Output('graphics-area','children'),
        Input('dropdown-exploration','value'),
        State('input_data',"data")
    )
    def create_exploration_graphics(value,data):
        if value != None:
            data = pd.read_json(data, dtype=dict(TS='datetime64[ns]'))
            
            if value=='Histogram':
                histograms = distribuition_graphs.generate_dist_plots(data)
                statistics = dispersive_statistics.generate_dispersive_statistics(data)
            
            graphichs = []
            for histogram in histograms:
                graphichs.append(dcc.Graph(figure=histogram))
            
            return graphichs

    
    
    
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
        elif pathname == '/exploration':
            return [                
                    dcc.Dropdown(id="dropdown-exploration",options=['Histogram', "Time Series", "Box plots"],
                    placeholder="Choice the type of graph for behavior visualization of input variables"
                    ),

            
            html.Div(
                id='graphics-area',
                children=[]
            )

            ]
            


    return app
    