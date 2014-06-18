# read every line, split by space
# uses the get function to see if the key already exists
# if the key exists, up the counter by one
# if the key doesn't yet exist, create it and increment by one
# for each key, print its value i.e. for key, value in dictionary_name,
# print key, value

def main():
    # open the text file
    text = open("twain.txt")
    word_list = [] # this will contain all of the words in twain.txt
    count_list = [] # this will contain a list of integers for the wordcounts
    word_dict = {} # this will contain key-value pairs representing asdffff
    wordcount_dict = {} # this will contain key-value pairs representing adfff

    # read in twain.txt 
    line = text.read()
    cleaned_line = "" # initialize empty string variable for cleaned-up text
        
    # go through each character in the line and do the following
    for char in line:
        # if the character has an ascii value in this range, it's a letter
        if ord(str(char)) >= 97 and ord(str(char)) <= 122:
            pass
        # if its ascii value is outside 97-122, it's not a letter
        else:
            char = " " # so we convert it to a space
        cleaned_line += char # put the resulting char back in the cleaned-up line
    # split the line up by spaces and add each segment to word_list
    word_list += cleaned_line.split(" ")

    # go through each word in the word list and
    for word in word_list:
        if word in word_dict:
            word_dict[word] += 1 # if the word is already a key, increment value by 1
        else:
            word_dict[word] = 1 # if the word isn't a key yet, create it and assign value of 1

    # go through each key/value pair in the word dictionary
    for key, value in word_dict.iteritems():
        # if the value (the count) is already in the wordcount dictionary
        if value in wordcount_dict.keys():
            # append the key (the word) to the value, which is a list of the words that appear key times
            wordcount_dict[value].append(key)
        else:
            # otherwise, assign a new key-value pair, and start the word list (the value)
            wordcount_dict[value] = [key]

    # go through each key/value pair in the wordcount dictionary
    for key, value in wordcount_dict.iteritems():
        value.sort() # alphabetize value, which is a list of words
        count_list.append(key) # appending the count (a number) to the count list, because it would be inefficient to go in sequence

    count_list.sort() # put the count_list (integers) in ascending order
    count_list.reverse() # put the count_list in descending order, per the extra credit

    # go through each count in the count_list
    for count in count_list:
        # in turn, go through each word in the wordcount dictionary
        for word in wordcount_dict[count]:
            # print the count, followed by the word in alphabetical order
            print count, word

if __name__ == "__main__":
    main()