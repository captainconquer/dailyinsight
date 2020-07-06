import pandas as pd
import os
import time
import json

from graph_draw import plot_candle
DECLINE_TIME_PERIOD = 4

def analyse_each_stock(df):
    for index, row in df.iterrows():
        if (index <= (DECLINE_TIME_PERIOD-1)):
            continue
    #ts_code	trade_date	open	high	low	close	pre_close	change	pct_chg	vol	amount
        previous_data = df[(index-DECLINE_TIME_PERIOD):index]
        pct_chg = previous_data['pct_chg'].values
        if pct_chg[0]<6:
            continue
        close = previous_data['close'].values
        if close[1]<close[2] or close[2]<close[3]:
            continue
        vol = previous_data['vol'].values
        if vol[1]<vol[2] or vol[2]<vol[3]:
            continue
        print(previous_data)
        sample_df = df[(index-30):(index+60)]
        start_index = index-DECLINE_TIME_PERIOD-1
        end_index = index
        low = previous_data['low'].values
        plot_candle(sample_df,start_index,end_index,low[0])

def check_each_stock(df,outputdir):
    latest_decline_period_df = df[(df.shape[0]-DECLINE_TIME_PERIOD):]
    pct_chg = latest_decline_period_df['pct_chg'].values
    if pct_chg[0]<6:
        return
    close = latest_decline_period_df['close'].values
    if close[1]<close[2] or close[2]<close[3]:
        return
    vol = latest_decline_period_df['vol'].values
    if vol[1]<vol[2] or vol[2]<vol[3]:
        return
    if vol[0]<vol[1]:
        return
    print(latest_decline_period_df)

    low = latest_decline_period_df['low'].values

    plot_candle(df,latest_decline_period_df.index.stop-DECLINE_TIME_PERIOD,latest_decline_period_df.index.stop-1,low[0],outputdir)

def sample_generate_with_allhistory():
    for root,_, files in os.walk('D:\\stock\\history\\pre\\'):
        for f in files:
            csv_file = os.path.join(root, f)
            df = pd.read_csv(csv_file)
            df = df.loc[:, ~df.columns.str.contains('Unnamed')]
            revert_df = df.iloc[::-1]
            revert_df = revert_df.reset_index(drop=True)
            # revert_df.to_csv("D:\\stock\\history\\000001_revert.csv",index=False)
            analyse_each_stock(revert_df)


def sort_all_stocks():
    stock_dic = {}
    for root,_, files in os.walk('D:\\stock\\history\\pre\\'):
        for f in files:
            csv_file = os.path.join(root, f)
            df = pd.read_csv(csv_file)
            df = df.loc[:, ~df.columns.str.contains('Unnamed')]
            revert_df = df.iloc[::-1]
            revert_df = revert_df.reset_index(drop=True)
            # revert_df.to_csv("D:\\stock\\history\\000001_revert.csv",index=False)
            ts_code = revert_df.values[0][0]
            first_open = revert_df.values[0][2]
            latest_open = revert_df.values[-1][2]
            changed_rate = round(latest_open/first_open,3)
            stock_dic[ts_code] = changed_rate

    sortted_dic = sorted(stock_dic.items(), key=lambda item: item[1],reverse = True)
    print(sortted_dic)
    filename = 'sortted_stock.json'
    with open(filename, 'w') as file_obj:
        json.dump(sortted_dic, file_obj)

def daily_insight():
    Currentdate = time.strftime('%Y%m%d', time.localtime(time.time()))
    outputdir = os.path.join('.\\output', Currentdate)
    print('to outputdir = {}'.format(outputdir))
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    for root,_, files in os.walk('D:\\stock\\history\\pre\\'):
        for f in files:
            csv_file = os.path.join(root, f)
            df = pd.read_csv(csv_file)
            if df.shape[0]<34:
                continue
            df = df.head(34)
            df = df.loc[:, ~df.columns.str.contains('Unnamed')]
            revert_df = df.iloc[::-1]
            revert_df = revert_df.reset_index(drop=True)
            # revert_df.to_csv("D:\\stock\\history\\000001_revert.csv",index=False)
            # latest_4df = revert_df.tail(4)
            check_each_stock(revert_df,outputdir)

if __name__ == "__main__":
    # sample_generate_with_allhistory()
    daily_insight()
    # sort_all_stocks()
