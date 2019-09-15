import dash
from dash.dependencies import Output,Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import sqlite3
import pandas as pd

#popular topics: google, olympics, trump, gun, usa

app = dash.Dash(__name__)
app.layout = html.Div(
    [   html.H2('Live Twitter Sentiment by Jp'),
        dcc.Input(id='sentiment_term',value='twitter',type='text'),
        dcc.Graph(id='live-graph', animate=False),
        dcc.Interval(
            id='graph-update',
            interval=1*1000,
            n_intervals=0
        ),
    ]
)

@app.callback(Output('live-graph', 'figure'),
             
              [Input(component_id='sentiment_term',component_property='value'),
              Input('graph-update', 'n_intervals')])
            # 
def update_graph_scatter(sentiment_term,n):
    try:
        conn = sqlite3.connect('twitter.db')
        df = pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000", conn ,params=('%'+sentiment_term+'%',))
        df.sort_values('unix', inplace=True)
        #df.set_index('date',inplace=True)
        #df['date'] = pd.to_datetime(df['unix'],unit='ms')
        df['smoothed_sentiment'] = df['sentiment'].rolling(int(len(df)/5)).mean()
        df.dropna(inplace=True)
        
        X = df.unix.values[-100:]
        Y = df.smoothed_sentiment.values[-100:]

        data = plotly.graph_objs.Scatter(
                x=X,
                y=Y,
                name='Scatter',
                mode= 'lines+markers'
                )

        return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]),
                                                    title='Searched Term: {} '.format(sentiment_term))}

    except Exception as e:
        with open('errors.txt','a') as f:
            f.write(str(e))
            f.write('\n')


if __name__ == '__main__':
    app.run_server(debug=True)