import sqlite3
import csv

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("melon.db")
    DB = CONN.cursor() # mechanism to interact with the database, to execute queries (similar to a file handle)

def initialize_customers_table():
    query = "TRUNCATE customers"
    DB.execute(query) 
    CONN.commit()

def customers_table_append(data_dict):

    # check: if customer_id exist, skip; else append
    query = "SELECT * FROM customers WHERE customer_id = ?"
    DB.execute(query, (int(data_dict['customer_id']),))
    customer_exists = DB.fetchall()

    if customer_exists: 
        return 0
    else: #insert new row
        fieldnames = []
        fieldvalues = []

        for key, value in data_dict.iteritems():
            fieldnames.append(key)
            fieldvalues.append(value)
 
        num_fields = '?'
        for i in range(0, len(fieldvalues)-1):
            num_fields += ',?'

        query = "INSERT into customers (%s) values (%s)" % (','.join(fieldnames), num_fields)
        DB.execute(query, (fieldvalues)) 
        CONN.commit()
        return 1 #1 record added
    
def read_customers_csv(filename):

    f = open(filename)

    reader = csv.reader(f)  # call reader function to parse and remove \n
    header_list = reader.next()  # read in first line to get header

    count = 0 # counter to track rows added

    for row in reader:
        row = [field.strip() for field in row if field]
        data_dict = dict(zip(header_list,row))
        count += customers_table_append(data_dict)

    print "Successfully added %d rows" % count

def main():
    connect_to_db()

    read_customers_csv("customers.csv")

    CONN.close()

if __name__ == "__main__":
    main()