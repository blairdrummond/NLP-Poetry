# TODO: everything

import os, re

regex = re.compile('([^ \)]+\)|-[^ \)]*)')

directory = 'Reference-Data/'

for file in os.listdir(directory):
    if file.endswith(".mrg"):
        text  = open(os.path.join(directory, file), 'r').read()
        write = open(os.path.join(directory, file[:-3]+"txt"), 'w')
        text  = regex.sub('',text)
        write.write(text)
        write.close()
