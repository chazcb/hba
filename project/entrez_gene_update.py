import gzip
import os
import model
from urllib import urlretrieve
from datetime import date, datetime

def read_human_gene_info(ftp_loc):

    gene_info_filename = "Homo_sapiens_gene_info.gz" 

    # retrieve file from ncbi ftp site, then write out a file into the local file directory
    urlretrieve(ftp_loc, gene_info_filename)

    gene_info = gzip.open(gene_info_filename)

    os.remove(gene_info_filename)

    return(gene_info)

def append_gene_table(db_session, gene_info, ftp_loc):

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

    column_name = "RowID\tGeneID\tSymbol\tSynonyms\tDescription\n"
    output_file.write(column_name)

    # write each row into db and output file
    # get existing max ids, set to 0 if table is empty
    max_gene_id = model.get_attr_max(db_session, model.Gene.id, 0)
    max_version_id = model.get_attr_max(db_session, model.Version.id, 0)
    max_gene_version_id = model.get_attr_max(db_session, model.Gene_version.id, 0)

    for line in gene_info:
        max_gene_id += 1
        max_gene_version_id += 1
        item = line.rstrip().split()
        # write to db
        gene = model.Gene(id = max_gene_id, 
                    entrez_gene_id = item[geneid_index],
                    entrez_gene_symbol = item[symbol_index],
                    entrez_gene_synonym = item[synonym_index],
                    entrez_gene_desc = item[desc_index]
                    )
        gene_version = model.Gene_version(id = max_gene_version_id,
                    gene_id = max_gene_id,
                    version_id = max_version_id+1
                    )
        db_session.add(gene)
        db_session.add(gene_version)
        # write to file
        datarow = ("%s\t%s\t%s\t%s\t%s\n") % (max_gene_id, 
            item[geneid_index], item[symbol_index], item[synonym_index], item[desc_index])
        output_file.write(datarow)

    version = model.Version(id = max_version_id+1, url = ftp_loc, timestamp = datetime.utcnow())
    db_session.add(version)

    db_session.commit()

    output_file.close()
    gene_info.close()

    print "Successfully created %s" % output_filename

def main():

    ftp_loc = "ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz"
    gene_info = read_human_gene_info(ftp_loc)
    append_gene_table(model.db_session, gene_info, ftp_loc)

if __name__ == "__main__":
    main()