import pymongo 
from pymongo import MongoClient
import pandas as pd
import dash
from dash import html
from dash import dcc 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

connstring = "mongodb+srv://MaseratiMatti:bif4ever@cluster0.pxwo2.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
cluster = MongoClient(connstring)

db = cluster["Omsætning"]

# Create collection - clients
collection = db["Virksomheder"]

# Create a new document
collection.insert_one({"-id":101, "Virksomhed":"Poulette", "Omsætning":"200000", "Årstal":"2022"})
collection.insert_one({"-id":101, "Virksomhed":"Turning Chicken", "Omsætning":"300000", "Årstal":"2022"})
collection.insert_one({"-id":101, "Virksomhed":"Osnacks", "Omsætning":"100000", "Årstal":"2022"})

#delete
#collection.drop()

data = pd.DataFrame(list(collection.find()))

print(data)

fig_omsætning = px.histogram(data, 
    x='Virksomhed', y='Omsætning', title='Omsætning pr Firma',
    hover_data=[],
    labels={'Omsætning':'Omsætning', 'Virksomhed':'firma'})
fig_omsætning.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=45)

dash_app = dash.Dash(__name__)
app = dash_app.server

dash_app.layout = html.Div(children=[

    html.Div(children=[
            dcc.Graph(id="Firmaomsætninger", figure=fig_omsætning)
        ]),
])


if __name__ == '__main__':
    dash_app.run_server(debug=True)
