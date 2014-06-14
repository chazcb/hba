string1 = "I do not like green eggs and ham."
list1 = [2, 5, 12, 6, 1, -5, 8, 5, 6, -2, 2, 27]
list2 = [-5, 6, 4, 8, 15, 16, 23, 42, 2, 7]
words = ["I", "do", "not", "like", "green", "eggs", "and", "ham", "I", "do", "not", "like", "them", "San", "I", "am"]

# """
# Write a function that takes a string and produces a dictionary with
# all distinct elements as the keys, and the number of each element as
# the value
# Bonus: do the same for a file (i.e. twain.txt)
# """
def count_unique(string):

    string_el = string.split()
    word_dict = {}

    for item in string_el:
        word_dict[item] = word_dict.get(item, 0) + 1

    return word_dict

# """
# Given two lists, (without using the keyword 'in' or the method 'index')
# return a list of all common items shared between both lists
# """
def common_items(list1, list2):

    common = {}

    for index1 in range(0,len(list1)):
        for index2 in range(0,len(list2)):
            if list1[index1] == list2[index2]:
                common[list1[index1]] = common.get(list1[index1],0) + 1

    keys = common.keys()

    return keys
# """
# Given two lists, (without using the keyword 'in' or the method 'index')
# return a list of all common items shared between both lists. This time,
# use a dictionary as part of your solution.
# """
def common_items2(list1, list2):

    list1_dict = {}
    common = []

    for index in range(0,len(list1)):
        key = list1[index]
        list1_dict[key] = list1_dict.get(key, 0) + 1

    for index in range(0,len(list2)):
        key = list2[index]
        if list1_dict.get(key, 0) > 0:
            common.append(key)

    return common

# """
# Given a list of numbers, return list of number pairs that sum to zero
# """
def sum_zero(list1):
    
    match = []

    for index in range(0,len(list1)):
        for index2 in range(1,len(list1)):
            if list1[index] + list1[index2] == 0:
                match.append((list1[index],list1[index2]))

    return match

# """
# Given a list of words, return a list of words with duplicates removed
# """
def find_duplicates(words):
    
    word_dict = {}

    for item in words:
        word_dict[item] = word_dict.get(item, 0) + 1

    deduped = word_dict.keys()

    return deduped

# """
# Given a list of words, print the words in ascending order of length
# Bonus: do it on a file instead of the list provided
# Bonus: print the words in alphabetical order in ascending order of length
# """
def word_length(words):
    
word_dict = {}
key_list = []
value_list = []
sorted_value_list = []

for item in words:
    word_dict[item] = len(item)

value_list = word_dict.values()

sorted_value_list = find_duplicates(value_list)
sorted_value_list.sort()

output = []

for num in sorted_value_list:
    for key, value in word_dict.iteritems():
        if value == num:
            output.append(key)

    return output

# """
# Here's a table of English to Pirate translations
# English     Pirate

# sir         matey
# hotel       fleabag inn
# student     swabbie
# boy         matey
# madam       proud beauty
# professor   foul blaggart
# restaurant  galley
# your        yer
# excuse      arr
# students    swabbies
# are         be
# lawyer      foul blaggart
# the         th'
# restroom    head
# my          me
# hello       avast
# is          be
# man         matey

# Write a program that asks the user to type in a sentence and then
# print the sentece translated to pirate.
# """
def pirate_translator(string):

    pirate_dict = {
        'sir': 'matey',
        'hotel': 'fleabag inn',
        'student': 'swabbie',
        'boy': 'matey',
        'madam': 'proud beauty',
        'professor': 'foul blaggart',
        'restaurant': 'galley',
        'your': 'yer',
        'excuse': 'arr',
        'students': 'swabbies',
        'are': 'be',
        'lawyer': 'foul blaggart',
        'the': "th'",
        'restroom': 'head',
        'my': 'me',
        'hello': 'avast',
        'is': 'be',
        'man': 'matey',
    }

    pirate_string = ""
    pirate_list = []

    for char in string:
        if (ord(str(char)) >=65 and ord(str(char)) <= 90) or (ord(str(char)) >=97 and ord(str(char)) <= 122):
            pass
        else:
            char = " "

    string.lower()
    string_list = string.split()

    for word in string_list:
        pirate_list.append(pirate_dict.get(word))

    pirate_string = " ".join(pirate_list)

    return pirate_string
