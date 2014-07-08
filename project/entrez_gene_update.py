import gzip
import os
import model
from urllib import urlretrieve
from datetime import date, datetime
from sqlalchemy import func

def read_human_gene_info():

    gene_info_filename = "Homo_sapiens_gene_info.gz" 

    # retrieve file from ncbi ftp site, then write out a file into the local file directory
    urlretrieve("ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz",
        gene_info_filename)

    gene_info = gzip.open(gene_info_filename)

    os.remove(gene_info_filename)

    return(gene_info)

def append_gene_table(db_session, gene_info):

    timestamp = date.today().isoformat()
    output_filename = timestamp + "_gene_id_sym_desc.txt"
    output_file = open(output_filename, 'w')  # creates file if does not exist, overwrite existing

    # read in first line to get header
    header = gene_info.readline()
    header_list = header.rstrip().split()
    # field names in header starts after first element ("Format:")
    geneid_index = header_list.index("GeneID")-1
    symbol_index = header_list.index("Symbol")-1
    synonym_index = header_list.index("Synonyms")-1
    desc_index = header_list.index("description")-1

    column_name = "RowID\tGeneID\tSymbol\tSynonyms\tDescription\tVersion\n"
    output_file.write(column_name)

    # write each row into db and output file

    if db_session.query(func.max(model.Gene.id)).one()[0]:
        i = db_session.query(func.max(model.Gene.id)).one()[0]
    else:
        i = 0

    for line in gene_info:
        i += 1
        item = line.rstrip().split()
        # write to db
        gene = model.Gene(id = i, 
                    entrez_gene_id = item[geneid_index],
                    entrez_gene_symbol = item[symbol_index],
                    entrez_gene_synonym = item[synonym_index],
                    entrez_gene_desc = item[desc_index], 
                    entrez_version = datetime.utcnow()
                    )
        db_session.add(gene)
        # write to file
        datarow = ("%s\t%s\t%s\t%s\t%s\t%s\n") % (i, 
            item[geneid_index], item[symbol_index], item[synonym_index], item[desc_index], timestamp)
        output_file.write(datarow)

    db_session.commit()

    output_file.close()
    gene_info.close()

    print "Successfully created %s" % output_filename

def main():

    gene_info = read_human_gene_info()
    append_gene_table(model.db_session, gene_info)

if __name__ == "__main__":
    main()
