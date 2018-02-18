
import re
quoted = re.compile('()')
file = open('madlib.txt', 'r') 

data=file.read()
listOfQuestions = re.findall('\((.*?)\)',data)

file = open('madlibInput.txt', 'w')
count = 0
for item in listOfQuestions:
    file.write("(Line:%d) Answer:  (%s)  Name: \n" % (count, item))
    count += 1
