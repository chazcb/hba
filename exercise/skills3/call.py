"""
call.py - Telemarketing script that displays the next name 
          and phone number of a Customer to call.

          This script is used to drive promotions for 
          specific customers based on their order history.
          We only want to call customers that have placed
          an order of over 20 Watermelons.

"""

import sqlite3
from datetime import date
from random import randint

DB = None
CONN = None

# Class definition to store our customer data
class Customer(object):
    def __init__(self, id=None, first=None, last=None, telephone=None):
        self.customer_id = ''
        self.first = ''
        self.last = ''
        self.telephone = ''
        pass

    def __str__(self):
        output = " Name: %s, %s\n" % (self.last, self.first)
        output += "Phone: %s" % self.telephone

        return output

# Connect to the Database
def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect('melon.db')

    DB = CONN.cursor()


# Retrieve the next uncontacted customer record from the database.
# Return the data in a Customer class object.
#
# Remember: Our telemarketers should only be calling customers
#           who have placed orders of 20 melons or more.
def get_next_customer():

    next_customer = Customer()

    query = """ SELECT DISTINCT c.customer_id
                FROM customers c
                JOIN orders o
                    ON c.customer_id = o.customer_id
                WHERE (o.num_watermelons + o.num_othermelons) > 20
                AND c.called IS NULL
    """
    DB.execute(query, )
    call_list = DB.fetchall()
    next_id = randint(0, len(call_list))
    print "%d eligible customers" %len(call_list)
    next_cust_id = call_list[next_id][0]

    query = """ SELECT first, last, telephone, customer_id
                FROM customers
                WHERE customer_id = ?
    """
    DB.execute(query, (next_cust_id,))
    customer_info = DB.fetchone()
    next_customer.first = customer_info[0]
    next_customer.last = customer_info[1]
    next_customer.telephone = customer_info[2]
    next_customer.customer_id = customer_info[3]
    return next_customer

def display_next_to_call(customer):
    print "---------------------"
    print "Next Customer to call"
    print "---------------------\n"
    print customer
    print "\n"


# Update the "last called" column for the customer
#   in the database.
def update_customer_called(customer):

    today = date.today()

    query = """ UPDATE customers  
                SET called = ?
                WHERE customer_id = ?
    """
    DB.execute(query, (today, customer.customer_id))
    CONN.commit()

def main():
    connect_to_db()

    done = False

    while not done:
        customer = get_next_customer()
        display_next_to_call(customer)

        print "Mark this customer as called?"
        user_answer = raw_input('(y/n) > ')

        if user_answer.lower() == 'y':
            update_customer_called(customer)
        else:
            done = True

    CONN.close()

if __name__ == '__main__':
    main()