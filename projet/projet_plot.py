import json

import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from natsort import index_natsorted


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
with open("stored_data/topics.json") as f:
    data = json.load(f)

with open("stored_data/daily_topics.json") as f:
    data_daily = json.load(f)

with open("stored_data/guardian_topics.json") as f:
    data_guardian = json.load(f)

with open("stored_data/huffpost_topics.json") as f:
    data_huffpost = json.load(f)

# Create DataFrame
df_daily = pd.DataFrame([data_daily])
df_guardian = pd.DataFrame([data_guardian])
df_huffpost = pd.DataFrame([data_huffpost])

freq_df = pd.DataFrame()
freq_df["daily"] = df_daily["mdsDat"][0]["Freq"]
freq_df["huffpost"] = df_huffpost["mdsDat"][0]["Freq"]
freq_df["guardian"] = df_guardian["mdsDat"][0]["Freq"]

df_graph = pd.DataFrame(df_daily["mdsDat"][0])
df_graph["Freq"] = np.log(freq_df.sum(axis=1) + 1)

df_graph["Freq_daily"] = [round(v, 2) for v in df_daily["mdsDat"][0]["Freq"]]
df_graph["Freq_huffpost"] = [round(v, 2) for v in df_huffpost["mdsDat"][0]["Freq"]]
df_graph["Freq_guardian"] = [round(v, 2) for v in df_guardian["mdsDat"][0]["Freq"]]


df_bar_daily = pd.DataFrame(df_daily["tinfo"][0])
website = ["daily" for i in range(len(df_bar_daily["Category"]))]
df_bar_daily["website"] = website
# df_bar_daily.drop(df_bar_daily[df_bar_daily['Category'] == 'Default'].index, inplace=True)

df_bar_huffpost = pd.DataFrame(df_huffpost["tinfo"][0])
website = ["huffpost" for i in range(len(df_bar_huffpost["Category"]))]
df_bar_huffpost["website"] = website
# df_bar_huffpost.drop(df_bar_huffpost[df_bar_huffpost['Category'] == 'Default'].index, inplace=True)

df_bar_guardian = pd.DataFrame(df_guardian["tinfo"][0])
website = ["guardian" for i in range(len(df_bar_guardian["Category"]))]
df_bar_guardian["website"] = website
# df_bar_guardian.drop(df_bar_guardian[df_bar_guardian['Category'] == 'Default'].index, inplace=True)

concat_all = [df_bar_daily, df_bar_huffpost, df_bar_guardian]
# df_bar_all = pd.merge(df_bar_daily, df_bar_huffpost, how='left', on='Category')
df_bar_all = pd.concat(concat_all, ignore_index=True)
df_bar_all.sort_values(
    by=["Category"],
    inplace=True,
    key=lambda x: np.argsort(index_natsorted(df_bar_all["Category"])),
)

# df_bar_all.sort_values(by=['Category'], inplace=True, ascending=True)
# print_full(df_bar_all)

# df_bar_all.to_json('test.json')
# df_bar_test.to_json('test.json')
# df_bar_split = pd.DataFrame({'Term': df["tinfo"][0]['Term'], 'Category': df['tinfo'][0]['Category']})
# print(df_bar_split)

df_bar_all.drop(df_bar_all[df_bar_all["Category"] == "Default"].index, inplace=True)
# df_bar_all.to_json('test.json')


# For each topic get the first and last index

# ... for DailyMail
dupes = df_bar_daily["Category"].duplicated("first")
dupes = [not elem for elem in dupes]
start_topic_index_df_daily = df_bar_daily["Category"][dupes].index

dupes = df_bar_daily["Category"].duplicated("last")
dupes = [not elem for elem in dupes]
end_topic_index_df_daily = df_bar_daily["Category"][dupes].index

# ... for HuffPost
dupes = df_bar_huffpost["Category"].duplicated("first")
dupes = [not elem for elem in dupes]
start_topic_index_df_huffpost = df_bar_huffpost["Category"][dupes].index

dupes = df_bar_huffpost["Category"].duplicated("last")
dupes = [not elem for elem in dupes]
end_topic_index_df_huffpost = df_bar_huffpost["Category"][dupes].index

# ... for TheGuardian
dupes = df_bar_guardian["Category"].duplicated("first")
dupes = [not elem for elem in dupes]
start_topic_index_df_guardian = df_bar_guardian["Category"][dupes].index

dupes = df_bar_guardian["Category"].duplicated("last")
dupes = [not elem for elem in dupes]
end_topic_index_df_guardian = df_bar_guardian["Category"][dupes].index

# ... for All
dupes = df_bar_all["Category"].duplicated("first")
dupes = [not elem for elem in dupes]
start_topic_index_df_all = df_bar_all["Category"][dupes].index

dupes = df_bar_all["Category"].duplicated("last")
dupes = [not elem for elem in dupes]
end_topic_index_df_all = df_bar_all["Category"][dupes].index

# Creating a scatter plot with dataframe df_graph.
fig_scatter = px.scatter(
    df_graph,
    x="x",
    y="y",
    text="topics",
    size="Freq",
    color="topics",
    hover_name="topics",
    size_max=80,
    hover_data={
        "x": False,
        "y": False,
        "Freq": False,
        "topics": False,
        "Freq_daily": True,
        "Freq_huffpost": True,
        "Freq_guardian": True,
    },
    labels={"x": "", "y": ""},
)
fig_scatter.update_traces(marker_coloraxis=None, textposition="middle center")
fig_scatter.update_yaxes(visible=False, showticklabels=False)
fig_scatter.update_xaxes(visible=False, showticklabels=False)

# Creating a bar chart with the dataframe df_bar_test.
fig_bar_daily = px.bar(
    df_bar_daily,
    title="DailyMail dataset",
    x="Freq",
    y="Term",
    color="Category",
    orientation="h",
)

# Creating a bar chart with the dataframe df_bar_test.
fig_bar_huffpost = px.bar(
    df_bar_huffpost,
    title="HuffPost dataset",
    x="Freq",
    y="Term",
    color="Category",
    orientation="h",
)

# Creating a bar chart with the dataframe df_bar_test.
fig_bar_guardian = px.bar(
    df_bar_guardian,
    title="TheGuardian dataset",
    x="Freq",
    y="Term",
    color="Category",
    orientation="h",
)

fig_bar_all = px.bar(
    df_bar_all,
    title="All datasets",
    x="Term",
    y="Freq",
    color="website",
    barmode="stack",
    height=1000,
)


app.layout = html.Div(
    [
        html.Div(
            [dcc.Graph(id="graph-topics", figure=fig_scatter)],
            style={"width": "50%", "display": "inline-block"},
        ),
        html.Div(
            [dcc.Graph(id="bar-topics-daily", figure=fig_bar_daily)],
            style={"width": "50%", "display": "inline-block"},
        ),
        html.Div(
            [dcc.Graph(id="bar-topics-huffpost", figure=fig_bar_huffpost)],
            style={"width": "50%", "display": "inline-block"},
        ),
        html.Div(
            [dcc.Graph(id="bar-topics-guardian", figure=fig_bar_guardian)],
            style={"width": "50%", "display": "inline-block"},
        ),
        html.Div(
            [dcc.Slider(1, 18, 1, value=1, id="slider-topics")],
            style={
                "width": "60%",
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto",
            },
        ),
        html.Div(
            [dcc.Graph(id="bar-topics-all", figure=fig_bar_all)],
            style={"width": "50%", "display": "inline-block"},
        ),
    ]
)


def update(topic_select, df):
    pass


@app.callback(Output("bar-topics-daily", "figure"), Input("slider-topics", "value"))
def update_bar_daily(slider_topic):
    term_topic = df_bar_daily["Term"][
        start_topic_index_df_daily[slider_topic] : end_topic_index_df_daily[
            slider_topic
        ]
        + 1
    ]
    freq_term_topic = df_bar_daily["Freq"][
        start_topic_index_df_daily[slider_topic] : end_topic_index_df_daily[
            slider_topic
        ]
        + 1
    ]
    dff = pd.DataFrame({"Term": term_topic, "Freq": freq_term_topic})
    dff.sort_values(by="Freq", ascending=False, inplace=True)

    dff = dff.head(10)

    dff.sort_values(by="Freq", ascending=True, inplace=True)
    fig = px.bar(
        dff,
        x="Freq",
        y="Term",
        orientation="h",
        labels={"x": "Frequency", "y": ""},
        hover_name="Term",
        hover_data={"Term": False, "Freq": True},
    )
    fig.update_layout(
        yaxis_title=None,
        title={
            "text": "DailyMail dataset",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    return fig


@app.callback(Output("bar-topics-huffpost", "figure"), Input("slider-topics", "value"))
def update_bar_huffpost(slider_topic):
    term_topic = df_bar_huffpost["Term"][
        start_topic_index_df_huffpost[slider_topic] : end_topic_index_df_huffpost[
            slider_topic
        ]
        + 1
    ]
    freq_term_topic = df_bar_huffpost["Freq"][
        start_topic_index_df_huffpost[slider_topic] : end_topic_index_df_huffpost[
            slider_topic
        ]
        + 1
    ]
    dff = pd.DataFrame({"Term": term_topic, "Freq": freq_term_topic})
    dff.sort_values(by="Freq", ascending=False, inplace=True)
    dff = dff.head(10)
    dff.sort_values(by="Freq", ascending=True, inplace=True)
    fig = px.bar(
        dff,
        x="Freq",
        y="Term",
        orientation="h",
        labels={"x": "Frequency", "y": ""},
        hover_name="Term",
        hover_data={"Term": False, "Freq": True},
    )
    fig.update_layout(
        yaxis_title=None,
        title={
            "text": "HuffPost dataset",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    return fig


@app.callback(Output("bar-topics-guardian", "figure"), Input("slider-topics", "value"))
def update_bar_guardian(slider_topic):
    term_topic = df_bar_guardian["Term"][
        start_topic_index_df_guardian[slider_topic] : end_topic_index_df_guardian[
            slider_topic
        ]
        + 1
    ]
    freq_term_topic = df_bar_guardian["Freq"][
        start_topic_index_df_guardian[slider_topic] : end_topic_index_df_guardian[
            slider_topic
        ]
        + 1
    ]
    dff = pd.DataFrame({"Term": term_topic, "Freq": freq_term_topic})
    dff.sort_values(by="Freq", ascending=False, inplace=True)
    dff = dff.head(10)
    dff.sort_values(by="Freq", ascending=True, inplace=True)
    fig = px.bar(
        dff,
        x="Freq",
        y="Term",
        orientation="h",
        labels={"x": "Frequency", "y": ""},
        hover_name="Term",
        hover_data={"Term": False, "Freq": True},
    )
    fig.update_layout(
        yaxis_title=None,
        title={
            "text": "TheGuardian dataset",
            "y": 0.9,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
