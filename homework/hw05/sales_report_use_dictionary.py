"""
sales_report.py - Generates sales report showing the total number
                  of melons each sales person sold.

"""
def create_sales_report(filename):
    f = open(filename)
    sales_tally = {}
    for line in f:
        line = line.rstrip()
        entries = line.split(",")
        salesperson = entries[0]
        melons = int(entries[2])
        if salesperson in sales_tally:
            sales_tally[salesperson] += melons
        else:
            sales_tally[salesperson] = melons
    return sales_tally

def print_report(sales_tally):
    for salesperson in sales_tally:
        print "%s sold %d melons" % (salesperson, sales_tally[salesperson])

def main():

    sales_tally = create_sales_report("sales_report.csv")
    print_report(sales_tally)

if __name__ == "__main__":
    main()