'''
Created on Mar 16, 2018

@author: Rose Reiner
'''
import re
user_input = " "


user_input = input("Enter a word or phrase to determine if it's a palindrome or not: ")


half_length = (len(user_input)//2) #Splitting the length of the string in half to get half of the value
#print(half_length)

first_half = user_input[0:half_length] #splicing the string to get the first part of the word
#print(first_half)

reverse_first_half = first_half[::-1] #reversing the word order of the first half of the string
#print(reverse_first_half)


""" Building up the regex"""
string2 = "^(" + first_half + ")" + ".?" + "(" + reverse_first_half + ")$" #creating a string format of the regex
regex = string2
p = re.compile(regex)
match = p.match(user_input)

""" Checking if the string matches the regex """
if match:
    print(user_input, "is a palindrome")
else:
    print(user_input, "is not a palindrome")







