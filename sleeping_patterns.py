# (c) scopalaffairs 2023

import json
from copy import deepcopy
from urllib.request import urlopen

import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def load_data(path):
    df = pd.read_csv(path)
    return df


sleep_df_raw = load_data(path="data/sleep_patterns.csv")
sleep_df = deepcopy(sleep_df_raw)

st.title("REM state Exploration")
st.header("Sleep Efficacy Patterns")

# plot_types = ["Matplotlib", "Plotly", "Altair"]
# plot_type = st.radio("Choose Plot Type", plot_types)

title = "Sleep Efficacy Patterns"
xlabel = "Displacement (Liters)"
ylabel = "Mileage per Gallon"

st.table(sleep_df)
# matplotlib
# m_fig, ax = plt.subplots(figsize=(12, 8))
# ax.scatter(sleep_df['displ'], sleep_df['hwy'], alpha=0.7)

# ax.set_title(title)
# ax.set_xlabel(xlabel)
# ax.set_ylabel(ylabel)

# # plotly
# p_fig = px.scatter(
    # sleep_df,
    # x='displ',
    # y='hwy',
    # opacity=0.5,
    # range_x=[1, 8],
    # range_y=[10, 50],
    # width=900,
    # height=600,
    # labels={"displ": xlabel, "hwy": ylabel},
    # title=title,
# )
# p_fig.update_layout(title_font_size=20)

# # altair
# a_plot = (
    # alt.Chart(sleep_df)
    # .mark_circle(size=90)
    # .encode(
        # x=alt.X('displ', title=xlabel),
        # y=alt.Y('hwy', title=ylabel),
        # color=alt.Color('year:N', title='Year'),
        # tooltip=[
            # alt.Tooltip('displ', title=xlabel),
            # alt.Tooltip('hwy', title='Highway'),
        # ],
    # )
    # .properties(width=900, height=600, title=title)
    # .interactive()
# )

# if plot_type == "Matplotlib":
    # st.pyplot(m_fig)
# elif plot_type == "Plotly":
    # st.plotly_chart(p_fig)
# elif plot_type == "Altair":
    # st.altair_chart(a_plot)
