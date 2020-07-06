import json
import pandas as pd
with open(r'./sortted_stock.json','r',encoding='utf8')as fp:
    json_data = json.load(fp)

df = pd.read_csv(r'D:\stock\history\company\CompanyInfo.csv')

result =pd.DataFrame(columns=('ts_code','acc_rate','chairman','reg_capital','setup_date','province','city','main_business','website'))

# comany_list = [company[0] for company in json_data[0:100]]
# sub_df = df[df['ts_code'].isin(comany_list)]
# sub_df.to_csv(r'BestCompanyMojor.csv',encoding = 'utf-8-sig')
# for company in json_data[0:100]:
for company in json_data:
    sub_df = df[df['ts_code']==company[0]]
    result = result.append(pd.DataFrame({'ts_code':sub_df['ts_code'].values,'acc_rate':[company[1]], 'chairman': sub_df['chairman'].values,\
                                         'reg_capital': sub_df['reg_capital'].values, 'setup_date':sub_df['setup_date'].values, \
                                         'province': sub_df['province'].values,\
                                         'city': sub_df['city'].values, \
                                         'main_business': sub_df['main_business'].values,\
                                         'website': sub_df['website'].values\
                                         }),
                           ignore_index=True)
    # print(sub_df)


result.to_excel(r'BestCompanyMojor.xlsx',encoding = 'utf-8-sig')