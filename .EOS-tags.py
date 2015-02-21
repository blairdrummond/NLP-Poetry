# Add annotation to mark the end of a sentence in a parse tree.
# Applied AFTER .mark-breaks.py, it nests <EOS> inside of the line and stanza breaks.
# (This is useful for processing done in .count-breaks.py)

# Blair bdrum047@uottawa.ca

import os

directory = 'output/'

for file in os.listdir(directory):
    if file.endswith(".txt"):
        with open(os.path.join(directory, file), 'r') as read:
            text = read.read()
        write = open(os.path.join(directory, file), 'w')
        text = text.replace('<//> \n','<EOS> <//> \n')
        text = text.replace('</> \n' ,'<EOS> </> \n')
        text = text.replace(') \n'   ,') <EOS> \n')
        text = text[:-5] + '<EOS> <//> '
        write.write(text)
        write.close()
            
