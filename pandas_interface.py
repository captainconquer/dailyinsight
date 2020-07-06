#https://blog.csdn.net/ch1209498273/article/details/81157495

import pandas as pd
data = pd.DataFrame({'A':[1,2,3],'B':[4,5,6],'C':[7,8,9]},index=["a","b","c"])
print(data)
print(data.loc["b","B"])
print(data.loc['b':'c','B':'C'])
print(data.iloc[1:3,1:3])
# print(data.ix[1, 1])
# print(data.ix["b", "B"])
