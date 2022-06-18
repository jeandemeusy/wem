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

# Load data
with open("topics.json") as f:
    data = json.load(f)
    
with open("daily_topics.json") as f:
    data_daily = json.load(f)

with open("guardian_topics.json") as f:
    data_guardian = json.load(f)

with open("huffpost_topics.json") as f:
    data_huffpost = json.load(f)

# Create DataFrame
df_daily = pd.DataFrame([data_daily])
df_guardian = pd.DataFrame([data_guardian])
df_huffpost = pd.DataFrame([data_huffpost])
df_test = pd.DataFrame([data])


# Copying the frequency of the topics from the dataframe.
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

df_bar_test = pd.DataFrame(df_test["tinfo"][0])
df_bar_daily = pd.DataFrame(df_daily["tinfo"][0])
df_bar_huffpost = pd.DataFrame(df_huffpost["tinfo"][0])
df_bar_guardian = pd.DataFrame(df_guardian["tinfo"][0])
# df_bar_test.to_json('test.json')
# df_bar_split = pd.DataFrame({'Term': df["tinfo"][0]['Term'], 'Category': df['tinfo'][0]['Category']})
# print(df_bar_split)

# For each topic get the first index
dupes = df_bar_test['Category'].duplicated('first')
dupes = [not elem for elem in dupes]
start_topic_index_testdf = df_bar_test['Category'][dupes].index

# For each topic get the last index
dupes = df_bar_test['Category'].duplicated('last')
dupes = [not elem for elem in dupes]
end_topic_index_testdf = df_bar_test['Category'][dupes].index

# Same for DailyMail
dupes = df_bar_daily['Category'].duplicated('first')
dupes = [not elem for elem in dupes]
start_topic_index_df_daily = df_bar_daily['Category'][dupes].index

dupes = df_bar_daily['Category'].duplicated('last')
dupes = [not elem for elem in dupes]
end_topic_index_df_daily = df_bar_daily['Category'][dupes].index

# Same for HuffPost
dupes = df_bar_huffpost['Category'].duplicated('first')
dupes = [not elem for elem in dupes]
start_topic_index_df_huffpost = df_bar_huffpost['Category'][dupes].index

dupes = df_bar_huffpost['Category'].duplicated('last')
dupes = [not elem for elem in dupes]
end_topic_index_df_huffpost = df_bar_huffpost['Category'][dupes].index

# Same for TheGuardian
dupes = df_bar_guardian['Category'].duplicated('first')
dupes = [not elem for elem in dupes]
start_topic_index_df_guardian = df_bar_guardian['Category'][dupes].index

dupes = df_bar_guardian['Category'].duplicated('last')
dupes = [not elem for elem in dupes]
end_topic_index_df_guardian = df_bar_guardian['Category'][dupes].index


# Creating a list of the terms for each topic.
topic1 = df_bar_test['Term'][start_topic_index_testdf[1]:end_topic_index_testdf[1]+1]
topic2 = df_bar_test['Term'][start_topic_index_testdf[2]:end_topic_index_testdf[2]+1]
topic3 = df_bar_test['Term'][start_topic_index_testdf[3]:end_topic_index_testdf[3]+1]
topic4 = df_bar_test['Term'][start_topic_index_testdf[4]:end_topic_index_testdf[4]+1]
topic5 = df_bar_test['Term'][start_topic_index_testdf[5]:end_topic_index_testdf[5]+1]
topic6 = df_bar_test['Term'][start_topic_index_testdf[6]:end_topic_index_testdf[6]+1]
topic7 = df_bar_test['Term'][start_topic_index_testdf[7]:end_topic_index_testdf[7]+1]
topic8 = df_bar_test['Term'][start_topic_index_testdf[8]:end_topic_index_testdf[8]+1]
topic9 = df_bar_test['Term'][start_topic_index_testdf[9]:end_topic_index_testdf[9]+1]
topic10 = df_bar_test['Term'][start_topic_index_testdf[10]:end_topic_index_testdf[10]+1]


# Creating a scatter plot with dataframe df_graph.
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

# Creating a bar chart with the dataframe df_bar_test.
fig_bar_test = px.bar(df_bar_test,
                      title="Test dataset",
                      x="Freq",
                      y="Term",
                      color="Category",
                      orientation='h',
)

# Creating a bar chart with the dataframe df_bar_test.
fig_bar_daily = px.bar(df_bar_daily,
                       title="DailyMail dataset",
                       x="Freq",
                       y="Term",
                       color="Category",
                       orientation='h',
)

# Creating a bar chart with the dataframe df_bar_test.
fig_bar_huffpost = px.bar(df_bar_huffpost,
                          title="HuffPost dataset",
                          x="Freq",
                          y="Term",
                          color="Category",
                          orientation='h',
)

# Creating a bar chart with the dataframe df_bar_test.
fig_bar_guardian = px.bar(df_bar_guardian,
                          title="TheGuardian dataset",
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
    # html.Div(
    #     [
    #         dcc.Graph(id='bar-topics-test', figure=fig_bar_test),
    #         dcc.Slider(1, 10, 1, value=1, id='slider-topics'),
    #     ],
    #     style={
    #         "width": "50%",
    #         "display": "inline-block",
    #     }
    # ),
    html.Div(
        [
            dcc.Graph(id='bar-topics-daily', figure=fig_bar_daily),
        ],
        style={
            "width": "50%",
            "display": "inline-block",
        }
    ),
    html.Div(
        [
            dcc.Graph(id='bar-topics-huffpost', figure=fig_bar_huffpost),
        ],
        style={
            "width": "50%",
            "display": "inline-block",
        }
    ),
    html.Div(
        [
            dcc.Graph(id='bar-topics-guardian', figure=fig_bar_guardian),
        ],
        style={
            "width": "50%",
            "display": "inline-block",
        }
    ),
    html.Div(
        [
            dcc.Slider(1, 10, 1, value=1, id='slider-topics')
        ],
        style={
            "width": "100%",
            "display": "inline-block",
        }
    )
])

def update(topic_select, df):
    pass

# @app.callback(
#     Output('bar-topics-test', 'figure'),
#     Input('slider-topics', 'value')
# )
# def update_bar_test(slider_topic):
#     term_topic = df_bar_test['Term'][start_topic_index_testdf[slider_topic]:end_topic_index_testdf[slider_topic]+1]
#     freq_term_topic = df_bar_test['Freq'][start_topic_index_testdf[slider_topic]:end_topic_index_testdf[slider_topic]+1]
#     dff = pd.DataFrame({'Term': term_topic, 'Freq': freq_term_topic})
#     dff.sort_values(by='Freq', ascending=False, inplace=True)
#     dff = dff.head(10)
#     dff.sort_values(by='Freq', ascending=True, inplace=True)
#     fig = px.bar(
#                  x=dff['Freq'],
#                  y=dff['Term'],
#                  orientation='h',
#     )
#     return fig

@app.callback(
    Output('bar-topics-daily', 'figure'),
    Input('slider-topics', 'value')
)
def update_bar_daily(slider_topic):
    term_topic = df_bar_daily['Term'][start_topic_index_df_daily[slider_topic]:end_topic_index_df_daily[slider_topic]+1]
    freq_term_topic = df_bar_daily['Freq'][start_topic_index_df_daily[slider_topic]:end_topic_index_df_daily[slider_topic]+1]
    dff = pd.DataFrame({'Term': term_topic, 'Freq': freq_term_topic})
    dff.sort_values(by='Freq', ascending=False, inplace=True)
    dff = dff.head(10)
    dff.sort_values(by='Freq', ascending=True, inplace=True)
    fig = px.bar(
        title="DailyMail dataset",
        x=dff['Freq'],
        y=dff['Term'],
        orientation='h',
    )
    return fig

@app.callback(
    Output('bar-topics-huffpost', 'figure'),
    Input('slider-topics', 'value')
)
def update_bar_huffpost(slider_topic):
    term_topic = df_bar_huffpost['Term'][start_topic_index_df_huffpost[slider_topic]:end_topic_index_df_huffpost[slider_topic]+1]
    freq_term_topic = df_bar_huffpost['Freq'][start_topic_index_df_huffpost[slider_topic]:end_topic_index_df_huffpost[slider_topic]+1]
    dff = pd.DataFrame({'Term': term_topic, 'Freq': freq_term_topic})
    dff.sort_values(by='Freq', ascending=False, inplace=True)
    dff = dff.head(10)
    dff.sort_values(by='Freq', ascending=True, inplace=True)
    fig = px.bar(
        title="HuffPost dataset",
        x=dff['Freq'],
        y=dff['Term'],
        orientation='h',
    )
    return fig

@app.callback(
    Output('bar-topics-guardian', 'figure'),
    Input('slider-topics', 'value')
)
def update_bar_guardian(slider_topic):
    term_topic = df_bar_guardian['Term'][start_topic_index_df_guardian[slider_topic]:end_topic_index_df_guardian[slider_topic]+1]
    freq_term_topic = df_bar_guardian['Freq'][start_topic_index_df_guardian[slider_topic]:end_topic_index_df_guardian[slider_topic]+1]
    dff = pd.DataFrame({'Term': term_topic, 'Freq': freq_term_topic})
    dff.sort_values(by='Freq', ascending=False, inplace=True)
    dff = dff.head(10)
    dff.sort_values(by='Freq', ascending=True, inplace=True)
    fig = px.bar(
        title="TheGuardian dataset",
        x=dff['Freq'],
        y=dff['Term'],
        orientation='h',
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
