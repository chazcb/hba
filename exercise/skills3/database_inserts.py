import sqlite3
import csv

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor() # mechanism to interact with the database, to execute queries (similar to a file handle)

def initialize_customers_table():
	TRUNCATE 
	pass

def customers_table_append(row):
	# customer_id 
 #    first 
 #    last 
 #    email 
 #    telephone 
 #    called 
	# query = """INSERT into customers values(?,?,?,?,?,?)"""
 #    DB.execute(query, (first_name, last_name, github)) #create new row
 #    CONN.commit()
    pass
	
def read_customers_csv(filename):

	f = open(filename)

	reader = csv.reader(f)  # call reader function to parse and remove \n
	header_list = reader.next()  # read in first line to get header

	customer = {}

	print header_list
	for row in reader:
		row = [x.strip() for x in row if x]


		customers_table_append(row)

def main():
    connect_to_db()

    read_customers_csv("customers.csv")

    CONN.close()

if __name__ == "__main__":
    main()