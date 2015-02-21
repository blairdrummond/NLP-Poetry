# Takes the XML output from the stanford system and takes the relevent tree parses from it. 
# These parses are copied into a similarily named tree_{}.txt in the .trees/ folder.

# Blair bdrum047@uottawa.ca

import os, re

#pattern to extract 
pattern = re.compile(r'<parse>.*(?=</parse>)')

path = os.getcwd() + '/.trees/'

for file in os.listdir(path):
    if file.endswith(".xml"):
        write = open(os.path.join(path, 'tree_' + file[:-4] + '.txt' ), 'w')
        read = open(os.path.join(path,  file), 'r')
        for penn in pattern.findall(read.read()):
            write.write(penn[7:] + '\n')
        read.close()
        write.close()
