import os
import re
import numpy as np
import pandas as pd

# file import
fileToDistrict = {
    '466910': 'Taipei ANBU',
    '466920': 'Taipei TAIPEI',
    '466921': 'Taipei X',
    '466930': 'Taipei ZHUZIHU',
    '466880': 'NewTaipei BANQIAO X',
    '466881': 'NewTaipei New Taipei',
    '466900': 'NewTaipei TAMSUI',
    'C0A520': 'NewTaipei Shanjia',
    '467490': 'Taichung TAICHUNG',
    '467770': 'Taichung WUQI X',
    'C0F000': 'Taichung Dadu',
    'C0F0A0': 'Taichung Xueshanjuangu',
    '467410': 'Tainan TAINAN',
    '467420': 'Tainan YONGKANG',
    '467780': 'Tainan QIGU X',
    'C0N010': 'Tainan KunshenElementarySchool',
    '467440': 'Kaohsiung KAOHSIUNG X',
    '467441': 'Kaohsiung Kaohsiung',
    'C0V210': 'Kaohsiung Fuxing',
    'C0V250': 'Kaohsiung Jiasian',
    '466940': 'Keelung KEELUNG',
    '466950': 'Keelung PENGJIAYU',
    'C0B010': 'Keelung Qidu',
    'C0B020': 'Keelung KeelungIslet',
    '467050': 'Taoyuan XINWU',
    'C0C460': 'Taoyuan Fuxing',
    'C0C480': 'Taoyuan Taoyuan',
    'C0C490': 'Taoyuan Bade',
    'C0D660': 'Hsinshu Dongqu',
    'C0D670': 'Hsinshu HAITIANYISIAN',
    'C0D680': 'Hsinshu SIANGSHANWETLAND',
    'C0D570': 'Hsinshu Siangshan X',
    '467571': 'Hsinshu HSINCHU',
    'C0D360': 'Hsinshu Meihua',
    'C0D390': 'Hsinshu Guanxi',
    'C0D430': 'Hsinshu Emei',
    'C0E420': 'Miaoli Jhunan',
    'C0E430': 'Miaoli Nanzhuang',
    'C0E520': 'Miaoli Dahu',
    'C0E540': 'Miaoli Houlong',
    '467550': 'Nantou YUSHAN',
    '467650': 'Nantou SUNMOONLAKE',
    'C0H890': 'Nantou Puli',
    'C0H950': 'Nantou Zhongliao',
    '467270': 'Changhua TianZhong',
    'C0G860': 'Changhua Shetou',
    'C0G870': 'Changhua Fangyuan',
    'C0G880': 'Changhua Ershui',
    'C0K240': 'Yunlin Caoling',
    'C0K250': 'Yunlin Lunbei',
    'C0K280': 'Yunlin Sihu',
    'C0K291': 'Yunlin Yiwu',
    '467480': 'Chiayi CHIAYI',
    'C0M730': 'Chiayi Dongqu',
    '467530': 'Chiayi ALISHAN',
    'C0M410': 'Chiayi Matoushan',
    'C0M520': 'Chiayi Donghouliao',
    'C0M530': 'Chiayi Fenqihu',
    '467590': 'Pingtung HENGCHUN',
    'C0R540': 'Pingtung Jiadong',
    'C0R550': 'Pingtung Xinpi',
    'C0R560': 'Pingtung Xinyuan',
    '467060': "Yilan SU-AO",
    '467080': 'Yilan YILAN',
    'C0U520': 'Yilan Shuanglianpi',
    'C0U600': 'Yilan Chiaoshi',
    '466990': 'Hualien HUALIEN',
    'C0T790': 'Hualien Dayuling',
    'C0T820': 'Hualien Tianxiang',
    'C0T9D0': 'Hualien Hezhong',
    '467540': 'Taitung DAWU',
    '467610': 'Taitung CHENGGONG',
    '467620': 'Taitung LANYU',
    '467660': 'Taitung TAITUNG',
    '467300': 'Penghu DONGJIDAO',
    '467350': 'Penghu PENGHU',
    'C0W120': 'Penghu Xiyu',
    'C0W130': 'Penghu Huayu',
    '467110': 'Kinmen KINMEN',
    'C0W140': 'Kinmen Jinsha',
    'C0W150': 'Kinmen Jinning',
    'C0W160': 'Kinmen Wuqiu',
    '467990': 'Lienchiang MATSU',
    'C0W110': 'Lienchiang Dongju',
    'C0W170': 'Lienchiang Dongyin X'
}

fileList = os.listdir("./data2")

uniqueFileList = np.array(tuple(map(lambda s: s.split('-')[0], fileList)))
uniqueFileList = np.unique(uniqueFileList)

dataDict = {}

for uf in uniqueFileList:
    district = fileToDistrict[uf]
    dataDict[district] = []
    for f in filter(lambda s: s.find(uf) != -1, fileList):
        df = pd.read_csv(f"./data2/{f}")
        df.replace('...', np.nan, inplace=True)
        df.replace('/', np.nan, inplace=True)
        df.replace('X', np.nan, inplace=True)
        df.columns = pd.MultiIndex.from_product(
            [[re.split("[-.]", f)[1]], df.columns], names=['Year', 'info'])
        dataDict[district].append(df)
