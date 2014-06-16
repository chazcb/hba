import unittest

from skills2 import *

class Test_Skills_2(unittest.TestCase):

    def setUp(self):
        self.string1 = "I do not like green eggs and ham. I do not like them."
        self.string2 = "Sir, is your excuse the student?  My lawyer is your professor."
        self.string3 = "professor restaurant your excuse students"
        self.list1 = [2, 5, 12, 6, 1, -5, 8, 5, 6, -2, 2, 27]
        self.list2 = [-5, 6, 4, 8, 15, 16, 23, 42, 2, 7]
        self.words = ["I", "do", "not", "like", "green", "eggs", "and", "ham", "I", "do", "not", "like", "them", "San", "I", "am"]
        self.words2 = ["to", "be", "or", "not", "to", "be"]

# """
# Write a function that takes a string and produces a dictionary with
# all distinct elements as the keys, and the number of each element as
# the value
# Bonus: do the same for a file (i.e. twain.txt)
# """

    def test_count_unique(self):
        self.assertEqual(count_unique(self.string1), {
            'I': 2,
            'do': 2,
            'not': 2,
            'like': 2,
            'and': 1,
            'green': 1,
            'eggs': 1,
            'ham.': 1,
            'them.': 1,
            })

# """
# Given two lists, (without using the keyword 'in' or the method 'index')
# return a list of all common items shared between both lists
# """
    def test_common_items(self):
        list1_list2_output = common_items(self.list1, self.list2)
        list1_list2_output.sort()
        self.assertEqual(list1_list2_output, [-5, 2, 6, 8])
        self.assertEqual(common_items(self.list2, self.words), [])

# """
# Given two lists, (without using the keyword 'in' or the method 'index')
# return a list of all common items shared between both lists. This time,
# use a dictionary as part of your solution.
# """

    def test_common_items2(self):
        list1_list2_output = common_items2(self.list1, self.list2)
        list1_list2_output.sort()
        self.assertEqual(list1_list2_output, [-5, 2, 6, 8])
        self.assertEqual(common_items(self.list2, self.words), [])

# """
# Given a list of numbers, return list of number pairs that sum to zero
# """
    def test_sum_zero(self):
        list1_output = sum_zero(self.list1)
        list1_output.sort()
        self.assertEqual(list1_output, [[-5, 5], [-2, 2], [2, -2], [5, -5]])
        self.assertEqual(sum_zero(self.list2), [])

# """
# Given a list of words, return a list of words with duplicates removed
# """

    def test_find_duplicates(self):
        words_output = find_duplicates(self.words)
        words_output.sort()
        self.assertEqual(words_output, ['I', 'San', 'am', 'and', 'do', 'eggs', 'green', 'ham', 'like', 'not', 'them'])
        words2_output = find_duplicates(self.words2)
        words2_output.sort()
        self.assertEqual(words2_output, ['be', 'not', 'or', 'to'])

# """
# Given a list of words, print the words in ascending order of length
# Bonus: do it on a file instead of the list provided
# Bonus: print the words in alphabetical order in ascending order of length
# """

    def test_word_length(self):
        self.assertEqual(word_length(self.words), ['I', 'am', 'do', 'San', 'and', 'ham', 'not', 'eggs', 'like', 'them', 'green'])

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
    def test_pirate_translator(self):
        self.assertEqual(pirate_translator(self.string3), 
            "foul blaggart galley yer arr swabbies")

if __name__ == '__main__':
    unittest.main()