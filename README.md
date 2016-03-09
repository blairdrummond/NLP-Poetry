# NLP-Poetry
Syntactic Analysis of a corpus of poems

A work in progress conducting a syntactic analysis of a corpora of poems as a part of an UROP project (Undergraduate Research Opprotunity Program),from the University Of Ottawa,
It is also a component of a larger project funded by a SSHRC (Social Sciences and Humanities Research Council) research grant, "Poetry Computational Graphs", for which Dr. Chris Tanasescu is the Principle Investigator, and Dr. Diana Inkpen is the Co-Investigator.

Home Website:
http://artsites.uottawa.ca/margento/en/the-graph-poem/

## BUGS

### Comaptibility Issues
There may be compatibility problems between python 2 and 3. I've started edits to this, but I need to test the code to verify that these issues have been resolved.

### Java hasn't been tested
This was written in an old version of the stanford corenlp project (2014). Should test to see if the newest version is still compatible. In fact, I have to redesign the directory system somewhat to accomodate new software versions going into the future (That shouldn't actually be too hard though).

## Dependencies:

Java 8, Stanford-CoreNLP, python, nltk, zss, editdist, tkinter for python

**MAY NOT BE COMPREHENSIVE!**


## Links:

|                            |                                                 |
|:---------------------------|:------------------------------------------------|
|  Stanford CoreNLP          | http://nlp.stanford.edu/software/corenlp.shtml  |
| Natural Language Tool Kit  | http://www.nltk.org/                            |
| editdist                   | http://www.mindrot.org/projects/py-editdist/    |
| Zhang-Shasha tree distance | https://github.com/timtadh/zhang-shasha         |
