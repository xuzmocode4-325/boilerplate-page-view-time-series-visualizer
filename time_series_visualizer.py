import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv(
    "fcc-forum-pageviews.csv", 
    index_col = "date",
    parse_dates = ["date"])

# Clean data
df = df.loc[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    fig, ax = plt.subplots(figsize =(32, 10))
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.plot(df.index, df["value"], "r", linewidth=1)
    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Draw bar plot
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    df_bar = df_bar.groupby(["year", "month"])["value"].mean()
    df_bar = df_bar.unstack()
    df_bar.columns =  [
        "January", "February", "March", "April", 
        "May", "June", "July", "August", 
        "September", "October", "November", "December"
    ]

    fig = df_bar.plot(kind="bar", figsize=(16, 9)).figure
    plt.xlabel("Years", fontsize=16)
    plt.ylabel("Average Page Views", fontsize=16)
    plt.legend(loc = "upper left", title = "Months", fontsize=16)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)

    # Extract year and month from date column
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Sort DataFrame by month order
    df_box["month_order"] = df_box["date"].dt.month
    df_box = df_box.sort_values("month_order")

    # Create figure and axes for subplots
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16, 9))

    # Year-wise Box Plot (Trend) using Matplotlib
    cat_order = list(df_box["month"].unique())
    ax1 = sns.boxplot(x=df_box["year"].astype("category"), y=df_box["value"].astype('float'), ax=ax1, orient = "v")
    ax2 = sns.boxplot(x=df_box["month"].astype("category"), y=df_box["value"].astype('float'), ax=ax2, orient = "v", order=cat_order)

    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    # Month-wise Box Plot (Seasonality) using Matplotlib
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
