def print_under_paid(input_line):
    line = input_line.rstrip()
    [rid, name, melons, paid] = line.split(',')
    
    melon_cost = 1.00
    expected = int(melons) * melon_cost

    if expected != paid:
        print "%s paid %.2f, expected %.2f" % (name, float(paid), float(expected))

def main():

    myfile = open("customer_orders.csv")

    for input_line in myfile:
        print_under_paid(input_line)

if __name__ == "__main__":
    main()