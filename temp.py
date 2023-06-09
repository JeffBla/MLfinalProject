import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf

cf.go_offline()


def read():
    df = pd.read_csv("./outputExcel/1901_2019_BD_weather.csv")
    df = df.drop('Rain', axis=1)
    df.rename(columns={
        'Year': 'Year',
        'Month': 'Month',
        'Temperature ': 'Temperature'
    },
              inplace=True)
    return df


def df_yearly_avg_temperature():
    df = read()
    yearly_temp = df.groupby('Year')['Temperature'].mean()
    X = yearly_temp.index.tolist()
    Y = yearly_temp
    df_year = pd.DataFrame({'Year': X, 'Year_temp': Y})
    df_year = df_year.reset_index(drop=True)
    return df_year


def plot_yearly_avg_temperature():
    df_year = df_yearly_avg_temperature()
    X = df_year[['Year']]
    Y = df_year['Year_temp']
    fig = go.Figure(data=go.Scatter(
        x=df_year['Year'], y=Y, name="Bengal year avg temperature"))
    lr = LinearRegression()
    lr.fit(X, Y)
    slope = lr.coef_[0]
    fig.add_trace(
        go.Scatter(x=df_year['Year'],
                   y=lr.predict(X),
                   name="slope: %f" % slope))
    fig.update_layout(xaxis=dict(title='Year'),
                      yaxis=dict(title='Temperature'))
    return fig


def boxplot():
    df_year = df_yearly_avg_temperature()
    fig = go.Figure()
    return fig.add_trace(
        go.Box(y=df_year['Year_temp'],
               boxpoints='all',
               boxmean='sd',
               name='Temperature'))


def set_winter_year(df_winter):
    if (df_winter['Month'] == 1) | (df_winter['Month'] == 2):
        return (int)(df_winter['Year'] - 1)
    else:
        return (int)(df_winter['Year'])


def df_winter_avg_temperature():
    df = read()
    df_winter = df[(df['Month'] == 12) | (df['Month'] == 1) |
                   (df['Month'] == 2)]
    df_winter['Winter_year'] = df_winter.apply(set_winter_year, axis=1)
    df_winter = df_winter[(df_winter['Winter_year'] > 1900)
                          & (df_winter['Winter_year'] < 2019)]
    return df_winter


def plot_winter_avg_temperature():
    df_winter = df_winter_avg_temperature()
    winter_avg_temp = df_winter.groupby('Winter_year')['Temperature'].mean()
    X = winter_avg_temp.index.tolist()
    Y = winter_avg_temp
    fig = go.Figure(
        data=go.Scatter(x=X, y=Y, name="Bengal year avg temperature"))
    fig.update_layout(xaxis=dict(title='Year'),
                      yaxis=dict(title='Temperature'),
                      showlegend=True)
    return fig


def plot_check_warm_winter():
    df_winter = df_winter_avg_temperature()
    winter_avg_temp = df_winter.groupby('Winter_year')['Temperature'].mean()
    mean = winter_avg_temp.mean()
    std = winter_avg_temp.std()
    X = winter_avg_temp.index.tolist()
    Y = winter_avg_temp
    plt.plot(X, Y, label='winter_avg_temperature')
    mean_line = np.ones(len(X)) * mean
    mean_plus_std_line = mean_line + std
    mean_minus_std_line = mean_line - std
    plt.plot(X, mean_plus_std_line, label='mean+std')
    plt.plot(X, mean_line, label='mean')
    plt.plot(X, mean_minus_std_line, label='mean-std')
    plt.xlabel('Year')
    plt.ylabel('Temperature')
    plt.legend()


def plot_check_cut_warm_winter():
    df_winter = df_winter_avg_temperature()
    cut_df_winter = df_winter[df_winter['Winter_year'] > 1994]
    cut_winter_avg_temp = cut_df_winter.groupby(
        'Winter_year')['Temperature'].mean()
    mean = cut_winter_avg_temp.mean()
    std = cut_winter_avg_temp.std()
    X = cut_winter_avg_temp.index.tolist()
    Y = cut_winter_avg_temp
    plt.plot(X, Y, label='cut_winter_avg_temperature')
    mean_line = np.ones(len(X)) * mean
    mean_plus_std_line = mean_line + std
    mean_minus_std_line = mean_line - std
    plt.plot(X, mean_plus_std_line, label='mean+std')
    plt.plot(X, mean_line, label='mean')
    plt.plot(X, mean_minus_std_line, label='mean-std')
    plt.xlabel('Year')
    plt.ylabel('Temperature')
    plt.legend(bbox_to_anchor=(1, 1))
