#!/usr/bin/env python3

import pyperclip
import random
import readline

orig_list=input('Please paste capture IDs here and press RETURN: ')

while orig_list=="":
    orig_list=input('Please try again. ')

user_list=orig_list.split(',')

print('There are '+str(len(user_list))+' captures in this session.')
total=int(len(user_list))

number_chosen=input('How many captures would you like to review? ')
while int(number_chosen)>total:
    number_chosen=input('Number is greater than avaialble captures. Please choose a smaller number. ')
    
increment=int(round((total)/int(number_chosen)))

if (increment * int(number_chosen))>total:
    print('Number is being adjusted due to math.')

while (increment * int(number_chosen))>total:
    number_chosen=int(number_chosen)-1
    increment=int(round((total)/int(number_chosen)))  

yn=input('Would you like to include the last image for review? Y/N ').lower() 

x=0    # refers to the first object position within user_list 
c=0    # is a variable whose value is capped at number_chosen
results=[]

if increment==1:
    results=random.sample(user_list, int(number_chosen))
    
else:
    if increment%2!=0:
        while c<int(number_chosen):
            results.append(user_list[x])
            x=x+int(increment)
            c=int(len(results))

    if increment%2==0:
        while c<int(number_chosen):
            results.append(user_list[x])
            if (int(len(results)))%2!=0:
                x=(x+int(increment))+1
            if (int(len(results)))%2==0:
                x=(x+int(increment))-1
            c=int(len(results))
    
if yn==('y'):
         results.append(user_list[-1])

final_list=list(set(results))
final_list.sort(key=user_list.index)

joined_string = ",". join(final_list)
pyperclip.copy(joined_string)                      
print('Capture IDs have been copied to your clipboard.')

