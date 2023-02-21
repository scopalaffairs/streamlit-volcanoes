#!/usr/bin/env python3
# coding: utf-8

# (c) 2023 scopalaffairs

import json
from copy import deepcopy
from urllib.request import urlopen

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st

### CONSTANTS

# colors
white = "rgb(255, 255, 255)"
blueish = "rgb(200, 200, 255)"
vintage_brown = "rgb(255,250,240)"
coastlinecolor = "rgb(205,133,63)"

# strings
title = "Volcanoes of the Earth"
header = "Study geographic features"

# Add title and header, define layout
st.set_page_config(page_title=title, layout='wide')
st.title(title)
st.header(header)

# Setting up columns
left_column, middle_column, right_column = st.columns([1, 3, 1])

# Loading dataframes
@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df


df_raw = load_data(path="./data/volcano_ds_pop.csv")
df = deepcopy(df_raw)
earthquakes_raw = load_data(path="./data/earthquakes.csv")
df_earthquakes = deepcopy(earthquakes_raw)

# Clean dataframe
type_singular = df["Type"].replace(
    [
        "Lava domes",
        "Cinder cones",
        "Calderas",
        "Maars",
        "Pyroclastic cones",
        "Scoria cones",
        "Volcanic fields",
        "Shield volcanoes",
        "Submarine volcanoes",
        "Stratovolcanoes",
    ],
    [
        "Lava dome",
        "Cinder cone",
        "Caldera",
        "Maar",
        "Pyroclastic cone",
        "Scoria cone",
        "Volcanic field",
        "Shield volcano",
        "Submarine volcano",
        "Stratovolcano",
    ],
)

df["Type"] = type_singular
df = df.drop("Unnamed: 0", axis=1)
df = df.rename(columns={"Elev": "Elevation"})

# scale the elevation to plottable sizes
# elev_min = df["Elevation"].min()
# elev_max = df["Elevation"].max()

# max_marker_size = 500
# min_marker_size = 100

# df["Elevation (scaled)"] = (df["Elevation"] - elev_min) / (elev_max - elev_min)
# marker_size = df["Elevation (scaled)"] * (max_marker_size - min_marker_size) + min_marker_size

# marker_size

# Get volcano types and map to colorscheme
unique_volcano_types = df["Type"].unique()
colors = sns.color_palette("rocket", n_colors=len(unique_volcano_types)).as_hex()
type_color_map = dict(zip(unique_volcano_types, colors))

active_volcanoes = (
    (df["Status"] == "Fumarolic")
    | (df["Status"] == "Pleistocene-Fumarol")
    | (df["Status"] == "Pleistocene")
)
df["active"] = active_volcanoes


# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
with left_column:
    # Widgets: selectbox
    volcano_types = ["All"] + sorted(df["Type"].unique())
    selected_volcano_type = st.selectbox("Select volcano type", volcano_types)

    # Widgets: radio buttons
    show_active = st.checkbox(label="Show Active Volcanoes")
# st.write(st.session_state)
    # show_earthquakes = st.checkbox(label="Show Earthquakes")

# Flow control and plotting
if selected_volcano_type == "All":
    selected_df = df
elif show_active:
    # st.session_state.selectbox = "All"
    selected_df = df[df["active"]]
else:
    selected_df = df[df["Type"] == selected_volcano_type]


# if show_earthquakes:
# selected_df = df_earthquakes

df = selected_df

# Interactive menu
updatemenus = [
    dict(
        type="buttons",
        showactive=True,
        buttons=[
            dict(
                args=["visible", "legendonly"],
                label="Hide all of chosen type",
                method="restyle",
            ),
            dict(
                args=["visible", True],
                label="Show all of chosen type",
                method="restyle",
            ),
        ],
        direction="left",
        x=0.05,
        y=1.2,
    )
]

# Tooltip hover label for each datapoint
text = []
for i, row in df.iterrows():
    tooltip = (
        f"Name: <b>{row['Volcano Name']}</b><br><br>"
        + f"Type: {row['Type']}<br><br>"
        + f"Country: {row['Country']}<br>"
        + f"Elevation: {row['Elevation']} meters<br>"
        + f"Active: {row['active']}"
    )
    text.append(tooltip)

with middle_column:
    # Actual plot
    if not show_active:
        fig = go.Figure(
            data=go.Scattergeo(
                lat=df["Latitude"],
                lon=df["Longitude"],
                mode="markers",
                text=text,
                marker_color=[type_color_map[type_val] for type_val in df["Type"]],
            )
        )
    else:
        # Get active volcanoes
        active_volcanoes = go.Scattergeo(
            lon=df[df["active"]]["Longitude"],
            lat=df[df["active"]]["Latitude"],
            mode="markers",
            text=text,
            marker=dict(size=20, color="crimson", opacity=0.2, symbol="circle"),
            name="Active volcanoes",
        )
        fig = go.Figure(data=active_volcanoes)

    # Make updatemenu interactive and define size and basic appearance
    fig.update_layout(
        # updatemenus=updatemenus,
        # autosize=True,
        height=1080,
        width=1280,
        # margin_pad=0,
        # margin_t=0,
        # paper_bgcolor="black",
        geo=dict(
            scope="world",
            showland=True,
            landcolor=vintage_brown,
            subunitcolor=white,
            countrycolor=white,
            coastlinecolor=coastlinecolor,
            showlakes=True,
            lakecolor=blueish,
            projection_type="natural earth",
        ),
        # legend=dict(font_size=12),
    )

    st.plotly_chart(fig,)
