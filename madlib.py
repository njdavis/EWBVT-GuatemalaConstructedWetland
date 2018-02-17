
import re
quoted = re.compile('()')
file = open('madlib.txt', 'r') 

data=file.read()

for value in quoted.findall(data):
    print(value)

#print(file.read())


