import os
from Main import makeDotToDot

for personpicture in os.listdir('testimages/people'):
    print ('Making dot to dot of: ' , str(personpicture))
    makeDotToDot('testimages/people/' + personpicture)
