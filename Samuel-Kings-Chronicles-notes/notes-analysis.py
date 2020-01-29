# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_excel('Kings.xlsx', 0, header=None, index_col=0)
df = df.loc[df.index.notna()].T

df = df.loc[df['名'].notna()]
df = df.loc[df['名'] != '亚他利雅']

# Check for duplicated names (South vs. North kingdoms)
assert df['名'].value_counts().max() == 1
name_counts = df['名'].str.replace('\[\w\]', '').value_counts()
dup_names = name_counts.index[name_counts > 1].tolist()

check_fathers = []
for father in df['父亲']:
    if not isinstance(father, str):
        continue
    for n in dup_names:
        if n in father:
            check_fathers.append(father)
assert all([f.startswith('[') for f in check_fathers])




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


import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['STSong']

df = df.loc[~df['名'].isin(['扫罗', '大卫', '所罗门'])]
fig, ax = plt.subplots(figsize=(6, 4))

sns.distplot(df.loc[df['国家']=='以色列', '在位时间_year'].values, hist=False, 
             color="r", kde_kws={"shade": True, "bw": 2}, ax=ax, label="以色列")
sns.distplot(df.loc[(df['国家']=='犹大') & df['行善_indic'], '在位时间_year'].values, hist=False, 
             color="g", kde_kws={"shade": True, "bw": 2}, ax=ax, label="犹大（行善）")
sns.distplot(df.loc[(df['国家']=='犹大') & ~df['行善_indic'], '在位时间_year'].values, hist=False, 
             color="b", kde_kws={"shade": True, "bw": 2}, ax=ax, label="犹大（行恶）")
fig.savefig('fig/reigning-years.png', bbox_inches='tight', dpi=300)


