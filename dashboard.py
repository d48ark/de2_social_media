import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import os
from datetime import datetime

app = dash.Dash(__name__)
app.title = "Real-time Social Media Dashboard"

app.layout = html.Div([
    html.H1("📊 Real-time Social Media Analytics", style={'textAlign': 'center'}),

    html.Div(id="stats-div", style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'padding': '10px 20px',
        'backgroundColor': '#f8f9fa',
        'border': '1px solid #ccc',
        'borderRadius': '8px',
        'marginBottom': '20px'
    }),

    dcc.Interval(
        id='interval-component',
        interval=5000,  # 5 seconds
        n_intervals=0
    ),

    dcc.Graph(id='spam-pie'),
    dcc.Graph(id='platform-bar'),
], style={'fontFamily': 'Arial, sans-serif', 'margin': '0 auto', 'width': '80%'})

@app.callback(
    [Output('spam-pie', 'figure'),
     Output('platform-bar', 'figure'),
     Output('stats-div', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    file_path = "data/streamed_tweets.csv"
    if not os.path.exists(file_path):
        return dash.no_update, dash.no_update, "No data yet."

    df = pd.read_csv(file_path, names=[
        "user", "text", "timestamp", "location", "platform", "is_spam"
    ])

    # Fill missing values
    df = df.fillna({
        "user": "Unknown User",
        "text": "No content",
        "timestamp": "Unknown Time",
        "location": "Unknown Location",
        "platform": "Unknown Platform",
        "is_spam": 0
    })

    df["is_spam"] = df["is_spam"].map({0: "Not Spam", 1: "Spam"})

    # Pie Chart
    pie_fig = px.pie(
        df,
        names='is_spam',
        title='Spam vs. Non-Spam Distribution',
        hole=0.4,
        color_discrete_sequence=["#2ca02c", "#d62728"]
    )
    pie_fig.update_traces(textinfo='percent+label', hovertemplate='%{label}: %{percent}')

    # Bar Chart
    bar_fig = px.histogram(
        df,
        x='platform',
        color='is_spam',
        barmode='group',
        title='Posts by Platform and Spam Status',
        color_discrete_map={"Spam": "#d62728", "Not Spam": "#2ca02c"},
        category_orders={"platform": sorted(df['platform'].unique())}
    )
    bar_fig.update_layout(xaxis_title="Platform", yaxis_title="Number of Posts")

    # Live stats text
    total_tweets = len(df)
    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S utc")

    stats = [
        html.Div(f"🕒 Current Time: {current_time}", style={'fontSize': '16px'}),
        html.Div(f"📊 Total Tweets Processed: {total_tweets}", style={'fontSize': '16px', 'fontWeight': 'bold'}),
    ]

    return pie_fig, bar_fig, stats

if __name__ == '__main__':
    app.run(debug=True)
