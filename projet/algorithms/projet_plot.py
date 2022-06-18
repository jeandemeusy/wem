from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import json
from pprint import pprint
import plotly.graph_objects as go


def print_full(x):
    """
    Prints the full content of a pandas dataframe
    """
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 2000)
    pd.set_option("display.float_format", "{:20,.2f}".format)
    pd.set_option("display.max_colwidth", None)
    print(x)
    pd.reset_option("display.max_rows")
    pd.reset_option("display.max_columns")
    pd.reset_option("display.width")
    pd.reset_option("display.float_format")
    pd.reset_option("display.max_colwidth")


app = Dash(__name__)

with open("topics.json") as f:
    data = json.load(f)

df = pd.DataFrame([data])

df_graph = pd.DataFrame(df["mdsDat"][0])
df_graph['Freq'] = np.log(df_graph['Freq']+1)

df_bar = pd.DataFrame(df["tinfo"][0])
df_bar.to_json('test.json')
# df_bar_split = pd.DataFrame({'Term': df["tinfo"][0]['Term'], 'Category': df['tinfo'][0]['Category']})
# print(df_bar_split)

dupes = df_bar['Category'].duplicated('first')
dupes = [not elem for elem in dupes]
my_topic = df_bar['Category'][dupes].index
print_full(my_topic)
# my_topic = df_bar['Category']['Topic1'].index
# print(my_topic)

fig_scatter = px.scatter(df_graph,
                         x="x",
                         y="y",
                         size="Freq",
                         color="topics",
                         hover_name="topics",
)

fig_bar = px.bar(df_bar,
                 x="Freq",
                 y="Term",
                 color="Category",
                 orientation='h',
)

# fig_scatter = go.Figure(data=[
#     go.Scatter(
#         x=data["x"],
#         y=data["y"],
#         mode='markers',
#         marker=dict(
#             size=data["Freq"],
#             sizemode='area',
#             sizeref=2.*max(data["Freq"]) / (200**2),
#         )
#     )
# ])


app.layout = html.Div([
    html.Div(
        [
            dcc.Graph(id="graph-topics", figure=fig_scatter),
        ],
        style={
            "width": "50%",
            "display": "inline-block",
        }
    ),
    html.Div(
        [
            dcc.Graph(id='bar-topics', figure=fig_bar),
            dcc.Slider(1, 10, 1, value=1, id='slider-topics'),
        ],
        style={
            "width": "50%",
            "display": "inline-block",
        }
    )
])

# @app.callback(
#     Input('slider-topics', 'value'),
#     Output('bar-topics', 'Figure'))
# def update_bar(slider_topics):
#     print()

if __name__ == "__main__":
    app.run_server(debug=True)
