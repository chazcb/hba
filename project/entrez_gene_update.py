import gzip
from urllib import urlretrieve
from urllib2 import urlopen
from datetime import date

def read_human_gene_info_urllib():
# This writes out a file into the local file directory

    timestamp = date.today().isoformat()

    # filenames
    gene_info_filename = "Homo_sapiens_gene_info.gz" 
    output_filename = "gene_id_sym_desc.txt"

    # retrieve file from ncbi ftp site
    urlretrieve("ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz",
        gene_info_filename)

    # file handles
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
    synonym_index = header_list.index("Synonyms")-1
    desc_index = header_list.index("description")-1

    column_name = "RowID, GeneID, Symbol, Synonyms, Description, Version\n"
    output_file.write(column_name)

    # write each row into output file
    i = 1
    for line in gene_info:
        item = line.rstrip().split()
        datarow = ("%s, %s, %s, %s, %s, %s\n") % (i, item[geneid_index], item[symbol_index], item[synonym_index], item[desc_index], timestamp)
        output_file.write(datarow)
        i += 1

    output_file.close()
    gene_info.close()

    print "Successfully created %s" % output_filename

def read_human_gene_info_urllib2():
# urlopen avoids writing out a file in the local file directory
# gzip not working in this function
    info_file = urlopen("ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz")

    output_file = gzip.info_file

def main():

    read_human_gene_info_urllib()

if __name__ == "__main__":
    main()
