# Edited off of https://github.com/timtadh/zhang-shasha

# TODO: Replace node distance comparator with an actual system

# Blair bdrum047@uottawa.ca

# tree.label()
# tree[i] is child i

import zss, re

# Eventually remove this
from editdist import distance

from nltk.tree import *

parser = re.compile('[^ \(\)]+(?=\))')


def strdist(a, b):
    if a == b:
        return 0
    else:
        return 1

class ottawaTree(object):
    def __init__(self, label):
        self.t = Tree(label, [])
    
    def __str__(self):
        return str(self.t)

    def assign(self, tree):
        self.t = tree

    @staticmethod
    def parse(string):
        s = parser.sub('', string)
        tree = Tree.fromstring(s)
        otree = ottawaTree('x')
        otree.assign(tree)
        return otree

    @staticmethod
    def get_children(tree):

        if tree == None:
            return []
            
        kids = []
        for kid in [branch for branch in tree.t]:
            o = ottawaTree('c')
            o.assign(kid)
            kids.append( o )
        return kids

    @staticmethod
    def get_label(tree):
        if tree == None:
            return ''

        return tree.t.label()


    def addkid(self, branch, before=False):
        if before:  
            self.t.insert(0, branch)
        else:   
            self.t.append(branch)
        return self


['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS','PRP',
'PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']











def POS_difference(a,b):
    










def test(a, b):
    #dist = zss.simple_distance(A, B, get_children, get_label, POS_difference)  # TODO
    dist = zss.simple_distance(a, b, ottawaTree.get_children, ottawaTree.get_label, distance)
    return dist
