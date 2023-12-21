import sys
import re
import pandas as pd
with open(sys.argv[2],"a") as out:





     into= pd.read_csv(sys.argv[1],sep=',')

     into=into.drop_duplicates(subset=['Gene_ID'],keep='first',inplace=False )
     into.to_csv(out,index=False)
