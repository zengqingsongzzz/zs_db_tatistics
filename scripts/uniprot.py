import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
import UniprotScraper as us
import numpy as np
import sys
import argparse

def main():
    global args
    file=args.inputfile

    uni_ids1 = []
    #all_seq = []


    for line in open(file,'r'):
        lines=line.strip('\n')
        lines=lines.strip("\"")
        #print(lines)
        uni_ids1.append(lines)
    uni_ids1=np.delete(uni_ids1 , 0, axis=0)

    uni_ids1=np.delete(uni_ids1 , 0, axis=0)

    
#print(uni_ids1)

    for ids in uni_ids1:
    #all_seq.append(us.get_sequence(ids))
        seq=us.get_sequence(ids)
        #print(us.get_sequence(ids))
        c=str('>'+ids +'\n')
        a=str(seq+'\n')
        file1=args.outputfile
        mydb=open(file1,'a')
        mydb.write(c)
        mydb.write(a)
        mydb.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="inputfile", help="Input file.", required=True)
    parser.add_argument("-o", dest="outputfile", help="Output file.", required=True)
    #parser.add_argument("--output_bed", dest="qualoutfile", help="Output BED file with uncalled regions.", required=True)
    # parser.add_argument("-g", "--gq", dest="gq", help="Genotype Quality threshold ", required=True, type=float)
    args = parser.parse_args()
    main()
