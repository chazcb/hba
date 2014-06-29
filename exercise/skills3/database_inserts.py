import sqlite3
import csv

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("melon.db")
    DB = CONN.cursor() # mechanism to interact with the database, to execute queries (similar to a file handle)

def initialize_customers_table(db_table):
    query = "DELETE FROM %s" % db_table
    DB.execute(query) 
    CONN.commit()

def table_append(data_dict, db_table, primary_key):

    # check: if customer_id exist, skip; else append
    query = "SELECT * FROM %s WHERE %s = ?" % (db_table, primary_key)
    DB.execute(query, (int(data_dict[primary_key]),))
    pk_exists = DB.fetchall()

    if pk_exists: 
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

        query = "INSERT into %s (%s) values (%s)" % (db_table, ','.join(fieldnames), num_fields)
        DB.execute(query, (fieldvalues)) 
        CONN.commit()
        return 1 #1 record added
    
def read_csv(filename, db_table, primary_key):

    f = open(filename)

    reader = csv.reader(f)  # call reader function to parse and remove \n
    header_list = reader.next()  # read in first line to get header

    count = 0 # counter to track rows added

    for row in reader:
        row = [field.strip() for field in row if field]
        data_dict = dict(zip(header_list,row))
        count += table_append(data_dict, db_table, primary_key)

    print "Successfully added %d rows to %s" % (count, db_table)

class Customer():
    def __init__(self, data=[]):
        self.customer_id = data
        self.first
        self.last
        self.email
        self.telephone
        self.called

def main():
    connect_to_db()

    # initialize_customers_table('customers')
    read_csv('customers.csv', 'customers', 'customer_id')
    # initialize_customers_table('orders')
    read_csv('orders.csv', 'orders', 'order_id')

    CONN.close()

if __name__ == "__main__":
    main()