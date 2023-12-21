import sys
import re
import pandas as pd

with open(sys.argv[2],"a") as out:


     into= pd.read_csv(sys.argv[1],sep='\t',header=None)
     into.columns = ['Gene_ID','pro','evlue','core','iden']
#df=pd.DataFrame(into,columns=['xielie','pro','core'])
#print(into)
     #into1=pd.read_csv(sys.argv[2],sep='\t')
     df_1 = into[['Gene_ID','core']].groupby(by='Gene_ID',as_index=False).max()
    # print(df_groupby)
     
     df_2 = pd.merge(df_1,into,on=['Gene_ID','core'],how='left')
     df_3 = df_2[['Gene_ID','evlue']].groupby(by='Gene_ID',as_index=False).min()
     df_merge = pd.merge(df_3,into,on=['Gene_ID','evlue'],how='left')
     #print(df_merge)
     df_merge.to_csv(out, index=False)

