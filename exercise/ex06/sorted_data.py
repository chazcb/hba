# Charanga:3
# Irma's Pampanga:5
# Bay Blend Coffee and Tea:3
# Giordano Bros:2

# open the file
# initialize an empty dictionary
# split up the lines of text by : and put line[0] as restaurant and line[1] as score
# create a list with just the keys (restaurant names) so that we can alphabetize it
# loop through the list, and print 'for each key (restaurant), the value (score) is whatever'

def main():
    print "hello"
    text = open("scores.txt")

    restaurant_names = []
    restaurant_scores = {}

    for line in text:
        line = line.rstrip()
        (restaurant, score) = line.split(':')
#        restaurant_names += line[0]
        restaurant_scores[restaurant] = score
        # print restaurant
        # print restaurant_names
        # print restaurant_scores

    restaurant_names = restaurant_scores.keys()
    restaurant_names.sort()

    for name in restaurant_names:
        print "The restaurant %s has a score of %r." % (name, int(restaurant_scores[name]))

if __name__ == "__main__":
    main()