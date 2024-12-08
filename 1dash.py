import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the dataset
df = pd.read_csv('/path_to/VeronicaData.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Initialize the app
app = dash.Dash(__name__)
app.title = "Veronica's Health Dashboard"

# Define a color scheme
colors = {
    'background': '#f8f9fa',  # Light gray
    'text': '#343a40',        # Dark gray
    'primary': '#007bff',     # Blue
    'secondary': '#6c757d'    # Muted gray
}

# Layout
app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'}, children=[
    html.H1(
        children="Veronica's Health Dashboard",
        style={'textAlign': 'center', 'color': colors['text']}
    ),
    html.Div(
        children="Visualizations of Veronica's health data, providing insights into her health journey.",
        style={'textAlign': 'center', 'color': colors['secondary'], 'marginBottom': '20px'}
    ),
    dcc.Tabs([
        dcc.Tab(label='Blood Glucose Trend', children=[
            dcc.Graph(id='glucose-trend'),
        ]),
        dcc.Tab(label='Caloric Intake by Meal', children=[
            dcc.Graph(id='calorie-intake'),
        ]),
        dcc.Tab(label='Exercise and Health Metrics', children=[
            dcc.Graph(id='health-metrics'),
        ]),
        dcc.Tab(label='Daily Calorie Intake', children=[
            dcc.Graph(id='daily-calorie-intake'),
        ]),
    ], style={'marginBottom': '20px'}),
])

@app.callback(
    Output('glucose-trend', 'figure'),
    Input('glucose-trend', 'id')
)
def update_glucose_trend(id):
    fig = px.line(
        df, x='Date', y='Blood Glucose', 
        title='Blood Glucose Trend Over Time',
        labels={'Date': 'Date', 'Blood Glucose': 'Blood Glucose (mg/dL)'},
        template='plotly_white'
    )
    fig.update_traces(line=dict(color=colors['primary'], width=3))
    fig.update_layout(
        font=dict(size=14, color=colors['text']),
        title=dict(font=dict(size=20))
    )
    return fig

@app.callback(
    Output('calorie-intake', 'figure'),
    Input('calorie-intake', 'id')
)
def update_calorie_intake(id):
    meal_types = ['Breakfast Calories', 'Lunch Calories', 'Dinner Calories', 'Desert Calories']
    averages = [df[meal].mean() for meal in meal_types]
    fig = px.bar(
        x=meal_types, y=averages,
        title='Average Caloric Intake by Meal Type',
        labels={'x': 'Meal Type', 'y': 'Average Calories'},
        template='plotly_white'
    )
    fig.update_traces(marker=dict(color=colors['primary']))
    fig.update_layout(
        font=dict(size=14, color=colors['text']),
        title=dict(font=dict(size=20))
    )
    return fig

@app.callback(
    Output('health-metrics', 'figure'),
    Input('health-metrics', 'id')
)
def update_health_metrics(id):
    fig = px.scatter(
        df, x='Exercise (minutes)', y='Heart Rate',
        size='Systolic', color='Diastolic',
        title='Exercise and Health Metrics',
        labels={'Exercise (minutes)': 'Exercise (minutes)', 'Heart Rate': 'Heart Rate (bpm)'},
        template='plotly_white'
    )
    fig.update_layout(
        font=dict(size=14, color=colors['text']),
        title=dict(font=dict(size=20)),
        legend_title=dict(font=dict(size=14))
    )
    return fig

@app.callback(
    Output('daily-calorie-intake', 'figure'),
    Input('daily-calorie-intake', 'id')
)
def update_daily_calorie_intake(id):
    recommended_threshold = 1500
    fig = px.bar(
        df, x='Date', y='Total Calories',
        title='Total Daily Calorie Intake vs Threshold',
        labels={'Total Calories': 'Calories (kcal)', 'Date': 'Date'},
        template='plotly_white'
    )
    fig.add_hline(
        y=recommended_threshold, line_dash="dash", line_color="red",
        annotation_text="1500 kcal Limit", annotation_position="bottom left"
    )
    fig.update_layout(
        font=dict(size=14, color=colors['text']),
        title=dict(font=dict(size=20))
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
