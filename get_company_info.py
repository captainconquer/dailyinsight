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
        # self.engine = create_engine('mysql+mysqldb://root:root@127.0.0.1/history?charset=utf8')
        self.sleepTime = 5

    def getCurrentTime(self):
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def UpdateHisDataCompanyInfo(self):
        filename = 'D:\\stock\\history\\company\\' + 'CompanyInfo' + '.csv'
        try:
            starttime = time.time()
            #交易所代码 ，SSE上交所 SZSE深交所
            df_SZSE = self.pro.stock_company(exchange='SZSE', fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,\
                                        province,city,introduction,website,email,office,employees,main_business,business_scope')
            df_SSE = self.pro.stock_company(exchange='SSE', fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,\
                                                    province,city,introduction,website,email,office,employees,main_business,business_scope')
            df = pd.concat([df_SSE,df_SZSE],axis=0)
            endtime = time.time()
            try:
                starttime = time.time()
                df.to_csv(filename, sep=',', header=True, index=False,encoding = 'utf-8-sig')
                endtime = time.time()
                print("Write data to csv spend time = ",endtime-starttime)
            except Exception as e:
                print ( self.getCurrentTime(),": SQL Exception :%s" % (e) )

        except Exception as e:
            print (self.getCurrentTime(),":get company info data from tushare Exception :%s" % (e) )

        print(self.getCurrentTime(),": Download company info Has Finished .")

def main():
    stockManager=tushareStock()
    stockManager.UpdateHisDataCompanyInfo()


if __name__ == "__main__":
    main()
