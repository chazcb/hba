import gzip
from urllib import urlretrieve
from urllib2 import urlopen
from datetime import date

def read_human_gene_info_urllib():
# This writes out a file into the local file directory

    timestamp = date.today().isoformat()

    gene_info_filename = "Homo_sapiens_gene_info.gz" 
    output_filename = "gene_id_sym_desc.txt"

    urlretrieve("ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz",
        gene_info_filename)

    gene_info = gzip.open(gene_info_filename)
    output_file = open(output_filename, 'w')
    # creates file if does not exist, overwrite existing

    # read in first line to get header
    header = gene_info.readline()
    header.rstrip()
    header_list = header.split()
    # field names in header starts after first element ("Format:")
    geneid_index = header_list.index("GeneID")-1
    symbol_index = header_list.index("Symbol")-1
    desc_index = header_list.index("description")-1

    column_name = "RowID, GeneID, Symbol, Description, Version"
    output_file.write(column_name)

    # write each row into output file
    i = 1
    for line in gene_info:
        row = line.rstrip()
        item = row.split()
        datarow = ("%s, %s, %s, %s, %s") % (i, item[geneid_index], item[symbol_index], item[desc_index], timestamp)
        output_file.write(datarow)

    output_file.close()
    gene_info.close()

    print "Successfully created %s" % output_filename

def read_human_gene_info_urllib2():
# This avoids writing out a file in the local file directory
    info_file = urlopen("ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz")

    output_file = gzip.info_file

def main():

    read_human_gene_info_urllib()

if __name__ == "__main__":
    main()
