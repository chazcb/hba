def main():
  
    def report(filename):
        my_file = open(filename)
        for line in my_file:
    	    line = line.rstrip()
            words = line.split(',')

            melon = words[0]
            count = words[1]
            amount = words[2]
            
            message = "Delivered %s %ss for a total of: $%s" % (count, melon, amount)
            print str.upper(message)
        my_file.close()
        print "\n",

    # Day 1
    print "Day 1"
    report("um-deliveries-20140519.csv")

    # Day 2
    print "Day 2"
    report("um-deliveries-20140520.csv")

    # Day 3
    print "Day 3"
    report("um-deliveries-20140521.csv")

if __name__ == "__main__":
    main()