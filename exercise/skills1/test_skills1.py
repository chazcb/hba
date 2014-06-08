import unittest

from skills1 import *

class Test_Skills_1(unittest.TestCase):

    def setUp(self):
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
                       'Sep', 'Oct', 'Nov', 'Dec']
        self.days = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        self.notes = ['Do', 'Re', 'Mi', 'Fa', 'So', 'La', 'Ti', 'Do']
        self.multiples = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27]
        self.mix = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun', 0, 3, 6, 
                        9, 12, 15, 18, 21, 24, 27]

# Write a function that takes a list and returns a new list with only the odd numbers.

    def test_all_odd(self):
        self.assertEqual(all_odd(self.months), [])
        self.assertEqual(all_odd(self.notes), [])
        self.assertEqual(all_odd(self.multiples), [3, 9, 15, 21, 27])
        self.assertEqual(all_odd(self.mix), [3, 9, 15, 21, 27])

# Write a function that takes a list and returns a new list with only the even numbers.

    def test_all_even(self):
        self.assertEqual(all_even(self.months), [])
        self.assertEqual(all_even(self.notes), [])
        self.assertEqual(all_even(self.multiples), [0, 6, 12, 18, 24])
        self.assertEqual(all_even(self.mix), [0, 6, 12, 18, 24])

# Write a function that takes a list of strings and a new list with all strings of length 4 or greater.

    def test_long_words(self):
        self.assertEqual(long_words(self.months), [])
        self.assertEqual(long_words(self.days), ['Tues','Thur'])
        self.assertEqual(long_words(self.notes), [])
        self.assertEqual(long_words(self.multiples), [])
        self.assertEqual(long_words(self.mix), ['Tues','Thur'])

# Write a function that finds the smallest element in a list of integers and returns it.

    def test_smallest(self):
        self.assertEqual(smallest(self.months), None)
        self.assertEqual(smallest(self.days), None)
        self.assertEqual(smallest(self.notes), None)
        self.assertEqual(smallest(self.multiples), 0)

# Write a function that finds the largest element in a list of integers and returns it.

    def test_largest(self):
        self.assertEqual(largest(self.months), None)
        self.assertEqual(largest(self.days), None)
        self.assertEqual(largest(self.notes), None)
        self.assertEqual(largest(self.multiples), 27)


# Write a function that takes a list of numbers and returns a new list of all those numbers divided by two.

    def test_halvesies(self):
        self.assertEqual(halvesies(self.months), [])
        self.assertEqual(halvesies(self.days), [])
        self.assertEqual(halvesies(self.notes), [])
        self.assertEqual(halvesies(self.multiples), [0.0, 1.5, 3.0, 
            4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5])

# Write a function that takes a list of words and returns a list of all the lengths of those words.

    def test_word_lengths(self):
        self.assertEqual(word_lengths(self.months), [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])
        self.assertEqual(word_lengths(self.days), [3, 4, 3, 4, 3, 3, 3])
        self.assertEqual(word_lengths(self.notes), [2, 2, 2, 2, 2, 2, 2, 2])
        self.assertEqual(word_lengths(self.multiples), [])

# Write a function (using iteration) that sums all the numbers in a list.

    def test_sum_numbers(self):
        self.assertEqual(sum_numbers(self.months), None)
        self.assertEqual(sum_numbers(self.days), None)
        self.assertEqual(sum_numbers(self.notes), None)
        self.assertEqual(sum_numbers(self.multiples), 135)
        self.assertEqual(sum_numbers(self.mix), 135)
 
# Write a function that multiplies all the numbers in a list together.

    def test_mult_numbers(self):
        self.assertEqual(mult_numbers(self.months), None)
        self.assertEqual(mult_numbers(self.days), None)
        self.assertEqual(mult_numbers(self.notes), None)
        self.assertEqual(mult_numbers(self.multiples), 0)
        self.assertEqual(mult_numbers(self.mix), 0)

# Write a function that joins all the strings in a list together (without using the join method) and returns a single string.

    def test_join_strings(self):
        self.assertEqual(join_strings(self.months), 'JanFebMarAprMayJunJulAugSepOctNovDec')
        self.assertEqual(join_strings(self.days), 'MonTuesWedThurFriSatSun')
        self.assertEqual(join_strings(self.notes), 'DoReMiFaSoLaTiDo')
        self.assertEqual(join_strings(self.multiples), None)
        self.assertEqual(join_strings(self.mix), 'MonTuesWedThurFriSatSun')

# Write a function that takes a list of integers and returns the average (without using the avg method)

    def test_average(self):
        self.assertEqual(average(self.months), None)
        self.assertEqual(average(self.days), None)
        self.assertEqual(average(self.notes), None)
        self.assertEqual(average(self.multiples), 13.5)
        self.assertEqual(average(self.mix), 13.5)

if __name__ == '__main__':
    unittest.main()