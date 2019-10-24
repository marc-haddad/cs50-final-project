from matplotlib import pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.axes as axes
import pandas as pd
import numpy as np


def main():

    stym = 0
    eym = 0
    dif = 0

    df = pd.read_csv("ineq_data.csv", index_col="Index")

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
        "WI": 50, "WY": 51
        }

    # Initialize plot1
    fig1, ax1 = plt.subplots()

    # Recession rectangles for plot1
    y_m_data = pd.read_csv("rec_data.csv")
    for sty, stm, ey, em in zip(
            y_m_data["start_year"],
            y_m_data["start_month_dec"],
            y_m_data["end_year"],
            y_m_data["end_month_dec"]):

        stym = sty + stm
        eym = ey + em
        dif = eym - stym
        rectangle = patches.Rectangle((stym, 0), (dif), 1, fc='grey', alpha=.45)
        ax1.add_patch(rectangle)
    rectangle.set_label("Recessions")

    plt.ylim(0, 1)

    # Select data
    all_df = df[["Year", "st", "State", "Gini"]]
    us_df = all_df[all_df["st"] == 0]

    # Ask user for input
    user_input = input("Select State: ").upper()
    
    # Ensure that input is valid, and store in list if user wants to plot more lines
    valid_user_inputs = []
    t = True
    while (t == True):
        for key in states.keys():
            if (user_input == key and user_input not in valid_user_inputs):
                valid_user_inputs.append(user_input)
                t = False
        if (t == True):
            if (user_input in valid_user_inputs):
                print("\nYou've selected that state already.")
                user_input = input("Select State: ").upper()
            else:
                print("\nPlease enter a valid state abbreviation.")
                user_input = input("Select State: ").upper()
        else:
            cont = ""
            while (cont != "y" and cont != "yes" and cont != "n" and cont != "no"):
                cont = input("Add another? (y/n)\n").lower()
                if (cont == "y" or cont == "yes"):
                    t = True
                    user_input = input("Select State: ").upper()
                elif (cont == "n" or cont == "no"):
                    continue
                else:
                    print("\nPlease type either 'y' or 'n'.")

    # Plot lines
    for valid_input in valid_user_inputs:
        line_plot(all_df, states[valid_input])

    plt.title("US State GINI Index Over Time\n1917-2015")

    # Tick and label formatting for plot1
    plt.xticks(np.arange(1910, 2020, step=10), rotation=45)
    plt.yticks(np.arange(0.2, 0.85, step=.05))
    plt.ylabel("GINI Score")
    plt.xlim(1915, 2017)
    plt.ylim(0.2, 0.8)
    ax1.minorticks_on()

    ax1.legend(fontsize=7.5)

    # Ask user if they wish to include 'US GINI Volatility per Year' graph
    include = input("\nInclude 'US GINI Volatility per Year' graph? (y/n)\n").lower()
    while (include != "y" and include != "yes" and include != "n" and include != "no"):
        print("\nPlease type either 'y' or 'n'.")
        include = input("Include 'US GINI Volatility per Year' graph? (y/n)\n").lower()
    if (include == "n" or include == "no"):
        plt.show()
    
    else:
        # Initialize plot2
        fig2, ax2 = plt.subplots()

        # Recession rectangles for plot2
        for sty, stm, ey, em in zip(
                y_m_data["start_year"],
                y_m_data["start_month_dec"],
                y_m_data["end_year"],
                y_m_data["end_month_dec"]):

            stym = sty + stm
            eym = ey + em
            dif = eym - stym
            rectangle = patches.Rectangle((stym, -10), (dif), 20, fc='grey', alpha=.45)
            ax2.add_patch(rectangle)
        rectangle.set_label("Recessions")

        # Change in Gini
        delt_gini_us = []
        delt_year_us = []
        prev_gini = 0
        for gini, year in zip(us_df["Gini"], us_df["Year"]):
            if gini == us_df["Gini"][0]:
                prev_gini = gini
                continue
            gini_perc_change = (gini - prev_gini) * 100
            delt_gini_us.append(gini_perc_change)
            delt_year_us.append(year)
            prev_gini = gini

        # Tick formatting for plot2
        plt.xticks(np.arange(1917, 2027, step=10), rotation=45)
        plt.yticks(np.arange(-15, 15, step=1))
        ax2.tick_params(axis="y", which='major', labelsize=9)
        ax2.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:.1f}%"))

        # Plot bars
        bars = ax2.bar(delt_year_us, delt_gini_us)
        i = 0
        j = 0
        for bar, val in zip(bars, delt_gini_us):
            if val > 0:
                bar.set(edgecolor="red", facecolor="salmon")
                if i == 0:
                    bar.set_label("Increase in Inequality")
                    i += 1
            else:
                bar.set(edgecolor="green", facecolor="lightgreen")
                if j == 0:
                    bar.set_label("Decrease in Inequality")
                    j += 1

        plt.ylim(-10, 10)
        ax2.legend(fontsize=7.5)

        axes.Axes.axhline(ax2, color="k", linestyle="solid", linewidth=.7)
        plt.title("US GINI Volatility per Year\n1917-2015")
        plt.ylabel("Percent Change")

        plt.show()


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


if __name__ == "__main__":
    main()