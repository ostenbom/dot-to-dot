import os
from Main import makeDotToDot

for i, personpicture in enumerate(os.listdir('testimages/people')):
    print (str(i) + ': ' + str(personpicture) + ' to be made')

startFrom = int(input("Image To Start From: "))
for i, personpicture in enumerate(os.listdir('testimages/people')):
    if i >= startFrom:
        print ('Making dot to dot of: ' , str(personpicture))
        makeDotToDot('testimages/people/' + personpicture)
