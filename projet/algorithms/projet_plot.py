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
    
with open("daily_topics.json") as f:
    data_daily = json.load(f)

with open("guardian_topics.json") as f:
    data_guardian = json.load(f)

with open("huffpost_topics.json") as f:
    data_huffpost = json.load(f)


df_daily = pd.DataFrame([data_daily])
df_guardian = pd.DataFrame([data_guardian])
df_huffpost = pd.DataFrame([data_huffpost])
df = pd.DataFrame([data])

freq_copy_daily = (df_daily["mdsDat"][0]["Freq"]).copy()
freq_copy_huffpost = (df_huffpost["mdsDat"][0]["Freq"]).copy()
freq_copy_guardian = (df_guardian["mdsDat"][0]["Freq"]).copy()

df_graph = pd.DataFrame(df_daily["mdsDat"][0])

for i in range(len(df_daily["topic.order"][0])):
    correct_index_daily = df_daily["topic.order"][0][i]
    df_daily["mdsDat"][0]['Freq'][correct_index_daily-1] = freq_copy_daily[i]

    correct_index_huffpost = df_huffpost["topic.order"][0][i]
    df_huffpost["mdsDat"][0]['Freq'][correct_index_huffpost-1] = freq_copy_huffpost[i]

    correct_index_guardian = df_guardian["topic.order"][0][i]
    df_guardian["mdsDat"][0]['Freq'][correct_index_guardian-1] = freq_copy_guardian[i]

for i in range(len(df_daily["mdsDat"][0]['Freq'])):
    df_graph['Freq'][i] = np.log((df_daily["mdsDat"][0]['Freq'][i] + df_huffpost["mdsDat"][0]['Freq'][i] + df_guardian["mdsDat"][0]['Freq'][i])/3+2)

df_graph["Freq_daily"] = df_daily["mdsDat"][0]['Freq']
df_graph["Freq_huffpost"] = df_huffpost["mdsDat"][0]['Freq']
df_graph["Freq_guardian"] = df_guardian["mdsDat"][0]['Freq']

df_bar = pd.DataFrame(df["tinfo"][0])
df_bar.to_json('test.json')
# df_bar_split = pd.DataFrame({'Term': df["tinfo"][0]['Term'], 'Category': df['tinfo'][0]['Category']})
# print(df_bar_split)

# Get first topic index
dupes = df_bar['Category'].duplicated('first')
dupes = [not elem for elem in dupes]
start_topic_index = df_bar['Category'][dupes].index

# Get last topic index
dupes = df_bar['Category'].duplicated('last')
dupes = [not elem for elem in dupes]
end_topic_index = df_bar['Category'][dupes].index

topic1 = df_bar['Term'][start_topic_index[1]:end_topic_index[1]+1]
topic2 = df_bar['Term'][start_topic_index[2]:end_topic_index[2]+1]
topic3 = df_bar['Term'][start_topic_index[3]:end_topic_index[3]+1]
topic4 = df_bar['Term'][start_topic_index[4]:end_topic_index[4]+1]
topic5 = df_bar['Term'][start_topic_index[5]:end_topic_index[5]+1]
topic6 = df_bar['Term'][start_topic_index[6]:end_topic_index[6]+1]
topic7 = df_bar['Term'][start_topic_index[7]:end_topic_index[7]+1]
topic8 = df_bar['Term'][start_topic_index[8]:end_topic_index[8]+1]
topic9 = df_bar['Term'][start_topic_index[9]:end_topic_index[9]+1]
topic10 = df_bar['Term'][start_topic_index[10]:end_topic_index[10]+1]


fig_scatter = px.scatter(df_graph,
                         x="x",
                         y="y",
                         size="Freq",
                         color="topics",
                         hover_name="topics",
                         hover_data={'x':False,
                                    'y':False, 
                                    'Freq':False, 
                                    'topics': False, 
                                    'Freq_daily' : True,
                                    'Freq_huffpost' : True,
                                    'Freq_guardian' :True
                                    }
                         
)

fig_bar = px.bar(df_bar,
                 x="Freq",
                 y="Term",
                 color="Category",
                 orientation='h',
)


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


@app.callback(
    Output('bar-topics', 'figure'),
    Input('slider-topics', 'value')
)
def update_bar(slider_topic):
    term_topic = df_bar['Term'][start_topic_index[slider_topic]:end_topic_index[slider_topic]+1]
    freq_term_topic = df_bar['Freq'][start_topic_index[slider_topic]:end_topic_index[slider_topic]+1]
    dff = pd.DataFrame({'Term': term_topic, 'Freq': freq_term_topic})
    dff.sort_values(by='Freq', ascending=False, inplace=True)
    dff = dff.head(10)
    dff.sort_values(by='Freq', ascending=True, inplace=True)
    print(dff)
    fig = px.bar(
                 x=dff['Freq'],
                 y=dff['Term'],
                 orientation='h',
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
