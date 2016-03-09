# Run the file in command line as...
# > python drawtree.py <poem number> <optional stanza number>
# make sure that it is in the right directory

# Blair bdrum047@uottawa.ca

import nltk.compat
import sys
import os
import random

from tkinter import IntVar, Menu, Tk

from nltk.util import in_idle
from nltk.tree import Tree
from nltk.draw.util import (CanvasFrame, CanvasWidget, BoxWidget,
                            TextWidget,  ParenWidget,  OvalWidget)
from nltk.draw.tree import *



# Windows? (not tested)
#directory = r'\output'

# Linux
directory = 'output/'

def grab_file(f):
    with open(os.path.join(directory, 'poem.'+ f + '.txt'), 'r') as fr:
        read  = fr.read().split('\n')  # Parse Tree of Poem
    end = read.index('')
    return read[:end]


def grab_stanza(f,s):
    with open(os.path.join(directory, 'poem.'+ f + '.txt'), 'r') as fr:
        read  = fr.read().split('\n')  # Parse Tree of Poem

    i    = 0
    line = 0
    while i < s:
        if i < s:
            i = i + read[line].count('<//>')
        line+=1

    if i > s:
        return [read[line]]

    i = line
    line+=1
    while -1 == read[line].find('<//>'):
        line+=1

    return read[i:line+1]


def test(parses):
    def fill(cw):
        cw['fill'] = '#%06d' % random.randint(0,999999)

    cf = CanvasFrame(width=550, height=450, closeenough=2)

    j = 10

    for parse in parses:
        t  = Tree.fromstring(parse)
        tc = TreeWidget(cf.canvas(), t, draggable=1,
                    node_font=('helvetica', -14, 'bold'),
                    leaf_font=('helvetica', -12, 'italic'),
                    roof_fill='white', roof_color='black',
                    leaf_color='green4', node_color='blue2')

        cf.add_widget(tc,10,j)
        tc.bind_click_trees(tc.toggle_collapsed)
        j += 500

    # Run mainloop
    cf.mainloop()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'Type your poem number, and (optionally) your stanza number to generate trees.'
        print '> python drawtree 123114 3'

    elif len(sys.argv) == 2:
        todo = [ s.rstrip('</EOS> ').replace('</>','(/)').replace('<//>','(//)')
                 for s in  grab_file(sys.argv[1]) ]
        test(todo)

    else:
        todo = [ s.rstrip('</EOS> ').replace('</>','(/)').replace('<//>','(//)')
                 for s in  grab_stanza(sys.argv[1], int(sys.argv[2])) ]
        print grab_stanza(sys.argv[1], int(sys.argv[2]))
        print todo
        test(todo)
