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

ANBUWinterYearAnalysisData = dict(type='scatter',
                                  x=distMeanTemp_winterMouth.index,
                                  y=distMeanTemp_winterMouth['Taipei ANBU'],
                                  name='Taipei ANBU')
ANBUWinterYearAnalysisFig = go.Figure(data=[ANBUWinterYearAnalysisData])
ANBUWinterYearMean = np.mean(distMeanTemp_winterMouth['Taipei ANBU'])
ANBUWinterYearStd = np.std(distMeanTemp_winterMouth['Taipei ANBU'])
ANBUWinterYearAnalysisFig.add_trace(
    go.Scatter(
        x=distMeanTemp_winterMouth.index,
        y=[
            ANBUWinterYearMean
            for i in range(len(distMeanTemp_winterMouth.index))
        ],
        mode='lines',
        name='28年總平均',
    ))
ANBUWinterYearAnalysisFig.add_trace(
    go.Scatter(x=distMeanTemp_winterMouth.index,
               y=[
                   ANBUWinterYearMean + ANBUWinterYearStd
                   for i in range(len(distMeanTemp_winterMouth.index))
               ],
               mode='lines',
               name='平均值 + 一個標準差'))
ANBUWinterYearAnalysisFig.add_trace(
    go.Scatter(x=distMeanTemp_winterMouth.index,
               y=[
                   ANBUWinterYearMean - ANBUWinterYearStd
                   for i in range(len(distMeanTemp_winterMouth.index))
               ],
               mode='lines',
               name='平均值 - 一個標準差'))

tempDistributeFigList = {}
for dist, df in zip(tempDataDist.keys(), tempDataDist.values()):
    if dist == 'Year':
        continue

    fig = df.figure(
        kind='box', boxpoints='all',
        mean='sd')  # boxmean='sd' represent mean and standard deviation
    fig.update_traces(boxmean='sd', selector=dict(type='box'))

    tempDistributeFigList[dist] = fig

dataTableBlockList = []
for dist, df in zip(tempDataDist.keys(), tempDataDist.values()):
    dataTableBlockList.append(dp.DataTable(df, label=dist))

tempDistributeBlockList = []
for dist, fig in zip(tempDistributeFigList.keys(),
                     tempDistributeFigList.values()):
    tempDistributeBlockList.append(dp.Plot(fig, label=dist))

app = dp.App(
    '# 到底什麼是暖冬？', '## Intro',
    '冬天看新聞時常常都會聽到暖冬這個詞，不過到底什麼是暖冬，"暖冬"不曾出現在教科書，也沒有明確的統計數字，應該如何理解它呢？常常聽到的這個詞有沒有什麼毛病。基於好奇與批判思考的精神，我做了這小小的分析，對於天氣的了解不深，統計也沒學好，如有誤敬請指教。',
    '## Temperature Changing Graph of Every Winter Months (1,2,12)',
    dp.Plot(distMeanTemp_winterMouthFig),
    "## Temperature Changing Graph of Every district",
    dp.Plot(distMeanTemp_YearlyFig), '## 各縣市各年每月氣溫分布',
    dp.Select(blocks=tempDistributeBlockList), '<hr/>',
    '<strong>Temperature Changing Graph of Every Winter Months (1,2,12)</strong>可以知道每年的冬季月平均溫度',
    '**Temperature Changing Graph of Every district**則是整年的平均溫度折線圖，圖中在末端有些混亂，可能是此統計只採納到2023年的1月，故有所偏差，加上網路上天氣資料取得不易，資料有些殘缺造成的，但整體來說，氣溫是緩慢上升的，且全台年氣溫變化趨勢差不多。',
    '由各縣市各年每月氣溫分布可以知道氣溫的分布離散程度，雖然月氣溫是以平均計算，極端值會被中和掉，或者抵銷，造成離散分布可能沒那麼明顯，但仍可以從此看到一些資訊，即是，離散的程度沒有那麼的誇張，以這些方式呈現似乎看不出極端氣候。不過台灣原本就處於中低緯度，對於極端氣候的影響不明顯。',
    '### Take Taipei ANBU for example',
    dp.Plot(ANBUYearAnalysisFig, caption='平均年氣溫折線圖'),
    '**以台北鞍部也就是陽明山那裏為例子**上圖可以看出氣候暖化以約0.022度/年速度上升，比較北邊的國家：韓國，1971~2009的上升速度為0.0423度/年',
    '![koreaYearTemp](./img/koreaYearTemp.png)',
    '而其他資訊可以到上面的圖表查詢，點擊右邊的字，該資訊就會隱藏或顯示，雙擊就是全部顯示或除了點擊到的留下其他全部隱藏', '<hr/>',
    '還記得2020和2019被新聞稱為暖冬嗎？其實在此例子中它們確實很暖，至於2021呢？似乎不能被稱為暖冬，但暖冬到底怎麼定義？',
    "### Let's Define",
    '其實完全沒有定義，科學家並沒有為這個名詞做定義，也就是我也不知道暖冬到底代表什麼，這就像今天天氣很冷一樣，冷到底是多少度？有些人這樣定義：**冷暖年 = ﹝該年冬季平均溫度﹞+或-﹝30年冬季平均氣溫標準差﹞**，於是我也這樣試著去定義來產生圖，但我沒有30年的資料，於是只採用28年。',
    dp.Plot(ANBUWinterYearAnalysisFig), '以此定義來看2020、2019確實是暖冬',
    '* **Wait a minute, so called "Warm winter" is mean the winter in this year is warm. But when news say this winter is a warm winter, the winter didn\'t end. So, it is nonsense.**',
    '看得懂英文就知道我在說什麼了，這是我在資料搜尋、思考時，發現一個重要弊端而脫口而出的英文：新聞說的冷暖冬往往都是在冬天還未結束時宣布的，但這往往不是專業統計人員所會說的話，因為要定義一段時間的氣候現象，往往要等到該段時間結束，完成統計，才能稱該年冬季為冷暖冬，但實際上新聞並不是這樣的。',
    '## 總結',
    '做到後面其實已經有點疲乏，隨著暖冬的定義越來越模糊，這個統計資料也越不重要，氣候原本就多少會不太準確，受到很多因素影響。\n總的來說，台灣的極端氣候不太明顯，暖化趨勢也不大，至於新聞的冷暖月就聽聽就好吧。',
    '## DataSet', '**列出所有所用資料( 已整理過 )**', dp.DataTable(distMeanTemp_Yearly),
    dp.Select(blocks=dataTableBlockList),
    '### The dataTable of Temperature Changing Graph of Every Winter Months',
    dp.DataTable(distMeanTemp_winterMouth),
    '[原資料所在位置](https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp)',
    '## reference',
    '[warm winter ref 1](https://www.atmos.pccu.edu.tw/asWeb/wp-content/uploads/2021/01/103%E5%AD%B8%E5%B9%B4%E5%BA%A6%E7%95%A2%E5%B1%95%E7%AC%AC6%E7%B5%84.pdf)',
    '[warm winter ref 2](http://web2.yzu.edu.tw/e_news/438/student/02.htm)',
    '[第 50 屆中小學科展:地球真的發燒了嗎？-深入探討全球暖化的趨勢](https://twsf.ntsec.gov.tw/activity/race-1/50/pdf/040503.pdf)'
)
app.save(path="simple-app.html", open=True)