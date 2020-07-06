# -*- coding:utf-8 -*-
import tushare as ts
import datetime,time
import os
import pandas as pd
import re
import numpy as np
import threading
import sys

class tushareStock():
    def __init__(self):
        print(ts.__version__)
        self.pro = ts.pro_api('56abe36c3119312257bb476314729f44f05457e604b54d09c4a09aa7')
        self.sleepTime = 5

    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def AStockHisDataIncome(self,stockCodes,start_date,end_date,step=0):
        print(self.getCurrentTime(),": Download A Stock Starting:")
        for row in stockCodes.itertuples(index=True, name='Pandas'):
            stockCode = getattr(row, "ts_code")
            startDate = getattr(row,"list_date")
            try:
                starttime = time.time()
                histdata = ts.get_hist_data('600848')
                df = self.pro.income(ts_code=stockCode, start_date=startDate, end_date=end_date, fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,basic_eps,diluted_eps')
                endtime = time.time()
                print("Get Data from Pro daily spend time = ",endtime-starttime)
                try:
                    # starttime = time.time()
                    # df.to_sql('STOCKDAILYDATA',self.engine,if_exists='append');
                    # endtime = time.time()
                    # print("Write data to mysql spend time = ",endtime-starttime)

                    filename = 'C:\\E\\quant\\winddata\\history\\csv\\income\\'+stockCode+'.csv'
                    starttime = time.time()
                    df.to_csv(filename, sep=',', header=True, index=True)
                    endtime = time.time()
                    print("Write data to csv spend time = ",endtime-starttime)

                    # filename = 'C:\\E\\quant\\winddata\\history\\json\\'+stockCode+'.json'
                    # starttime = time.time()
                    # df.to_json(filename)
                    # endtime = time.time()
                    # print("Write data to json spend time = ",endtime-starttime)
                except Exception as e:
                    #如果写入数据库失败，写入日志表，便于后续分析处理
                    error_log_dic={}
                    error_log_dic['start_date']=start_date
                    error_log_dic['end_date']=end_date
                    error_log_dic['symbol']=stockCode
                    error_log = pd.DataFrame(error_log_dic,index=[0])
                    # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                    print ( self.getCurrentTime(),": SQL Exception :%s" % (e) )
                    continue
            except Exception as e:
                #如果读取处理失败，可能是网络中断、频繁访问被限、历史数据缺失等原因。写入相关信息到日志表，便于后续补充处理
                error_log_dic={}
                error_log_dic['start_date']=start_date
                error_log_dic['end_date']=end_date
                error_log_dic['symbol']=stockCode
                error_log = pd.DataFrame(error_log_dic,index=[0])
                # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                print (self.getCurrentTime(),":get data from tushare %s : Exception :%s" % (stockCode,e) )
                time.sleep(self.sleepTime)
                continue
            print(self.getCurrentTime(),": Downloading [",stockCode,"] From "+startDate+" to "+end_date)
        print(self.getCurrentTime(),": Download A Stock Has Finished .")

    def AStockHisDataPost(self,stockCodes,start_date,end_date,step=0):
        print(self.getCurrentTime(),": Download A Stock Starting:")
        for row in stockCodes.itertuples(index=True, name='Pandas'):
            stockCode = getattr(row, "ts_code")
            startDate = getattr(row,"list_date")
            try:
                starttime = time.time()
                df = ts.pro_bar(ts_code=stockCode, adj='hfq', start_date=startDate, end_date=end_date)
                endtime = time.time()
                print("Get Data from Pro daily spend time = ",endtime-starttime)
                try:
                    starttime = time.time()
                    # df.to_sql('STOCKDAILYDATA',self.engine,if_exists='append');
                    endtime = time.time()
                    print("Write data to mysql spend time = ",endtime-starttime)

                    filename = 'C:\\E\\quant\\winddata\\history\\csv\\post\\'+stockCode+'.csv'
                    starttime = time.time()
                    df.to_csv(filename, sep=',', header=True, index=True)
                    endtime = time.time()
                    print("Write data to csv spend time = ",endtime-starttime)

                    # filename = 'C:\\E\\quant\\winddata\\history\\json\\'+stockCode+'.json'
                    # starttime = time.time()
                    # df.to_json(filename)
                    # endtime = time.time()
                    # print("Write data to json spend time = ",endtime-starttime)
                except Exception as e:
                    #如果写入数据库失败，写入日志表，便于后续分析处理
                    error_log_dic={}
                    error_log_dic['start_date']=start_date
                    error_log_dic['end_date']=end_date
                    error_log_dic['symbol']=stockCode
                    error_log = pd.DataFrame(error_log_dic,index=[0])
                    # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                    print ( self.getCurrentTime(),": SQL Exception :%s" % (e) )
                    continue
            except Exception as e:
                #如果读取处理失败，可能是网络中断、频繁访问被限、历史数据缺失等原因。写入相关信息到日志表，便于后续补充处理
                error_log_dic={}
                error_log_dic['start_date']=start_date
                error_log_dic['end_date']=end_date
                error_log_dic['symbol']=stockCode
                error_log = pd.DataFrame(error_log_dic,index=[0])
                # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                print (self.getCurrentTime(),":get data from tushare %s : Exception :%s" % (stockCode,e) )
                time.sleep(self.sleepTime)
                continue
            print(self.getCurrentTime(),": Downloading [",stockCode,"] From "+startDate+" to "+end_date)
        print(self.getCurrentTime(),": Download A Stock Has Finished .")

    def AStockHisData(self,stockCodes,start_date,end_date,step=0):
        print(self.getCurrentTime(),": Download A Stock Starting:")
        for row in stockCodes.itertuples(index=True, name='Pandas'):
            stockCode = getattr(row, "ts_code")
            startDate = getattr(row,"list_date")
            filename = 'C:\\E\\quant\\winddata\\history\\csv\\pre\\' + stockCode + '.csv'
            if os.path.exists(filename)==False:
                try:
                    # cps = CountsPerSec().start()
                    starttime = time.time()
                    df_before_2005 = ts.pro_bar(api=self.pro, ts_code=stockCode, adj='hfq', start_date=startDate, end_date="20060104")
                    df_after_2005 = ts.pro_bar(api=self.pro, ts_code=stockCode, adj='hfq', start_date="20060105", end_date=end_date)
                    df = df_after_2005.append(df_before_2005,ignore_index=True)
                    endtime = time.time()
                    print("Get Data from Pro daily spend time = ",endtime-starttime)

                    # starttime = time.time()
                    # npdf = np.array(df)#np.ndarray()
                    # dflist=npdf.tolist()#list
                    # endtime = time.time()
                    # print("df convert to list time spend = ",endtime-starttime)
                    try:
                        # starttime = time.time()
                        # df.to_sql('STOCKDAILYDATA',self.engine,if_exists='append');
                        # endtime = time.time()
                        # print("Write data to mysql spend time = ",endtime-starttime)


                        starttime = time.time()
                        df.to_csv(filename, sep=',', header=True, index=True)
                        endtime = time.time()
                        print("Write data to csv spend time = ",endtime-starttime)

                        # filename = 'C:\\E\\quant\\winddata\\history\\json\\'+stockCode+'.json'
                        # starttime = time.time()
                        # df.to_json(filename)
                        # endtime = time.time()
                        # print("Write data to json spend time = ",endtime-starttime)
                    except Exception as e:
                        #如果写入数据库失败，写入日志表，便于后续分析处理
                        error_log_dic={}
                        error_log_dic['start_date']=start_date
                        error_log_dic['end_date']=end_date
                        error_log_dic['symbol']=stockCode
                        error_log = pd.DataFrame(error_log_dic,index=[0])
                        # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                        print ( self.getCurrentTime(),": SQL Exception :%s" % (e) )
                        continue
                except Exception as e:
                    #如果读取处理失败，可能是网络中断、频繁访问被限、历史数据缺失等原因。写入相关信息到日志表，便于后续补充处理
                    error_log_dic={}
                    error_log_dic['start_date']=start_date
                    error_log_dic['end_date']=end_date
                    error_log_dic['symbol']=stockCode
                    error_log = pd.DataFrame(error_log_dic,index=[0])
                    # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                    print (self.getCurrentTime(),":get data from tushare %s : Exception :%s" % (stockCode,e) )
                    time.sleep(self.sleepTime)
                    continue
                print(self.getCurrentTime(),": Downloading [",stockCode,"] From "+startDate+" to "+end_date)
        print(self.getCurrentTime(),": Download A Stock Has Finished .")

    def UpdateHisData2Old(self,stockCodes,start_date,end_date,step=0):
        print(self.getCurrentTime(),": Download A Stock Starting:")
        for row in stockCodes.itertuples(index=True, name='Pandas'):
            stockCode = getattr(row, "ts_code")
            startDate = getattr(row,"list_date")
            filename = 'C:\\E\\quant\\winddata\\history\\csv\\pre\\' + stockCode + '.csv'
            if os.path.exists(filename):
                CurrentStockData = pd.read_csv(filename,index_col=False)
                if 'Unnamed: 0' in CurrentStockData.columns:
                    CurrentStockData = CurrentStockData.drop('Unnamed: 0', axis=1, inplace=False)
                lastRowNum = CurrentStockData.shape[0]
                lastRow = CurrentStockData.iloc[[lastRowNum-1]]

                earlistDate = long(getattr(lastRow,"trade_date").values)
                if startDate<earlistDate-1:
                    startDate = str(startDate)
                    end_date = str(earlistDate-1)
                else:
                    print ("already earlist data skipping ", stockCode)
                    continue

                try:
                    # cps = CountsPerSec().start()
                    starttime = time.time()
                    # df = self.pro.daily(ts_code=stockCode, start_date=startDate, end_date=end_date)
                    df = ts.pro_bar(api=self.pro, ts_code=stockCode, adj='hfq', start_date=startDate, end_date=end_date)
                    endtime = time.time()
                    print("Get Data from Pro daily spend time = ",endtime-starttime)
                    if df.size == 0:
                        print ("no data avaliable skipping ",stockCode)
                        continue
                    CurrentStockData = CurrentStockData.append(df)
                    # starttime = time.time()
                    # npdf = np.array(df)#np.ndarray()
                    # dflist=npdf.tolist()#list
                    # endtime = time.time()
                    # print("df convert to list time spend = ",endtime-starttime)
                    try:
                        # starttime = time.time()
                        # df.to_sql('STOCKDAILYDATA',self.engine,if_exists='append');
                        # endtime = time.time()
                        # print("Write data to mysql spend time = ",endtime-starttime)


                        starttime = time.time()
                        CurrentStockData.to_csv(filename, sep=',', header=True, index=False)
                        endtime = time.time()
                        print("Write data to csv spend time = ",endtime-starttime)

                        # filename = 'C:\\E\\quant\\winddata\\history\\json\\'+stockCode+'.json'
                        # starttime = time.time()
                        # df.to_json(filename)
                        # endtime = time.time()
                        # print("Write data to json spend time = ",endtime-starttime)
                    except Exception as e:
                        #如果写入数据库失败，写入日志表，便于后续分析处理
                        error_log_dic={}
                        error_log_dic['start_date']=start_date
                        error_log_dic['end_date']=end_date
                        error_log_dic['symbol']=stockCode
                        error_log = pd.DataFrame(error_log_dic,index=[0])
                        # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                        print ( self.getCurrentTime(),": SQL Exception :%s" % (e) )
                        continue
                except Exception as e:
                    #如果读取处理失败，可能是网络中断、频繁访问被限、历史数据缺失等原因。写入相关信息到日志表，便于后续补充处理
                    error_log_dic={}
                    error_log_dic['start_date']=start_date
                    error_log_dic['end_date']=end_date
                    error_log_dic['symbol']=stockCode
                    error_log = pd.DataFrame(error_log_dic,index=[0])
                    # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                    print (self.getCurrentTime(),":get data from tushare %s : Exception :%s" % (stockCode,e) )
                    time.sleep(self.sleepTime)
                    continue
                print(self.getCurrentTime(),": Downloading [",stockCode,"] From "+startDate+" to "+end_date)
        print(self.getCurrentTime(),": Download A Stock Has Finished .")
    thread_number = 30
    def mult_thread_UpdateHisData2Newest(self,stockCodes,end_date):
        sub_df_len = int(stockCodes.shape[0]/self.thread_number)
        extra_line_number = stockCodes.shape[0] % self.thread_number

        for i in range(self.thread_number):

            if ((i ==  (self.thread_number-1)) and (extra_line_number>0)):
                end_line = ((i+1)*sub_df_len)+extra_line_number
            else:
                end_line = (i+1)*sub_df_len
            start_line = (i)*sub_df_len
            sub_stockCodes = stockCodes[start_line:end_line :]
            t = threading.Thread(target=self.UpdateHisData2Newest, args=(sub_stockCodes,end_date))
            t.start()

    def UpdateHisData2Newest(self,stockCodes,end_date):
        print(self.getCurrentTime(),": Download A Stock Starting: \n")
        currentDate = int(end_date)
        for row in stockCodes.itertuples(index=True, name='Pandas'):
            stockCode = getattr(row, "ts_code")
            # stockCode = "000001.SZ"
            filename = 'D:\\stock\\history\\pre\\' + stockCode + '.csv'
            if os.path.exists(filename):
                CurrentStockData = pd.read_csv(filename,index_col=False)
                if 'Unnamed: 0' in CurrentStockData.columns:
                    CurrentStockData = CurrentStockData.drop('Unnamed: 0', axis=1, inplace=False)
                LatestRow = CurrentStockData.iloc[[0]]

                LatestDate = int(getattr(LatestRow,"trade_date").values)
                if currentDate>LatestDate:
                    startDate = str(LatestDate+1)
                    end_date = str(currentDate)
                else:
                    print ("Already latest data skipping {}\n".format(stockCode))
                    continue
                # if (startDate == end_date):
                #     print ("Already latest data skipping \n".format(stockCode))
                #     continue
                try:
                    starttime = time.time()
                    df = ts.pro_bar(api=self.pro, ts_code=stockCode, adj='hfq', start_date=startDate, end_date=end_date)
                    endtime = time.time()
                    print("Get Data from Pro daily spend time = {}\n".format(endtime-starttime))
                    if df.size == 0:
                        print ("no data avaliable skipping {}\n".format(stockCode))
                        continue
                    df = df.append(CurrentStockData)

                    try:
                        starttime = time.time()
                        df.to_csv(filename, sep=',', header=True, index=False)
                        endtime = time.time()
                        print("Write data to csv spend time = ",endtime-starttime)
                    except Exception as e:
                        error_log_dic={}
                        error_log_dic['start_date']=startDate
                        error_log_dic['end_date']=end_date
                        error_log_dic['symbol']=stockCode
                        error_log = pd.DataFrame(error_log_dic,index=[0])
                        print ( self.getCurrentTime(),": SQL Exception :%s" % (e) )
                        continue
                except Exception as e:
                    error_log_dic={}
                    error_log_dic['start_date']=startDate
                    error_log_dic['end_date']=end_date
                    error_log_dic['symbol']=stockCode
                    error_log = pd.DataFrame(error_log_dic,index=[0])
                    # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                    print (self.getCurrentTime(),":get data from tushare %s : Exception :%s" % (stockCode,e) )
                    time.sleep(self.sleepTime)
                    continue
                print(self.getCurrentTime(),": Downloading [",stockCode,"] From "+startDate+" to "+end_date+'\n')
        print(self.getCurrentTime(),": Download A Stock Has Finished .")

    def getIndex_daily(self):
        data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

        df = self.pro.index_daily(ts_code='000001.SH')
        df.to_csv('C:\\E\\quant\\winddata\\history\\000001.csv', sep=',', header=True, index=False)

        df = self.pro.index_basic(market='SSE')
        # df.to_csv('C:\\E\\quant\\winddata\\history\\sse.csv',encoding='unicode')
        df.to_csv('C:\\E\\quant\\winddata\\history\\sse.csv',encoding = 'utf-8-sig')


    def getAStockCodesFromCsv(self):
        '''
        获取股票代码清单，链接数据库
        '''
        file_path=os.path.join(os.getcwd(),'Stock.csv')
        stock_code = pd.read_csv(filepath_or_buffer=file_path, encoding='gbk')
        Code=stock_code.code
        return Code

    def getAStockCodesFromTushare(self,end_date=time.strftime('%Y%m%d',time.localtime(time.time()))):
        '''
        通过wset数据集获取所有A股股票代码，深市代码为股票代码+SZ后缀，沪市代码为股票代码+SH后缀。
        如设定日期参数，则获取参数指定日期所有A股代码，不指定日期参数则默认为当前日期
        :return: 指定日期所有A股代码，不指定日期默认为最新日期
        '''
        data = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        # data.to_sql('stockcode',self.engine,if_exists='replace')
        print(data)
        return data

    def getStockCodeFromErrorlog(self):
        stockcodelist = []
        sql = '''
              select * from stockerrorlog;
              '''
        # df = pd.read_sql_query(sql, self.engine)
        # for indexs in df.index:
        #     print(df.loc[indexs].values)
        #     sc = re.findall(r"error: (.+?) From",str(df.loc[indexs].values))[0]
        #     stockcodelist.append(sc)
        #     print(sc)

        for row in df.itertuples(index=True, name='Pandas'):
            symbol = getattr(row, "symbol")
            stockCode = re.findall(r"error: (.+?) From",str(symbol))[0]
            startDate = getattr(row,"start_date")
            end_date = getattr(row,"end_date")
            try:
                # cps = CountsPerSec().start()
                starttime = time.time()
                df = self.pro.daily(ts_code=stockCode, start_date=startDate, end_date=end_date)
                endtime = time.time()
                print("Get Data from Pro daily spend time = ",endtime-starttime)
                try:
                    starttime = time.time()
                    # df.to_sql('stockdailydata',self.engine,if_exists='append')
                    endtime = time.time()
                    print("Write data to mysql spend time = ",endtime-starttime)
                except Exception as e:
                    #如果写入数据库失败，写入日志表，便于后续分析处理
                    error_log_dic={}
                    error_log_dic['start_date']=startDate
                    error_log_dic['end_date']=end_date
                    error_log_dic['symbol']=stockCode
                    error_log = pd.DataFrame(error_log_dic,index=[0])
                    # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                    print ( self.getCurrentTime(),": SQL Exception :%s" % (e) )
                    continue
            except Exception as e:
                #如果读取处理失败，可能是网络中断、频繁访问被限、历史数据缺失等原因。写入相关信息到日志表，便于后续补充处理
                error_log_dic={}
                error_log_dic['start_date']=startDate
                error_log_dic['end_date']=end_date
                error_log_dic['symbol']=stockCode
                error_log = pd.DataFrame(error_log_dic,index=[0])
                # error_log.to_sql('stockerrorlog',self.engine,if_exists='append')
                print (self.getCurrentTime(),":get data from tushare %s : Exception :%s" % (stockCode,e) )
                time.sleep(self.sleepTime)
                continue
            print(self.getCurrentTime(),": Downloading [",stockCode,"] From "+startDate+" to "+end_date)

def main():
    '''
    主调函数，可以通过参数调整实现分批下载
    '''
    stockManager=tushareStock()

    # stockManager.getIndex_daily()

    # stockManager.getStockCodeFromErrorlog()
    stocklistfile = 'D:\\stock\\history\\stocklist.csv'
    # if os.path.exists(stocklistfile)==False:
    if True:
        stockCodes = stockManager.getAStockCodesFromTushare()
        stockCodes.to_csv(stocklistfile, sep=',', header=True, index=True,encoding='utf-8-sig')
    else:
        stockCodes = pd.read_csv(stocklistfile)


    start_date='20140101'
    end_date = stockManager.getCurrentTime()
    end_date=end_date[1:5]+end_date[6:8]+end_date[9:11]

    # stockManager.AStockHisData(stockCodes,start_date,end_date)#获取向后复权历史数据
    # stockManager.UpdateHisData2Old(stockCodes, start_date, end_date)  # 更新历史数据
    stockManager.mult_thread_UpdateHisData2Newest(stockCodes, end_date) #更新到最新历史数据


    # stockManager.AStockHisDataPost(stockCodes,start_date,end_date)
    # stockManager.AStockHisDataIncome(stockCodes,start_date,end_date)


if __name__ == "__main__":
    main()
