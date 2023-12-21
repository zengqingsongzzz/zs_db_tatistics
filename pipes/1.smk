from snakemake.utils import min_version
import os

min_version("7.32.4")

The_file_of_KO_number = config.get("The_file_of_KO_number", "")
#METHOD_DIR2 = config.get
DIAMOND_QUERY_FILE=config.get("DIAMOND_QUERY_FILE",'')
DIAMOND_THREADS=config.get("DIAMOND_THREADS")###?
Abundance_table=config.get("Abundance_table",'')


uni_ids = []

for line in open(The_file_of_KO_number,'r'):
    lines=line.strip('\n')
    lines=lines.strip("\"")
    uni_ids.append(lines)
print(uni_ids)







rule all:
    input:
        expand("result_files/2.uinprot/{sample}", sample=uni_ids),
        expand("result_files/1.getuinprotid/{sample}", sample=uni_ids),
        "result_files/2.uinprot/new_rmdup.dmnd",
	    "result_files/4.diamond/blastout_db",
        "result_files/4.diamond/1blastout_db",
        "result_files/4.diamond/2blastout_db",
        "result_files/4.diamond/3blastout_db",
        "result_files/4.diamond/4blastout_db"

## 1st step: make database-Obtain the uniprot code corresponding to the kegg number
rule get_uniprotid:
    input:
        a = expand("{dir}", dir=The_file_of_KO_number)
       
    #threads:
    #    SAMPLE_THREADS
    output:
        expand("result_files/1.getuinprotid/{sample}", sample=uni_ids)
        

    params:
        workdir = "result_files/1.getuinprotid/"



    shell:
        "python scripts/get_uniprotid.py -i {input.a} -o {params.workdir} "
    #run:
        #shell("")


## 2st step: make database-Obtaining protein sequences through the uniport number
file_list = os.listdir('result_files/2.uinprot')

if len(file_list) == 0:
    rule uniprot:
        input:
            expand("result_files/1.getuinprotid/{sample}", sample=uni_ids)
        output:
           expand("result_files/2.uinprot/{sample}", sample=uni_ids)
        params:
            workdir = "result_files/1.getuinprotid"
            #workdir2 = "result_files/2.uinprot"

        shell:
            """
            path={params.workdir}
            files=$(ls $path)
            for filename in $files
            do 
                echo 'python scripts/uniprot.py -i result_files/1.getuinprotid/'$filename' -o result_files/2.uinprot/'$filename' '>> result_files/2_uniprot.sh
            done
            bash result_files/2_uniprot.sh
    
        
            """
else:
    pass




## 3st step: make database-Obtaining protein sequences through the uniport number
rule rmdup:
    input:
        expand("result_files/2.uinprot/{sample}", sample=uni_ids)
    output:
        "result_files/2.uinprot/new_rmdup.dmnd"

    params:
        workdir = "result_files/1.getuinprotid"
        #workdir2 = "2.uinprot"


    shell:
        """
        path={params.workdir}
        files=$(ls $path)
        for filename in $files
        do 
            echo ' seqkit rmdup -s -i result_files/2.uinprot/'$filename' -o result_files/2.uinprot/'$filename'.rmdup '>> result_files/2.uinprot/rmdup1.sh
        done
        bash result_files/2.uinprot/rmdup1.sh  >result_files/2.uinprot/rmdup_log 2>&1 
        cat result_files/2.uinprot/*.rmdup > result_files/2.uinprot/new.rmdup
        grep -v 'ERROR:' result_files/2.uinprot/new.rmdup >result_files/2.uinprot/new.rmdup_grep_dup_error
        diamond makedb --in result_files/2.uinprot/new.rmdup_grep_dup_error -d result_files/2.uinprot/new_rmdup
        
        """
## 4st step: make database-Diamond and data filtering
rule data_filtering:
    input:
        "result_files/2.uinprot/new_rmdup.dmnd"
    output:
        "result_files/4.diamond/blastout_db",
        "result_files/4.diamond/1blastout_db",
        "result_files/4.diamond/2blastout_db",
        "result_files/4.diamond/3blastout_db",
        "result_files/4.diamond/4blastout_db"
   
	
    shell:
        """
        diamond blastp --db {input} --query {DIAMOND_QUERY_FILE} -p {DIAMOND_THREADS}  -o result_files/4.diamond/blastout_db --sensitive -e 1e-5  >result_files/4.diamond/diamond_log 2>&1

        python scripts/1_diamondjieguochuli.py result_files/4.diamond/blastout_db result_files/4.diamond/1blastout_db
        python scripts/2_diamondselsct.py result_files/4.diamond/1blastout_db result_files/4.diamond/2blastout_db
        python scripts/3_deletduplicate.py result_files/4.diamond/2blastout_db result_files/4.diamond/3blastout_db 
        python scripts/4_merge.py {Abundance_table} result_files/4.diamond/3blastout_db result_files/4.diamond/4blastout_db
        """

