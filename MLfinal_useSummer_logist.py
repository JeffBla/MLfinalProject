import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.express as px
import plotly.graph_objects as go
import cufflinks as cf
import datapane as dp

from excelImport import fileToDistrict

cf.go_offline()

distMeanTemp_Yearly = pd.read_excel('./outputExcel/distMeanTemp_Yearly.xlsx',
                                    sheet_name='new1',
                                    index_col=0)

distMeanTemp_winterMouth = pd.read_excel(
    './outputExcel/distMeanTemp_winterMonth.xlsx',
    sheet_name='new1',
    index_col=0)

tempDataDist = {}
for dist in fileToDistrict.values():
    tempDataDist[dist] = pd.read_excel('./outputExcel/tempData.xlsx',
                                       sheet_name=dist,
                                       index_col=0)

distMeanTemp_YearlyDataSet = []
for dist in distMeanTemp_Yearly.columns:
    distMeanTemp_YearlyDataSet.append(
        dict(type='scatter',
             x=distMeanTemp_Yearly.index,
             y=distMeanTemp_Yearly[dist],
             name=dist))
distMeanTemp_YearlyFig = go.Figure(data=distMeanTemp_YearlyDataSet)

distMeanTemp_winterMouthFig = distMeanTemp_winterMouth.figure(kind='scatter')

ANBUYearAnalysisData = dict(type='scatter',
                            x=distMeanTemp_Yearly.index,
                            y=distMeanTemp_Yearly['Taipei ANBU'],
                            name='Taipei ANBU')
X = np.array(ANBUYearAnalysisData['x']).reshape(len(ANBUYearAnalysisData['x']),
                                                1)
y = ANBUYearAnalysisData['y'].values

model = LinearRegression()
model.fit(X, y)
pred = model.predict(X)
ANBUYearAnalysisFig = go.Figure(data=[ANBUYearAnalysisData])
ANBUYearAnalysisFig.add_trace(
    go.Scatter(
        x=X.reshape(1, len(X))[0],
        y=pred,
        mode='lines',
        name=f'Regression Line (slope: {model.coef_[0]})',
    ))

# train model
tempData_Summer = None
for key, val in tempDataDist.items():
    val = val.iloc[5:8]
    if '2023' in val.columns:
        val.drop('2023', axis=1, inplace=True)
    val = val.transpose()
    if tempData_Summer is None:
        tempData_Summer = val
    else:
        tempData_Summer = pd.concat([tempData_Summer, val])
tempData_Summer.reset_index(inplace=True, drop=True)

distMeanTemp_warmWinter_Mean = distMeanTemp_winterMouth.mean(axis=0)
distMeanTemp_warmWinter_Std = distMeanTemp_winterMouth.std(axis=0)

distMeanTemp_warmWinter = None
for dist in distMeanTemp_winterMouth:
    isWarmWinter = distMeanTemp_winterMouth[dist].apply(
        lambda t: 1 if t > (distMeanTemp_warmWinter_Mean[dist] +
                            distMeanTemp_warmWinter_Std[dist]) else 0)
    if distMeanTemp_warmWinter is None:
        distMeanTemp_warmWinter = isWarmWinter
    else:
        distMeanTemp_warmWinter = pd.concat(
            [distMeanTemp_warmWinter, isWarmWinter])
distMeanTemp_warmWinter.reset_index(inplace=True, drop=True)
distMeanTemp_warmWinter.name = 'warmWinter'

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import TomekLinks

X = tempData_Summer
y = distMeanTemp_warmWinter
df = X.join(y)
df.dropna(inplace=True)

# df_show_isWarmWinter = df[df['warmWinter'] == 1]
# df_show_notWarmWinter = df[df['warmWinter'] == 0]
# Plot SVM dataset: X,y
# fig = go.FigureWidget()
# fig.add_scatter3d(x=df_show_notWarmWinter[6],
#                   y=df_show_notWarmWinter[7],
#                   z=df_show_notWarmWinter[8],
#                   mode='markers',
#                   marker={'color': 'red'})
# fig.add_scatter3d(x=df_show_isWarmWinter[6],
#                   y=df_show_isWarmWinter[7],
#                   z=df_show_isWarmWinter[8],
#                   mode='markers',
#                   marker={'color': 'blue'})
# fig.show()

# X_train, X_test, y_train, y_test = train_test_split(df[[6, 7, 8]],
#                                                     df['warmWinter'],
#                                                     test_size=0.33)

# X_train, y_train = SMOTE().fit_resample(X_train, y_train)
# X_train, y_train = TomekLinks().fit_resample(X_train, y_train)

# # logist
# logist = LogisticRegression()
# logist.fit(X_train, y_train)
# pred = logist.predict(X_train)

# print(classification_report(y_train, pred))