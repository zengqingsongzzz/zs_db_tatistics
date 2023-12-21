import sys
import re
import pandas as pd

with open(sys.argv[3],"a") as out:





     into= pd.read_csv(sys.argv[1],sep=',')
    # into.rename(columns={'xielie':'Gene_ID'}, inplace=True)
     #into.loc['Row_sum'] = into.apply(lambda x: x.sum())
     #print(into)
     #into['Col_sum'] = into.apply(lambda x: x.sum(), axis=1)
     #print(into)
     into1= pd.read_csv(sys.argv[2],sep=',')
     into1.columns = ['Gene_ID','evlue','pro','core','iden']
     #print(into1)
     fina=pd.merge(into1,into,on='Gene_ID',how="inner")
     #fina.loc['Row_sum'] = into.apply(lambda x: x.sum())
     fina.to_csv(out,index=False)
