'''
Created on Mar 16, 2018

@author: Rose Reiner
'''
import re
user_input = " "


user_input = input("Enter a word or phrase to determine if it's a palindrome or not: ")

user_input_cleaned = user_input.lower().replace(" ","").replace("," ,"").replace(".", "").replace(";", "") #removing all the whitespace, ".", ";", "," in the string and turned all the cases into lower case
print(user_input_cleaned)


half_length = (len(user_input_cleaned)//2) #Splitting the length of the string in half to get half of the value
#print(half_length)

first_half = user_input_cleaned[0:half_length] #splicing the string to get the first part of the word
#print(first_half)

reverse_first_half = first_half[::-1] #reversing the word order of the first half of the string
#print(reverse_first_half)


""" Building up the regex"""
regex_string = "^(" + first_half + ")" + ".?" + "(" + reverse_first_half + ")$" #creating a string format of the regex
regex = regex_string
p = re.compile(regex)

match1 = p.match(user_input_cleaned) #matching the regex to the formatted version
match2= p.match(user_input) #matching the regex to the version the user inputed


""" Checking if the string matches the regex """

if match2:
    print(user_input, "is a palindrome")
else:
    print(user_input, "is not a palindrome")

if match1:
    print(user_input_cleaned, "is a palindrome if I ignore whitespace, punctuation, and capitalization")
else:
    print(user_input_cleaned, "is not a palindrome if I ignore whitespace, punctuation, and capitalization")







