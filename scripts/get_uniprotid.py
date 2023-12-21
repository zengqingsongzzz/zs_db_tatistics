import re
from xml.dom.pulldom import parseString
import requests
from bs4 import BeautifulSoup
import pandas as pd
import UniprotScraper as us
import numpy as np
import sys
import argparse

def main():
    global args
    #file=sys.argv[1]+'/home/data/zs/new_ko_db/Organic_carbon/1'
    file=args.inputfile
    uni_ids = []
    for line in open(file,'r'):

        lines=line.strip('\n')
        lines=lines.strip("\"")
        uni_ids.append(lines)
    #uni_ids=np.delete(uni_ids , 0, axis=0)
    
    for ids in uni_ids:

        dizi='https://www.genome.jp/kegg-bin/uniprot_list?ko='+ids
        print(dizi)
        url = dizi

        response = requests.get(url)

        response.encoding='utf-8'

        html = response.text
        #print(html)
        soup = BeautifulSoup(html, 'html.parser')
        txt=soup.find_all('a')
        txt=str(txt)

        s = re.findall('\>[0-9a-zA-Z]*\<\/a\>', txt)
        s=str(s)
        s1=re.sub('\<\/a\>','\n',s)
        s1=str(s1)
        s2=re.sub('\'\, \'\>','',s1)
        s2=str(s2)
        s3=re.sub('\'\]','',s2)
        s3=str(s3)
        s4=re.sub('\[\'\>','',s3)

        #outaddress='/home/data/zs/new_ko_db/Organic_carbon/'+ids
        outaddress=args.outputfile+'/'+ids
        mydb=open(outaddress,'a')

        mydb.write(s4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="inputfile", help="Input file.", required=True)
    parser.add_argument("-o", dest="outputfile", help="Output file.", required=True)
    #parser.add_argument("--output_bed", dest="qualoutfile", help="Output BED file with uncalled regions.", required=True)
    # parser.add_argument("-g", "--gq", dest="gq", help="Genotype Quality threshold ", required=True, type=float)
    args = parser.parse_args()
    main()
