
# Daily Report Potensi Kepadatan BMS

# import package
from dash import Dash, dcc, html, Input, Output

import dash_bootstrap_components as dbc
from dash import dash_table

import pandas as pd
import plotly.graph_objects as go
import numpy as np

import locale

import math

# -----

# Function to generate graph
def generate_graph(data_x, data_y, terminal):

    mean = data_y.mean()
    err = math.sqrt(np.var(data_y))

    mean_plus = mean + err
    mean_min = mean - err

    # Create an area chart for the revenue apsd figures
    fig = go.Figure()

    
    ## function to generate graph
    def line_on_chart(x, mean, color):
            return fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=min(x),
                x1=max(x),
                y0=np.round(mean,2),
                y1=np.round(mean,2),
                line=dict(
                    color=f"{color}",
                    width=2,
                    dash="dashdot",
                )
            )
        )

    def line_legend(mean, text, color):
        return fig.add_trace(
        go.Scatter(
            x=[None],  # This trace will not show any data points
            y=[None],
            mode='lines',
            name=f'{text} = {np.round(mean,2)}',  # The legend label
            line=dict(color=f'{color}', dash='dashdot'),
            showlegend=True,
            legendgroup="legendgroup1",  # Optional: use this if you have multiple shapes/lines you want to group in the legend
            visible='legendonly'
        )
    )


    fig.add_trace(
        go.Scatter(
            x=data_x,
            y=data_y,
            mode='lines+markers',
            line=dict(color='rgb(255, 45, 165)', width=2.5),
            marker=dict(color='rgb(255, 45, 165)', size=7),
            name='Perkiraan Jumlah Penumpang',
            hovertemplate=f"Terminal {terminal}<br>""Jumlah Penumpang: %{y}",
        )
    )

    # Format the layout
    fig.update_layout(
        # title=f"Prakiraan Jumlah Penumpang Bus<br>Terminal {terminal} CGK",
        xaxis_title='Jam',
        yaxis_title='Jumlah Penumpang',
        font=dict(  # Default font for other text elements
            family='Poppins, sans-serif',
            size=12,
            color='black'),
        title_x=0,
        xaxis=dict(
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='gray',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Poppins, sans-serif',
                size=12,
                color='gray',
            ),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            zeroline=False,
            showline=False,
            showticklabels=True,
            tickfont=dict(
                family='Poppins, sans-serif',
                size=12,
                color='gray',
            ),
        ),
        template="plotly_white",
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(r=10, l=10, b=0, t=10, pad=5),
    )

    line_on_chart(data_x, mean_plus, 'red')
    line_legend(mean_plus, "batas atas", 'red')

    line_on_chart(data_x, mean, 'orange')
    line_legend(mean, "rata-rata", 'orange')

    line_on_chart(data_x, mean_min, 'green')
    line_legend(mean_min, "batas bawah", 'green')


    fig.update_layout(
        width=1000,   # Width in pixels
        height=300,  # Height in pixels
    )
    return fig

# --------

# Load the dataset with error handling
try:
    url = "https://raw.githubusercontent.com/faridazhr/datasource-dashboard-bms/main/passenger_prediction_hourly.csv"
    df = pd.read_csv(url, delimiter=';')
except Exception as e:
    print(f"Error loading data: {e}")

# Convert 'TIME' column to datetime, specifying format to optimize performance
try:
    df['TIME'] = pd.to_datetime(df['TIME'], errors='coerce')
except Exception as e:
    print(f"Error converting 'TIME' column: {e}")

df = df.dropna(axis=1, how='all')
df = df.dropna(how='all')

# Color Code
green = '#65D56A'
yellow = '#FFF494'
red = '#E95F5F'
navyblue = '#19274F'
cyan = '#00B5E3'

# Get date from data
tanggal = df['TIME'].unique()[0]

# Set the locale to Indonesian
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.utf8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'C')

# Format the date as per Indonesian locale
hari_ini = tanggal.strftime("%A, %d %B %Y")

# Start page content
app = Dash(__name__,
           external_stylesheets=[
               dbc.themes.BOOTSTRAP, 
               "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap",
           ])

server = app.server

import dash_bootstrap_components as dbc
from dash import html

app.layout = dbc.Container([
    dbc.Row([
        html.Div(
            children=[
                    dbc.Row([
                        dbc.Col(
                            children=[
                                dbc.Row([
                                    html.H1("Daily Report", style={
                                        "textAlign": "left",
                                        'color': 'white',
                                        'font-size': '18px',
                                        'font-family': 'Poppins',
                                        'font-weight': 'semibold',
                                        'margin-top': '20px',
                                        'margin-left': '30px'
                                        }),
                                    ]),
                                dbc.Row([
                                    html.H2("Prediksi Jumlah Penumpang Bus", style={
                                        "textAlign": "left",
                                        'color': 'white',
                                        'font-size': '28px',
                                        'font-family': 'Poppins',
                                        'font-weight': 'bold',
                                        'margin-left': '30px',
                                        'padding-bottom': '5px'
                                    })
                                ])
                            ], 
                            width=6
                        ),
                        dbc.Col(
                            children=[
                                html.Img(
                                    src='https://raw.githubusercontent.com/faridazhr/datasource-dashboard-bms/main/assets/Logo%20EzBus-white%20(low).png',
                                    style={
                                        'height': '35px',
                                        'margin-right': '10px',
                                        'margin-top': '40px'
                                    }),
                                html.Img(
                                    src='https://raw.githubusercontent.com/faridazhr/datasource-dashboard-bms/main/assets/LOGO%20PRIMER%20APSD%20(1).png',
                                    style={
                                        'height': '50px',
                                        'margin-right': '20px',
                                        'margin-top': '20px'
                                    }),
                            ],
                            width=6, style={
                                'textAlign': 'right', 
                                'display': 'inline-block',
                                }
                        ),
                    ], justify="between"),  # Bootstrap will space the columns as needed
                ],
                style={
                    "width": "100%",
                    "background-color": navyblue,
                    "color": "white",
                    "height": '100px'
                }
            )
    ]),
    
    dbc.Row([
        dbc.Col(
        [
            html.Div(
                className='terminal-dropdown',
                children=[
                    terminal_input := dcc.Dropdown(
                        options=[
                            {'label': 'Terminal 1', 'value': 1},
                            {'label': 'Terminal 2', 'value': 2},
                            {'label': 'Terminal 3', 'value': 3},
                        ],
                        value=3,
                        style={
                            'width': '130px', 
                            'font-size': '16px', 
                        },
                        clearable=False,  
                        className='custom-dropdown'
                    )
                ],
                style={
                    'display': 'inline-block', 
                    'width': '150px',
                    'margin-top': '30px',
                    'margin-left': '30px',
                }
            ),
            html.P(
                "Bandara Soekarno-Hatta",
                style={
                    'display': 'inline-block', 
                    "textAlign": "left",
                    'color': navyblue,
                    'font-size': '24px',
                    'font-family': 'Poppins',
                    'font-weight': 'bold',
                    'margin-top': '30px',
                    'margin-left': '5px',
                }
            ),
        ],
        width=6,
        style={
            'display': 'flex',
            'flex-direction': 'row',
            'justify-content': 'left',
            'align-items': 'left', 
        }),

        dbc.Col([
            html.H2(hari_ini, style={
                "textAlign": "right",
                'color': navyblue,
                'font-size': '26px',
                'font-family': 'Poppins',
                'font-weight': 'medium',
                'margin-right': '30px',
                'margin-top': '30px'
            }),
            ], width=6),
    ]),
    
    dbc.Row([
        html.Div("Prediksi Total Penumpang: ",
                style={
                    "width": "auto",
                    "color": navyblue,
                    "font-family": "'Poppins', sans-serif",                
                    "font-weight": "bold",
                    "font-size": "18px",
                    "display": "inline-block",
                    'margin-left': '30px',
                    'margin-top': '20px',
                }),
         html.Div(id='total_penumpang',
            style={
                "width": "auto",
                "background-color": navyblue,
                "color": "white",
                "font-family": "'Poppins', sans-serif",                
                "font-weight": "bold",
                "font-size": "14px",
                "padding": "7px 10px",
                "border-radius": "5px",
                "display": "inline-block",
                'margin-left': '5px',
                'margin-top': '15px',
            }),
    ],style={
            'display': 'flex',
            'flex-direction': 'row',
            'justify-content': 'left',
            'align-items': 'left', }),

    dbc.Row([

        dbc.Col([

            dbc.Col([
                html.Div(
                    "Tren Prediksi Jumlah Penumpang Bus per Jam",
                    style={
                        "width": "auto",
                        "color": navyblue,
                        "font-family": "'Poppins', sans-serif",                
                        "font-weight": "regular",
                        "font-size": "18px",
                        "display": "inline-block",
                        'margin-left': '30px',
                        'margin-top': '20px',
                    }),                    
            ]),
            
            dbc.Row([
                gr := dcc.Graph(figure={})
            ]),

            html.Div(
                style={
                    'margin-left': '30px',
                },
                children=[   
                html.Div(
                    id='volume_penumpang_tinggi',
                    style={
                        "width": "auto",
                        "background-color": navyblue,
                        "color": "white",
                        "font-family": "'Poppins', sans-serif",                
                        "font-weight": "bold",
                        "font-size": "20px",
                        "padding": "7px 10px",
                        "border-radius": "10px",
                        "display": "inline-block",
                        'margin-bottom': '5px',
                    }), 
                           
                html.P(
                    style={
                        'fontSize': '18px',
                        'font-family': 'Poppins',
                        'fontWeight': 'medium'
                                },
                    children=[
                        html.Span('Periode', 
                                  style={'fontWeight': 'bold'}), 
                        ' yang diperkirakan mengalami  ',
                        html.Span('volume penumpang cukup tinggi', 
                                  style={'fontWeight': 'bold'}),
                            ]),
                ]),
            html.Div(
                style={
                    'margin-left': '30px',
                    'margin-top': '10px',
                },
                children=[
                    # html.Div(time_divs),   
                    html.Div(id="jam_sibuk", children=[]),                    
                    html.P(
                        style={
                        'fontSize': '18px',
                        'font-family': 'Poppins',
                        'fontWeight': 'medium'
                                },
                    children=[
                        html.Span('Jam-jam sibuk', 
                                  style={'fontWeight': 'bold'}), 
                        ' dengan proyeksi  ',
                        html.Span('lonjakan penumpang', 
                                  style={'fontWeight': 'bold'}),
                            ]
                )
                ]
            ),
        html.Div(
                style={
                    'margin-left': '30px',
                    'margin-top': '10px',
                },
                children=[
                    html.P(
                        style={
                        'fontSize': '18px',
                        'font-family': 'Poppins',
                        'fontWeight': 'medium'
                                },
                    children=[
                        'Pada periode waktu tersebut, ',
                        html.Span('diperlukan perhatian khusus', 
                                  style={'fontWeight': 'bold'}), 
                        ' oleh tim operasional yang bertugas',
                         ]
                )
                ]
            )
        ],width=8,),
        
        dbc.Col([
            html.Div(
                id='table',
                style={}
                ),
        ],width=4, align='left')
    ]),

    

    dbc.Row([
        html.Div(children=[
            html.Div(' '),  # Empty content, only used for the shape
        ],
        style={
            'backgroundImage': f'linear-gradient(to right, {navyblue}, {cyan})',  # Gradient background
            'position': 'fixed',        # Fix it to the bottom of the page
            'bottom': '0',              # Stick to the bottom
            'width': '100%',            # Full width
            'height': '15px',          # Height of the shape
            # 'clipPath': 'polygon(0 85%, 100% 0, 100% 100%, 0 100%)',  # Clip to create a wave shape
            'zIndex': '9999',           # Ensure it's above other content
        })
    ])

], fluid=True, style={'fontFamily': 'Poppins'})



@app.callback(
    Output(gr, component_property='figure'),
    Input(terminal_input, component_property='value'),
)

def update_graph(value):
    df_temp = df.copy()
    df_temp['TIME'] = pd.to_datetime(df_temp['TIME'], errors='coerce')
    df_temp['TIME'] = df_temp['TIME'].dt.strftime('%H:%M')
    fig =  generate_graph(data_x=df_temp['TIME'], data_y=df_temp[f'T{value}'], terminal=value)
    return fig

@app.callback(
    Output('total_penumpang', component_property='children'),
    Input(terminal_input, component_property='value'),
)

def update_total_penumpang(value):
    df_temp = df.copy()
    total = df_temp[f'T{value}'].sum()
    return f'{total:,} penumpang'.replace(",", ".")

@app.callback(
    Output('jam_sibuk', component_property='children'),
    Input(terminal_input, component_property='value'),
)

def update_jamsibuk(terminal):
    mean = df[f'T{terminal}'].mean()
    err = math.sqrt(np.var(df[f'T{terminal}']))

    mean_plus = mean + err
    mean_min = mean - err

    list_ovtime = df['TIME'][df[f'T{terminal}'] > (mean_plus)].dt.strftime('%H:%M').values
    formatted_ovtime = [time_value for time_value in list_ovtime]

    time_divs = [
        html.Div(
            time,
            style={
                "width": "auto",
                "background-color": cyan,
                "color": "white",
                "font-family": "'Poppins', sans-serif",
                "font-weight": "bold",
                "font-size": "16px",
                "padding": "7px 10px",
                "border-radius": "10px",
                "display": "inline-block",
                'margin-bottom': '5px',
                'margin-right': '5px',
            }
        ) for time in formatted_ovtime
    ]
    return time_divs

@app.callback(
    Output('volume_penumpang_tinggi', component_property='children'),
    Input(terminal_input, component_property='value'),
)

def update_volumetinggi(terminal):
    # Calculate the mean
    mean_value = df[f'T{terminal}'].mean()

    # Filter rows greater than the mean
    filtered_df = df[df[f'T{terminal}'] > mean_value]

    # Extract the first and last formatted times
    time_ = filtered_df['TIME'].dt.strftime('%H:%M').iloc[[0, -1]].tolist()
    
    return f"{time_[0]} – {time_[1]}",

@app.callback(
    Output('table', component_property='children'),
    Input(terminal_input, component_property='value'),
)

def update_table(terminal):
    mean = df[f'T{terminal}'].mean()
    err = math.sqrt(np.var(df[f'T{terminal}']))

    mean_plus = mean + err
    mean_min = mean - err

    color_seq = []

    for value in df[f'T{terminal}'].values:
        if value <= mean_min:
            color_seq.append(green)
        elif value < mean_plus:
            color_seq.append(yellow)
        else:
            color_seq.append(red)
    
    df_temp = df.copy()
    df_temp['TIME'] = df_temp['TIME'].dt.strftime('%H:%M')
        
    return dash_table.DataTable(
                data=df_temp.to_dict('records'),
                columns=[
                    {'name': 'Pukul', 'id': 'TIME', 'type': 'text'},
                    {'name': 'Jumlah Penumpang', 'id': f'T{terminal}', 'type': 'numeric'}
                ],
                style_cell={
                    'textAlign': 'center',
                    'fontFamily': 'Poppins',
                    'fontSize': '16px',
                    'height': '30px',
                },
                style_header={
                    'backgroundColor': '#19274F',
                    'fontFamily': 'Poppins',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': i},
                        'backgroundColor': color_seq[i],  # Apply row color from color_seq
                        'color': '#19274F'  # Navyblue font color for the data rows
                    } for i in range(len(df)) ] + 
                [
                    {
                        "if": {"column_id": "TIME"},
                        "width": "100px"
                    },
                    {
                        "if": {"column_id": f'T{terminal}'},
                        "width": "180px"
                    },
                ],
                style_table={
                    'width': '100%', 
                    'height': '590px',                    
                    'minHeight': '580px',  # Limit table height
                    # 'maxHeight': '590px',  # Limit table height
                    'overflowY': 'scroll'  # Enable vertical scroll
                    }, 
                fixed_rows={'headers': True},  # Freeze the header row
                fill_width=False
                )

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_ui=False)