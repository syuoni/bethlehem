# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_excel('Kings.xlsx', 0, header=None, index_col=0)
df = df.loc[df.index.notna()].T

df = df.loc[df['名'].notna()]

df['行善_indic'] = df['行善'].notna()
df['行恶_indic'] = df['行恶'].notna()
print(df.groupby('国家')['行善_indic'].sum())
print(df.groupby('国家')['行恶_indic'].sum())

def parse2year(duration):
    if pd.isna(duration):
        return duration
    elif duration.endswith('年'):
        return float(duration[:-1])
    elif duration.endswith('月'):
        return float(duration[:-1]) / 12
    elif duration.endswith('日'):
        return float(duration[:-1]) / 365
    

df['在位时间_year'] = df['在位时间'].map(parse2year)
df['在位时间_year'].hist(bins=20)

