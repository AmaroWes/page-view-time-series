import matplotlib.pyplot as plt
import pandas as pd
import subprocess
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

try:
    import seaborn as sns
except:
    subprocess.run(['py', '-m', 'pip', 'install', 'seaborn'])
    import seaborn as sns


df = pd.read_csv('page-view-time-series/CSV/fcc-forum-pageviews.csv', index_col = 'date', parse_dates = ['date'])

df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df['value'], '-r', linewidth=0.75)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    fig.savefig('page-view-time-series/Results/line_plot.png')
    return fig

def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['month'] = df.index.month
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    fig = df_bar.plot(kind = 'bar', legend = True, figsize=(7, 7)).figure
    plt.legend(title='Months', labels = month)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    fig.savefig('page-view-time-series/Results/bar_plot.png')
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['m']=df_box['date'].dt.month
    df_box = df_box.sort_values('m')
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0] = sns.boxplot(x=df_box['year'], y=df_box['value'], ax=axes[0]).set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)')
    axes[1] = sns.boxplot(x=df_box['month'], y=df_box['value'], ax=axes[1]).set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)')
    fig.savefig('page-view-time-series/Results/box_plot.png')
    return fig
