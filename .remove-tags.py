# Takes poems mined by sopaHarmosa.py and extracts the proper poem text.
# The original poems are unaltered, the new text goes in the .temp/ folder

# Blair bdrum047@uottawa.ca

import os, sys, re

fix = re.compile('(?<=\n)(\n)?[^a-zA-Z\n]+(\n)?(?=\n)')

inpath  = sys.argv[1] + '/'                                   # input folder
outpath = os.getcwd() + "/.temp/"                             # folder for temporary files
f = open('.PoemsList.txt' , 'w')                              # Poem Index

for file in os.listdir(inpath):                               # iterate through every txt file in input folder
    if file.endswith(".txt"):
        f.write(outpath + file + '\n')                        # Add poem to index
        read  = open(os.path.join(inpath,  file), 'r')        # Open Input
        write = open(os.path.join(outpath, file), 'w')        # Open Output
        
        # NOT TESTED YET
        text = fix.sub('\n' , read.read())
        # Write parsed text
        write.write(text.split('text :')[1].split('\n\n\n\n')[0])  
        write.close()                                         # Close open file x2
        read.close()

f.close()
