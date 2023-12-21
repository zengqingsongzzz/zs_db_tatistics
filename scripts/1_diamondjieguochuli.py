import sys
import re

with open(sys.argv[1]) as into:
    with open(sys.argv[2],"a") as out:
        #uni_ids = []
        
        for line in into.readlines():
            
            into_array=line.split()
            #mydb=open(out,'a')
            c=str(into_array[0] +'\t'+into_array[1]+ '\t'+into_array[10] +'\t'+into_array[11]+'\t'+into_array[2]+'\n')

            out.write(c)
      
            #mydb.close()
            
            #s = re.findall('"TimeSpan":"([\d.]+)"', line)
            


