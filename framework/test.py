

dict1 = {'banana' : 'yellow', 'apple' : 'red'}
dict2 = {'pear' : 'green', 'orange' : 'orange'}

for d1, d2 in zip(dict1.items(), dict2.items()):
    print(d1[0], d2)