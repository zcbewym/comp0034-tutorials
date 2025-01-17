from importlib import resources

import pandas as pd
import plotly.express as px


def bar_gender(event_type):
    """
    Creates a stacked bar chart showing change in the ration of male and female competitors in the summer and winter paralympics.

    Parameters
    event_type: str Winter or Summer

    Returns
    fig: Plotly Express bar chart
    """
    cols = ['type', 'year', 'host', 'participants_m', 'participants_f', 'participants']
    with resources.path("data", "paralympics.csv") as path:
        df_events = pd.read_csv(path, usecols=cols)
        # Drop Rome as there is no male/female data
        # Drop rows where male/female data is missing
        df_events = df_events.dropna(subset=['participants_m', 'participants_f'])
        df_events.reset_index(drop=True, inplace=True)

        # Add new columns that each contain the result of calculating the % of male and female participants
        df_events['Male'] = df_events['participants_m'] / df_events['participants']
        df_events['Female'] = df_events['participants_f'] / df_events['participants']

        # Sort the values by Type and Year
        df_events.sort_values(['type', 'year'], ascending=(True, True), inplace=True)
        # Create a new column that combines Location and Year to use as the x-axis
        df_events['xlabel'] = df_events['host'] + ' ' + df_events['year'].astype(str)

        # Create the stacked bar plot of the % for male and female
        # Ensure event_type is a list if checklist input can return multiple values
        if isinstance(event_type, list):
            df_events = df_events[df_events['type'].isin(event_type)]

        # Check if df_events is empty after filtering
        if df_events.empty:
            print(f"No matching data found for event_type: {event_type}")
            return {}

        fig = px.bar(df_events,
                     x='xlabel',
                     y=['Male', 'Female'],
                     title=f'How has the ratio of female:male participants changed in {event_type} paralympics?',
                     labels={'xlabel': '', 'value': '', 'variable': ''},
                     template="simple_white",
                     color_discrete_map={'Male': 'blue', 'Female': 'green'}
                     )
        fig.update_xaxes(ticklen=0)
        fig.update_yaxes(tickformat=".0%")
        return fig