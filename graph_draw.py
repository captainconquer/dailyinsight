import pandas as pd
import mplfinance as mpf
import os


def plot_candle(df,start_index,end_index,bottom,output_path):
    #df = pd.read_csv(r'D:\stock\history\000001.SZ.csv')
    sub_df = df[['trade_date','open','high','low','close','vol']].copy()
    # daily = sub_df.head(30)
    sub_df.rename(columns={'trade_date':'Date', 'open':'Open', 'high':'High','low':'Low', 'close':'Close','vol':'Volume'}, inplace = True)

    # daily['Date'] = pd.to_datetime(daily['Date'])
    sub_df[['Date']] = sub_df[['Date']].astype(str)
    # print(sub_df['Date'])
    sub_df['Date'] = pd.to_datetime(sub_df['Date'])
    start_date = sub_df['Date'][start_index]
    end_date = sub_df['Date'][end_index]
    sub_df.set_index("Date", inplace=True)


    kwargs = dict(type='candle',volume=True,figratio=(11,8),figscale=0.85)
    mc = mpf.make_marketcolors(up='r',down='g',volume='in')
    s = mpf.make_mpf_style(marketcolors=mc)
    # mpf.plot(daily,**kwargs,style=s,savefig='testsave.png')
    saved_filename = '{}_{}.png'.format(str(start_date).split(' ')[0],df['ts_code'][0].split('.')[0])
    outputfile = os.path.join(output_path,saved_filename)

    # mpf.plot(sub_df, **kwargs, style=s,vlines=dict(vlines=[start_date,end_date],linewidths=(0.5,0.5),linestyle='-.'),\
    #          hlines=dict(hlines=[bottom],linewidths=(0.5),colors=['r'],linestyle='-.'),savefig=outputfile)

    mpf.plot(sub_df, **kwargs, style=s,\
             hlines=dict(hlines=[bottom],linewidths=(0.5),colors=['r'],linestyle='-.'),savefig=outputfile,title=saved_filename)

