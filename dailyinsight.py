from rqalpha.apis import *
import talib
import numpy as np
from rqalpha.utils.datetime_func import convert_date_to_int, convert_int_to_date
import pandas as pd
class DailyStockStatus():
    def __init__(self,StockID,GoldenPrice):
        self.StockID = StockID
        self.GoldenPrice = GoldenPrice
        self.MinPrice = 0
        self.DateTimeMax = 0
        self.DateTimeMin = 0
        self.MaxPrice = 0

class SelfSelectedPool():
    def __init__(self):
        self.stock_pool = {}

    def update(self, context):
        for stock in context.stocks:
            if stock in self.stock_pool:
                #忽略已经在股票池中的股票
                continue
            # 读取历史数据
            prices = history_bars(stock, context.DECLINE_TIME_PERIOD + 1, '1d',None,True,False,'post')
            if prices.size < (context.DECLINE_TIME_PERIOD+1):
                continue

            #判断股价当天是否出现最小值
            stock_low = prices['low']
            MinPrice = np.min(stock_low)
            MinPrice_index = stock_low.argmin()
            date_time = prices['datetime']
            DateTimeMin = date_time[MinPrice_index]
            dt = np.uint64(convert_date_to_int(context.now))
            if dt != DateTimeMin:
                continue
            # 如果跌到黄金分割位则加入stock pool
            stock_high = prices['high']
            MaxPrice = np.max(stock_high)

            golden_price = MaxPrice * context.GOLDEN_RATIO
            close_price = prices[-1]['close']
            if not stock_price_equal(MinPrice, golden_price, context.UNCERTAINTY_RATE):
                continue

            prices318 = history_bars(stock, 318, '1d', None, True, False, 'post')
            if prices318.size < (318):
                continue
            ma318 = sum(prices318['close']) / 318

            prices110 = history_bars(stock, 110, '1d', None, True, False, 'post')
            if prices110.size < (110):
                continue
            ma110 = sum(prices110['close'])/110

            prices250 = history_bars(stock, 250, '1d', None, True, False, 'post')
            if prices250.size < (250):
                continue
            ma250 = sum(prices250['close']) / 250
            # if ma120<ma318 or ma318>ma250 or ma120<ma250:
            #     continue
            if not (stock_price_equal(MinPrice, ma110, context.UNCERTAINTY_RATE) or stock_price_equal(MinPrice, ma250, context.UNCERTAINTY_RATE) \
                    or stock_price_equal(MinPrice, ma318, context.UNCERTAINTY_RATE)):
                continue

            # if stock not in context.sample['StockID'].values:
            if True:
                self.stock_pool[stock] = DailyStockStatus(stock[0:6],golden_price)
                self.stock_pool[stock].DateTimeMin = DateTimeMin
                MaxPrice_index = np.where(stock_high == MaxPrice)[-1][-1]
                self.stock_pool[stock].DateTimeMax = date_time[MaxPrice_index]
                self.stock_pool[stock].MinPrice = MinPrice
                self.stock_pool[stock].MaxPrice = MaxPrice
                #logger.info(stock + " added to self selected stock pool")
        #每天更新加入到了股票池里面的每只股票的状态
        for stock in list(self.stock_pool.keys()):
            # 读取历史数据
            prices = history_bars(stock, context.DECLINE_TIME_PERIOD + 1, '1d',None,True,False,'post')
            low_price = prices[-1]['low']
            if low_price < self.stock_pool[stock].MinPrice:
                # 股价创出新低，更新股票最低价
                self.stock_pool[stock].MinPrice = low_price
                # del self.stock_pool[stock]
                dt = np.uint64(convert_date_to_int(context.now))
                self.stock_pool[stock].DateTimeMin = dt
                logger.info(stock + " falling with new lowest price")
            else:
                sampledata={'StockID':stock,
                            # 'GoldenPrice':self.stock_pool[stock].GoldenPrice,
                            'MinPrice':self.stock_pool[stock].MinPrice,
                            'DateTimeMin': [int(self.stock_pool[stock].DateTimeMin / 1000000)],
                            'DateTimeMax':[int(self.stock_pool[stock].DateTimeMax/1000000)],
                            # 'MaxPrice':self.stock_pool[stock].MaxPrice,
                            'Change':'0%',
                            'symbol':context.stocksmap[stock],
                            'Downdays':0,
                            'MaxDrawdown':0,
                            'DateDownMin':0,
                            'Updays':0,
                            'MaxChange':0,
                            'DateUpMax':0}
                context.sample=context.sample.append(pd.DataFrame(sampledata),ignore_index=False)

                context.sample.reset_index(drop=True, inplace=True)
                # context.sample.set_index('DateTimeMin')
                del self.stock_pool[stock]
        # context.MonitoringDays
        Index2BeDeleted = []
        for index, row in context.sample.iterrows():
            #1. 获取增长最大幅度，以及增长天数
            DateTimeGolden = row['DateTimeMin']
            DateNow = str(int((convert_date_to_int(context.now))/1000000))
            (DateTimeGoldenPrice2Now,) = get_trading_dates(str(DateTimeGolden), end_date=DateNow).shape
            if DateTimeGoldenPrice2Now>context.MonitoringDays:
                Index2BeDeleted.append(index)
                continue
            prices = history_bars(row['StockID'], DateTimeGoldenPrice2Now, '1d',None,True,False,'post')
            stock_high = prices['high']
            MaxPrice = np.max(stock_high)



            # stock_low = prices['low']
            # MinPrice = np.min(stock_low)
            MinPrice = row['MinPrice']
            date_time = prices['datetime']

            # date_time = prices['datetime']
            MaxPrice_index = np.where(stock_high == MaxPrice)[-1][-1]
            # MinPrice_index = np.where(stock_low == MinPrice)[-1][-1]
            DateTimeMax = int(date_time[MaxPrice_index]/1000000)

            (UpdayNums,) = get_trading_dates(str(DateTimeGolden), str(DateTimeMax)).shape
            UpdayNums = UpdayNums-1
            Updays_index = list(context.sample.columns).index('Updays')
            context.sample.iloc[index,Updays_index] = UpdayNums

            if UpdayNums>0:
                MaxChange = str(round(((MaxPrice-MinPrice)/MinPrice)*100,2))+'%'
                MaxChange_index = list(context.sample.columns).index('MaxChange')
                context.sample.iloc[index,MaxChange_index] = MaxChange

                DateUpMax_index = list(context.sample.columns).index('DateUpMax')
                context.sample.iloc[index,DateUpMax_index] = int(DateTimeMax)
            #2. 获取下跌最大幅度以及下跌天数
            DateNow = str(int((convert_date_to_int(context.now))/1000000))
            (DateNumMinePrice2Now,) = get_trading_dates(str(DateTimeGolden), end_date=DateNow).shape
            prices = history_bars(row['StockID'], DateNumMinePrice2Now, '1d',None,True,False,'post')
            stock_low = prices['low']
            MinPrice = np.min(stock_low)

            # stock_low = prices['low']
            # MinPrice = np.min(stock_low)
            GoldenPrice = row['MinPrice']
            date_time = prices['datetime']

            # date_time = prices['datetime']
            MinPrice_index = np.where(stock_low == MinPrice)[-1][-1]
            # MinPrice_index = np.where(stock_low == MinPrice)[-1][-1]
            DateTimeMin = int(date_time[MinPrice_index]/1000000)
            # if (row['StockID']=='300631.XSHE'):
            #     DateTimeMin = DateTimeMin

            (DowndayNums,) = get_trading_dates(str(DateTimeGolden), str(DateTimeMin)).shape
            DowndayNums = DowndayNums-1
            Downdays_index = list(context.sample.columns).index('Downdays')
            context.sample.iloc[index,Downdays_index] = DowndayNums

            if DowndayNums>0:
                MaxDrawdown = str(round(((MinPrice-GoldenPrice)/GoldenPrice)*100,2))+'%'
                MaxDrawdown_index = list(context.sample.columns).index('MaxDrawdown')
                context.sample.iloc[index,MaxDrawdown_index] = MaxDrawdown

                DateDownMin_index = list(context.sample.columns).index('DateDownMin')
                context.sample.iloc[index,DateDownMin_index] = int(DateTimeMin)
            #3. 更新每天股价
            MinPrice = row['MinPrice']
            Close = prices[-1]['close']
            Change = str(round(((Close-MinPrice)/MinPrice)*100,2))+'%'
            Change_index = list(context.sample.columns).index('Change')
            context.sample.iloc[index,Change_index] = Change
        if len(Index2BeDeleted)>0:
            context.sample.drop(index=Index2BeDeleted)

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")
    context.self_selected_pool = SelfSelectedPool()
    all_instrument = all_instruments('CS')
    # stocklist = all_instrument.values.tolist()
    # context.stocks = []
    # for stock in stocklist:
    #     #logger.info(stock[13] + ' '+stock[7]+'\n')
    #     context.stocks.append(stock[8])
    context.stocks = all_instrument['order_book_id'].tolist()
    context.symbols = all_instrument['symbol'].tolist()
    context.stocksmap = {}
    for stock, symbol in zip(context.stocks,context.symbols):
        context.stocksmap[stock] = symbol
    #logger.info(context.stocks)
    # context.stocks = ["300631.XSHE"]

    context.DECLINE_TIME_PERIOD = 34
    context.GOLDEN_RATIO = 0.6792
    context.UNCERTAINTY_RATE = 0.02

    context.sample = pd.DataFrame(columns=('StockID',
                                           # 'GoldenPrice',
                                           'DateTimeMin',
                                           'MinPrice',
                                           'DateTimeMax',
                                           # 'MaxPrice',
                                           'Change',
                                           'symbol',
                                           'Downdays',
                                           'MaxDrawdown',
                                           'DateDownMin',
                                           'Updays',
                                           'MaxChange',
                                           'DateUpMax'))
    context.MonitoringDays = 34
#result = df1.append(df2)
def before_trading(context):
    pass

def stock_price_equal(stock_price, target, uncertainty_rate):
    return all([(stock_price<(target*(1+uncertainty_rate))),(stock_price>(target*(1-uncertainty_rate)))])



def handle_bar(context, bar_dict):
    # TODO: 开始编写你的算法吧！
    context.self_selected_pool.update(context)