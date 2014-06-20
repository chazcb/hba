import sqlite3

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
	pass

def read_customers_csv(filename):
	f = open(filename)
	for row in f:
		row.rstrip()
		fields = row.split(",")
		print fields
	


def main():
    connect_to_db()

    read_customers_csv("customers.csv")

    CONN.close()

if __name__ == "__main__":
    main()