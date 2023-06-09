import numpy as np
import pandas as pd
import datapane as dp

from excelImport import *

# produce Temperature dataset
TempDataSet = {}
for key in dataDict:
    for data in dataDict[key]:
        if key not in TempDataSet.keys():
            TempDataSet[key] = data.xs('氣溫(℃)', level='info', axis=1)
        else:
            TempDataSet[key] = pd.concat(
                [TempDataSet[key],
                 data.xs('氣溫(℃)', level='info', axis=1)],
                axis=1)
    TempDataSet[key].drop(0, inplace=True)
    TempDataSet[key] = TempDataSet[key].astype('float')

TempDataSet = pd.read_excel('./outputExcel/tempData.xlsx')
distMeanTemp_winterMonth = None
for district, df in zip(TempDataSet.keys(), TempDataSet.values()):
    df_winterMonth = df.loc[[1, 2]]
    df_winterMonth.loc[12] = df.loc[12].shift(1)
    if distMeanTemp_winterMonth is None:
        distMeanTemp_winterMonth = pd.DataFrame(df_winterMonth.mean(),
                                                columns=[district])
    else:
        distMeanTemp_winterMonth = pd.concat([
            distMeanTemp_winterMonth,
            pd.DataFrame(df_winterMonth.mean(), columns=[district])
        ],
                                             axis=1)

# distMeanTemp_winterMonth = None
# for district, df in zip(TempDataSet.keys(), TempDataSet.values()):
#     df_winterMonth = df.loc[[1, 2]]
#     df_winterMonth.loc[12] = df.loc[12].shift(1)
#     if distMeanTemp_winterMonth is None:
#         distMeanTemp_winterMonth = pd.DataFrame(df_winterMonth.mean(),
#                                                 columns=[district])
#     else:
#         distMeanTemp_winterMonth = pd.concat([
#             distMeanTemp_winterMonth,
#             pd.DataFrame(df_winterMonth.mean(), columns=[district])
#         ],
#                                              axis=1)

# distMeanTemp_Yearly = None
# for district, df in zip(TempDataSet.keys(), TempDataSet.values()):
#     if distMeanTemp_Yearly is None:
#         distMeanTemp_Yearly = pd.DataFrame(df.mean(), columns=[district])
#     else:
#         distMeanTemp_Yearly = pd.concat(
#             [distMeanTemp_Yearly,
#              pd.DataFrame(df.mean(), columns=[district])],
#             axis=1)

# dataTableBlockList = []
# for district, df in zip(TempDataSet.keys(), TempDataSet.values()):
#     dataTableBlockList.append(dp.DataTable(df, label=district))

# with pd.ExcelWriter('./outputExcel/tempData.xlsx',
#                     mode="a",
#                     engine="openpyxl") as writer:
#     df.to_excel(writer, sheet_name=district)

# distMeanTemp_Yearly.sort_index(inplace=True)
# distMeanTemp_Yearly.to_excel('./outputExcel/distMeanTemp_Yearly.xlsx', 'new1')

distMeanTemp_winterMonth.sort_index(inplace=True)
distMeanTemp_winterMonth.to_excel(
    './outputExcel/distMeanTemp_winterMonth.xlsx', 'new1')
