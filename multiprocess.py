import pandas as pd
import os
from threading import Thread
import time



filelist = os.listdir("D:\stock\history")
for filename in filelist:
    stockcode = filename.split('.')[0]
    exec('stock_' + stockcode + '=' + '1')

def read_csv_data(csv_file,fname):
    stockcode = fname.split('.')[0]
    df = pd.read_csv(csv_file)
    exec('stock_' + stockcode + '=' + 'df')


def main():
    for root,_, files in os.walk("D:\stock\history"):
        for fname in files:
            csv_file = os.path.join(root, fname)
            t = Thread(target=read_csv_data, args=(csv_file,fname))
            t.start()




if __name__ == "__main__":
    main()
    time.sleep(4)
    print(eval('stock_' + '000001.head()'))