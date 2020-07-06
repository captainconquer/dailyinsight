import pandas as pd
import os

def get_guojiadui_stock():
    result = pd.DataFrame(
        columns=('ts_code', 'ann_date', 'end_date', 'holder_name_huijin', 'hold_amount', 'hold_ratio','holder_name_xianggang','hold_amount_xianggang', 'hold_ratio_xianggang'))

    for root,_, files in os.walk('C:\\E\\quant\\winddata\\history\\top10_holders\\'):
        for f in files:
            try:
                csv_file = os.path.join(root, f)
                # csv_file = 'C:\\E\\quant\\winddata\\history\\top10_holders\\000543.SZtop10_holders.csv'
                df = pd.read_csv(csv_file)
                latestDate = df["end_date"].unique()[0]
                latestDF = df[df["end_date"].isin([latestDate])]
                if ('中央汇金资产管理有限责任公司' in latestDF['holder_name'].to_list()) and ('香港中央结算有限公司(陆股通)' in latestDF['holder_name'].to_list()):
                    # print(latestDF)
                    HuiJinDF = df[df["holder_name"].isin(['中央汇金资产管理有限责任公司'])]
                    latestHuiJin = HuiJinDF.head(1)
                    XiangGangDF = df[df["holder_name"].isin(['香港中央结算有限公司(陆股通)'])]
                    latestXiangGang = XiangGangDF.head(1)
                    df_xianggang = latestXiangGang[['holder_name','hold_amount','hold_ratio']]
                    result = result.append(pd.DataFrame({'ts_code': latestHuiJin['ts_code'].values, 'ann_date': latestHuiJin['ann_date'].values,
                                                         'end_date': latestHuiJin['end_date'].values, \
                                                         'holder_name_huijin': latestHuiJin['holder_name'].values,
                                                         'hold_amount': latestHuiJin['hold_amount'].values, \
                                                         'hold_ratio': latestHuiJin['hold_ratio'].values, \
                                                         'holder_name_xianggang': latestXiangGang['holder_name'].values, \
                                                         'hold_amount_xianggang': latestXiangGang['hold_amount'].values, \
                                                         'hold_ratio_xianggang': latestXiangGang['hold_ratio'].values \
                                                         }),
                                           ignore_index=True)
                    breakp = 1
                    # latestHuiJin = latestHuiJin.reset_index(drop=True)
                    # latestXiangGang = latestXiangGang.reset_index(drop=True)
                    # df_merge = pd.merge(latestHuiJin,df_xianggang,left_on='ts_code',right_on='holder_name',how='inner')

                    # result = result.append(df_merge.head(1))
            except Exception as e:
                print(csv_file)
    result.to_csv('.\\guojiadui.csv',encoding='utf-8-sig')

if __name__ == "__main__":
    get_guojiadui_stock()