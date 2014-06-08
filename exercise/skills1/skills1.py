# Write a function that takes a list and returns a new list with only the odd numbers.
def all_odd(some_list):
    output = []
    # no_num = True
    # no_odd_num = True
    for i in some_list:
    	if type(i) == int:
	    	if (i % 2 == 1):
	    		output.append(i)
	#     		no_odd_num = False
	#     	no_num = False
	# if no_odd_num:
	# 	print ("There are no odd numbers in your list")
	# elif no_num:
	# 	print ("There are no numbers in your list")
    return output

# Write a function that takes a list and returns a new list with only the even numbers.
def all_even(some_list):	
    output = []
    # no_num = True
    # no_even_num = True
    for i in some_list:
    	if type(i) == int:
	    	if (i % 2 == 0):
	    		output.append(i)
	#     		no_even_num = False
	#     	no_num = False
	# if no_even_num:
	# 	print ("There are no even numbers in your list")
	# elif no_num:
	# 	print ("There are no numbers in your list")
    return output

# Write a function that takes a list of strings and a new list with all strings of length 4 or greater.
def long_words(word_list):
    print word_list
    no_str = True	
    no_long_str = True
    output = []
    for i in word_list:
    	if type(i) == str:
    		no_str = False
    		if len(i) >= 4:
	    		output.append(i)
	    		no_long_str = False
	    		print i, output
	if no_str:
		print ("There are no strings in your list")
		return []
	elif no_long_str:
		print ("There are no strings of length 4 or greater in your list")
		return []
    else: 
    	return output

# Write a function that finds the smallest element in a list of integers and returns it.
def smallest(some_list):
    output = []
    for i in some_list:
    	if type(i) == int:
	    	output.append(i)
	output.sort()
    if len(output) > 0:
    	return output[0]
    else:
    	return None

# Write a function that finds the largest element in a list of integers and returns it.
def largest(some_list):
    output = []
    for i in some_list:
    	if type(i) == int:
	    	output.append(i)
	output.sort()
    if len(output) > 0:
    	return output[-1]
    else:
    	return None

# Write a function that takes a list of numbers and returns a new list of all those numbers divided by two.
def halvesies(some_list):
    output = []
    for i in some_list:
    	if type(i) == int:
	    	output.append(float(i)/2)
    return output

# Write a function that takes a list of words and returns a list of all the lengths of those words.
def word_lengths(word_list):
    output = []
    for i in word_list:
    	if type(i) == str:
	    	output.append(len(i))
    return output

# Write a function (using iteration) that sums all the numbers in a list.
def sum_numbers(numbers):
    no_num = True
    num_sum = 0
    for i in numbers:
    	if type(i) == int:
    		num_sum += i
    		no_num = False
    if no_num:
    	return None
    	print ("There are no numbers in your list")
    else:
    	return num_sum

# Write a function that multiplies all the numbers in a list together.
def mult_numbers(numbers):
    no_num = True
    num_prod = 1
    for i in numbers:
    	if type(i) == int:
    		num_prod = i * num_prod
    		no_num = False
    if no_num:
    	return None
    	print ("There are no numbers in your list")
    else:
    	return num_prod

# Write a function that joins all the strings in a list together (without using the join method) and returns a single string.
def join_strings(string_list):
	no_str = True
	concat_str = ""
	for i in string_list:
		if type(i) == str:
			concat_str = concat_str + i
			no_str = False
	if no_str:
		return None
		print ("There are no strings in your list")    
	else:
		return concat_str

# Write a function that takes a list of integers and returns the average (without using the avg method)
def average(numbers):
    no_num = True
    num_list = []
    for i in numbers:
    	if type(i) == int:
			num_list.append(i)
			no_num = False
    if no_num:
    	return None
    	print ("There are no numbers in your list")
    else:
    	return float(sum_numbers(num_list))/len(num_list)