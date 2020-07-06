# -*- coding:utf-8 -*-
import tushare as ts
import datetime,time
import pandas as pd
import json

class tushareStock():
    def __init__(self):
        print(ts.__version__)
        self.pro = ts.pro_api('56abe36c3119312257bb476314729f44f05457e604b54d09c4a09aa7')
        # self.engine = create_engine('mysql+mysqldb://root:root@127.0.0.1/history?charset=utf8')
        self.sleepTime = 5

    def getCurrentTime(self):
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))
    def get_top10_holders_2file(self,company):
        starttime = time.time()
        # 交易所代码 ，SSE上交所 SZSE深交所
        df = self.pro.query('top10_holders', ts_code=company[0], start_date='20200101', end_date='20200627')
        endtime = time.time()
        try:
            filename = 'D:\\stock\\history\\top10_holders\\' + company[0] + 'top10_holders' + '.csv'
            starttime = time.time()
            df.to_csv(filename, sep=',', header=True, index=False, encoding='utf-8-sig')
            endtime = time.time()
            print("Write data to csv spend time = ", endtime - starttime)
        except Exception as e:
            print(self.getCurrentTime(), ": SQL Exception :%s" % (e))

    def get_top10_holders(self):
        with open(r'./sortted_stock.json', 'r', encoding='utf8')as fp:
            json_data = json.load(fp)

        for company in json_data[0:100]:
            try:
                self.get_top10_holders_2file(company)

            except Exception as e:
                if "您每分钟最多访问该接口10次" in str(e):
                    print(self.getCurrentTime(), ":get top10 holders data from tushare Exception :%s" % (e))
                    time.sleep(60)
                    self.get_top10_holders_2file(company)

        print(self.getCurrentTime(),": Download company info Has Finished .")

def main():
    stockManager=tushareStock()
    stockManager.get_top10_holders()


if __name__ == "__main__":
    main()
