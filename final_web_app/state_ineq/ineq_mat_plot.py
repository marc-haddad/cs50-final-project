
from matplotlib import pyplot as plt
import mpld3
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.axes as axes
import pandas as pd
import numpy as np


def graph(states_form):

    stym = 0
    eym = 0
    dif = 0

    df = pd.read_csv("resources/ineq_data.csv", index_col="Index")

    # Assign State abbreviations to corresponding IDs defined in the .csv
    states = {
        "US":  0, "AL":  1, "AK":  2, "AZ":  3, "AR":  4,
        "CA":  5, "CO":  6, "CT":  7, "DE":  8, "DC":  9,
        "FL": 10, "GA": 11, "HI": 12, "ID": 13, "IL": 14,
        "IN": 15, "IA": 16, "KS": 17, "KY": 18, "LA": 19,
        "ME": 20, "MD": 21, "MA": 22, "MI": 23, "MN": 24,
        "MS": 25, "MO": 26, "MT": 27, "NE": 28, "NV": 29,
        "NH": 30, "NJ": 31, "NM": 32, "NY": 33, "NC": 34,
        "ND": 35, "OH": 36, "OK": 37, "OR": 38, "PA": 39,
        "RI": 40, "SC": 41, "SD": 42, "TN": 43, "TX": 44,
        "UT": 45, "VT": 46, "VA": 47, "WA": 48, "WV": 49,
        "WI": 50, "WY": 51,
        }


    # Initialize plot1
    fig1, ax1 = plt.subplots()

    # Recession rectangles for plot1
    y_m_data = pd.read_csv("resources/rec_data.csv")
    for sty, stm, ey, em in zip(
            y_m_data["start_year"],
            y_m_data["start_month_dec"],
            y_m_data["end_year"],
            y_m_data["end_month_dec"]):

        stym = sty + stm
        eym = ey + em
        dif = eym - stym
        rectangle = patches.Rectangle((stym, 0), (dif), 1, fc='lightgrey', ec='black', alpha=.45)
        ax1.add_patch(rectangle)
    rectangle.set_label("Recessions")

    plt.ylim(0, 1)

    # Select data
    all_df = df[["Year", "st", "State", "Gini"]]
    us_df = all_df[all_df["st"] == 0]

    # Ensure that input is valid, and store in list if user wants to plot more lines
    valid_user_inputs = states_form

    # Plot lines
    for valid_input in valid_user_inputs:
        line_plot(all_df, states[valid_input])

    # Tick and label formatting for plot1
    ax1.set_facecolor("#343a40")
    plt.xticks(np.arange(1910, 2020, step=10), labels=np.arange(1910, 2020, step=10), rotation=45, size=15)
    plt.yticks(np.arange(0.2, 0.85, step=.05), size=15)
    plt.ylabel("GINI Score", size=15)
    plt.xlabel("Year", size=15)
    plt.xlim(1915, 2017)
    plt.ylim(0.2, 0.8)
    ax1.minorticks_on()
    ax1.grid(axis='y', color='r', linestyle='--', alpha=.6)
    ax1.legend(fontsize=11.5, facecolor="inherit", ncol=2)
    plt.figure(dpi=700)
    plt.tight_layout()
    return d3_plot(fig1, ax1)


def line_plot(df, n):
    if n > 51 or n < 0:
        return False

    # Select data
    n_df = df[df["st"] == n]

    # Config label
    label = [df[df["st"] == n]["State"]]
    label = label[0].value_counts().keys()
    lb = ""
    for s in label:
        lb = s

    # Plot lines
    n_line = plt.plot(n_df["Year"], n_df["Gini"], label=lb)
    return(n_line)

def d3_plot(fig, ax):
    plt.figure(figsize=(300, 230))
    return mpld3.fig_to_html(fig)
