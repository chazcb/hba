def main():

    from sys import argv
    script, filename = argv

    f = open(filename)
    content = f.read()
    total_count = len(content)
    print "The file you entered is %s and is %d long" % (filename, total_count)

    char_array = []
    count_array = []

    for char in content:
        if char in char_array:
            char_index = char_array.index(char)
            count_array[char_index] += 1
        else:
            char_array.append(char)
            array_len = len(char_array)
            count_array[array_len:array_len] = [1]

    # sorted_char_array = char_array
    # sorted_char_array.sort()

    # for i in sorted_char_array:
    #     orig_index = char_array.index(i)
    #     print "There are %d instances of %s" % (count_array[orig_index], i)

    for i in char_array:
        index = char_array.index(i)
        print "There are %d instances of %s" % (count_array[index], i)

if __name__ == "__main__":
    main()
