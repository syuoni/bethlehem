# -*- coding: utf-8 -*-
import re
import pandas as pd


NO_pt = re.compile('\d{1,2}\.')
colon_pt = re.compile('[:：,，;；]')
name_syn = pd.read_excel('name-syn.xlsx', 'name-syn', index_col='syn', squeeze=True)
name_syn = name_syn.to_dict()


res_exrd = pd.ExcelFile('读经打卡表.xlsx')
last_week_NO = res_exrd.sheet_names[-1]
week_NO = int(re.search('(?<=第)\d+(?=周)', last_week_NO).group()) + 1
week_NO = re.sub('(?<=第)\d+(?=周)', str(week_NO), last_week_NO)
print("Last week: %s" % last_week_NO)
print("This week: %s" % week_NO)


df = pd.read_excel('raw-records.xlsx', week_NO)
last_res = res_exrd.parse(last_week_NO, index_col=0)

name_sr_data = []
for day in df.columns:
    text = df.loc[0, day]
    name_list = []
    for k, record in enumerate(text.split('\n')[1:], 1):
        k_str = str(k)
        assert record[:len(k_str)+1] == ('%d.' % k)
        
        name, *_ = colon_pt.split(record[len(k_str)+1:])
        name = name.strip().replace(' ', '')
        name = name_syn[name] if name in name_syn else name
        name_list.append(name)
    name_list = list(set(name_list))
    name_sr = pd.Series(1, index=name_list, name=day)
    name_sr_data.append(name_sr)
    
rec_df = pd.concat(name_sr_data, axis=1, sort=False)

new_names = [name for name in rec_df.index if name not in last_res.index]
if len(new_names) > 0:
    print('New names: %s' % new_names)
for name in new_names:
    last_res.loc[name] = 0

print('%d people out of records...' % (last_res.shape[0] - rec_df.shape[0]))
print(set(last_res.index) - set(rec_df.index))
rec_df = rec_df.reindex(index=last_res.index)
rec_df = rec_df.fillna(0).astype(int)
rec_df['应缴罚款'] = 6 - rec_df.sum(axis=1)

rec_df.to_excel('count-res/%s.xlsx' % week_NO, week_NO)
