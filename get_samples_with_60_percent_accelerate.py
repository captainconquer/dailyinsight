import pandas as pd
import os
import numpy as np

def check_each_stock(df):
    one_stock_samples = pd.DataFrame(
        columns=('ts_code', 'start_date', 'end_date', 'accelerate'))

    for i in range(df.shape[0]-34):
        df_in_slid_window = df[i:i+34]

        pct_chg_array = df_in_slid_window['pct_chg'].to_numpy()
        if np.max(pct_chg_array) > 40:
            continue

        high_array = df_in_slid_window['high'].to_numpy()
        low_array = df_in_slid_window['low'].to_numpy()
        if high_array[0] == low_array[0]:
            continue


        close_array = df_in_slid_window['close'].to_numpy()

        start = close_array[0]
        end = close_array[-1]
        accelerate = (end-start)/start
        if accelerate > 0.8:
            one_stock_samples = one_stock_samples.append(
                pd.DataFrame({'ts_code': [df['ts_code'][0]], 'start_date': [df['trade_date'][i]],\
                              'end_date': [df['trade_date'][i+33]], \
                              'accelerate': [round(accelerate,2)]\
                              }), ignore_index=True)
            print("adding sample")
    return(one_stock_samples)

def get_samples_with_60_percent_accelerate():
    result = pd.DataFrame(
        columns=('ts_code', 'start_date', 'end_date', 'accelerate'))
    for root,_, files in os.walk(r'D:\stock\history\pre'):
        for f in files:
            try:
                csv_file = os.path.join(root, f)
                df = pd.read_csv(csv_file)
                if df.shape[0] < 34:
                    continue
                # df = df.head(34)
                df = df.loc[:, ~df.columns.str.contains('Unnamed')]
                revert_df = df.iloc[::-1]
                revert_df = revert_df.reset_index(drop=True)

                result = result.append(check_each_stock(revert_df))

            except Exception as e:
                print("sample generate error for stock {}".format(csv_file))
                print(e)
    result.to_csv('.\\samples_with_80_percent_accelerate.csv',encoding='utf-8-sig')

if __name__ == "__main__":
    get_samples_with_60_percent_accelerate()