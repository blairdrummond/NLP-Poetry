# Takes poems mined by sopaHarmosa.py and extracts the proper poem text.
# The original poems are unaltered, the new text goes in the .temp/ folder

# Blair bdrum047@uottawa.ca

import os, sys, re

fix = re.compile('(?<=\n)[0-9IVX* ]+(?=\n)')

inpath  = sys.argv[1] + '/'                                   # input folder
outpath = os.getcwd() + "/.temp/"                             # folder for temporary files
f = open('.PoemsList.txt' , 'w')                              # Poem Index

for file in os.listdir(inpath):                               # iterate through every txt file in input folder
    if file.endswith(".txt"):
        f.write(outpath + file + '\n')                        # Add poem to index
        with open(os.path.join(inpath,  file), 'r') as fi:
            read = ''.join(fi.readlines()[9:])               # Open Input
        
        # NOT TESTED YET
        text = fix.sub('\n' , read)
        # Write parsed text
        with open(os.path.join(outpath, file), 'w') as write: # Write Output
            write.write(text)                                 

f.close()
