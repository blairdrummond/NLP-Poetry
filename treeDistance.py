# Edited off of https://github.com/timtadh/zhang-shasha

# tree.label()
# tree[i] is child i

import zss, re

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


def getA():
    return ottawaTree.parse('(S (NP cat) (VP (V in) (NP (Det the) (N hat))))')

def getB():
    return ottawaTree.parse('(ROOT (VP poop) (NP poop))')


def test(a, b):
    #dist = zss.simple_distance(A, B, get_children, get_label, POS_difference)
    dist = zss.simple_distance(a, b, ottawaTree.get_children, ottawaTree.get_label, distance)

    print dist
    #assert dist == 20
