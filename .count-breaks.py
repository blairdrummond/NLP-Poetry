# Finds the number of line (and stanza breaks), as well as their context, and appends them onto the file

# Blair bdrum047@uottawa.ca

import os, re, sys, copy

directory = 'output/'

# Better to compile these ahead of time (They get used a lot)
head = re.compile('(?<=\()[A-Z$]+')
line_sibl = re.compile('[A-Z$]+(?= ((\(. .)|[^\(])+\)+  </>)')
line_sibr = re.compile('(?<=</> )(?:.*?)([A-Z$]+)')
stan_sibl = re.compile('[A-Z$]+(?= ((\(. .)|[^\(])+\)+  <//>)')
stan_sibr = re.compile('(?<=<//> )(?:.*?)([A-Z$]+)')
punct     = re.compile("""(?<=\([;:.,\?!-] )[;:.,\?!-](?=(\( ["'`]{1,2} ["'`]{1,2}\))?\)+  (<EOS> )?<//?>)""")
splitlines= re.compile('(</>|<//>)')
words     = re.compile("[a-zA-Z'0-9](?=\))")

################# Find subtree ######################

class Poem:
    def __init__(self, stanza_breaks, enjambed_stanzas):

        self.stanza_breaks    = stanza_breaks
        self.enjambed_stanzas = enjambed_stanzas
        
        self.line_breaks      = 0
        self.num_sentences    = 0
        self.enjambed_lines   = 0
        self.stanzas          = []


    def add_stanza(self,stanza):
        self.stanzas.append(stanza)

    def stanza_agg_data(self):
        self.stanzas[0].closedbegin = True        
        for i in range(1,len(stanzas)):
            self.stanzas[i].closedbegin = self.stanzas[i-1].closedend        
        
        
        self.num_sentences  = sum( [ x.sentence_ends for x in self.stanzas] )
        self.enjambed_lines = sum( [ x.enjambed      for x in self.stanzas] )
        self.line_breaks    = sum( [ x.lines         for x in self.stanzas] )

        

    def __str__(self):
        self.stanza_agg_data()
        s =('<Poem  NumStanzas="'       + str(self.stanza_breaks)  + 
                '"  NumLines="'         + str(self.line_breaks)    + 
                '"  NumSentences="'     + str(self.num_sentences)  +
                '"  NumEnjambedLines="' + str(self.enjambed_lines) +
            '">\n' +
            '    <Stanzas>\n'                                                           + 
            '        \n'.join( [str(stza) for stza in self.stanzas] )+'\n' + 
            '    </Stanzas>\n'                                                          + 
            '</Poem>')
        return s

def boolToStr(b):
    if b:
        return 'true'
    else:
        return 'false'

class Stanza:
    def __init__(self, number, stanza ):
        self.number        = number
        self.lines         = stanza.count('</>')
        self.sentence_ends = stanza.count('<EOS>')
        self.end_stops     = stanza.count('<EOS> </>')
        self.text          = stanza
        self.enjambed      = self.lines - self.end_stops
        self.end           = None
        self.linebreaks    = []

        self.closedbegin   = False
        self.closedend     = False
        self.listoflines   = []

    def endswith(self, t):
        if t == None:
            self.lines     += 1
            self.end_stops += 1
            self.closedend  = True
        else:
            self.lines     += 1
            self.enjambed  += 1
            self.end = t

        

    def __str__(self):
        temp = copy.copy(self.linebreaks)
        temp.append(self.end)
        self.generate_lines(temp)
        s =('    <Stanza number="' + str(self.number)                       +                       
                  '" closedbegin="'+ boolToStr(self.closedbegin)            + 
                  '" closedend="'  + boolToStr(self.closedend)+'">\n'       + 

            '        <Count  NumLines="'  + str(self.lines)                 + 
                     '"  NumSentences="'  + str(self.sentence_ends)         +
                     '"  NumEnjambed="'   + str(self.enjambed)              +
                     '"/>\n'                                                +

            '        <LineEndings>\n'   + '            '                    +
            '            '.join( [str(line) for line in self.listoflines] ) +
            '        </LineEndings>\n' + 
            '    </Stanza>')
        return s

    def generate_lines(self, breaks):
        lines = splitlines.split(self.text)

        self.listoflines = map( (lambda pair: Line(pair[0], pair[1])),
                                 zip(breaks, [line for line in lines if line != '</>' ])) 
        self.listoflines[-1].stanzabreak = True # the last line is a stanza break

class Line:
    def __init__(self, quad, tree_seg):
        if quad == None:
            self.nobreak      = True
        else:
            self.nobreak      = False
            self.head         = quad[0]
            self.left         = quad[1]
            self.right        = quad[2]
            self.punc         = quad[3]

        self.stanzabreak  = False
        self.length= len(words.findall(tree_seg))
        self.sents = tree_seg.count('<EOS>')
        

    def __str__(self):
        if self.stanzabreak:
            lineend = 'LineEnd="//"'
        else:
            lineend = 'LineEnd="/"'

        if not self.nobreak:
            return '<Line length="'    + str(self.length)  + \
                   '"  NumSentences="' + str(self.sents)   + \
                   '"  '               + lineend           + \
                   '>\n                <Linebreak'         + \
                   '"  head="'         + self.head         + \
                   '"  leftSibling="'  + self.left         + \
                   '"  rightSibling="' + self.right        + \
                   '"  punctuation="'  + self.punc         + \
                   '"/>\n            </Line>\n' 
        else:
            return '<Line length="'    + str(self.length)  + \
                   '"  NumSentences="' + str(self.sents)   + \
                   '"  ' + lineend + '/>\n'

# Little Auxiliary function
# Takes a string and parses out the governing and adjacent tokens
def find_tokens(s,tag):
    if s == None:
        return None

    if tag == '</>':
        sibl = line_sibl
        sibr = line_sibr
    else:
        sibl = stan_sibl
        sibr = stan_sibr

    # find and label head-leftsibling-rightsibling
    htoken = head.search(s).group(0)
    ltoken = sibl.search(s).group(0)
    rtoken = sibr.search(s).group(1)
    punkt  = punct.search(s)

    # if there is no punctuation, denote it with empty string
    if punkt == None:
        return  ( htoken,  ltoken,  rtoken, '' ) 
    else:
        return  ( htoken,  ltoken,  rtoken,  punkt.group(0) )

# builds a list of environements
def match_brackets(s,tag):

    #Find the indeces of every match
    i = s.find(')  '+tag+' (')
    j = s.find(tag)
    list = []
    while j != -1 :
        if j < i+3 or i == -1:
            list.append(  (j,0)  )
            j = s.find(tag, j+1)
        else:
            list.append(  (i,1)  )
            i = s.find(')  '+tag+' (', i+1)
            j = s.find(      tag,      j+1)

    # find the subtree that the break occurs in,, list them in strings
    strings = []
    for j in list:
        
        # Filter out non-tags
        if j[1] == 0:
            strings.append(None)
            continue

        i = j[0]
        # Find the leftmost bracket
        l = i
        lc=2
        while lc != 0:
            l = l-1
            if s[l] == '(':
                lc = lc -1
            elif s[l] == ')':
                lc = lc +1
        # Find the rightmost bracket
        r = i+4 + len(tag)
        rc=-2
        while rc != 0:
            r = r+1
            if s[r] == '(':
                rc = rc -1
            elif s[r] == ')':
                rc = rc +1

        # Save the string found
        strings.append(s[l:r])
        
        # As you go through the string, you have to replace the old occurences of the tag
        # otherwise, the regexes get stuck on first occurence in multi-tagged strings
        s = s.replace(tag, ' '*len(tag) , 1)

    # Parse the tokens out of the branches we just found, and return
    return map(  ( lambda x: find_tokens(x,tag) ),   strings  )

############## END Find subtree #####################





##################### Program Proper #######################

f=0 # file counter
number_of_files = len([item for item in os.listdir(directory)])

for file in os.listdir(directory):
    if file.endswith(".txt") :

        # Completion %. Nice for the user.
        sys.stdout.write("\rCounting breaks..." + str(int(round((f*100)/float(number_of_files)))) + "%")
        sys.stdout.flush()
        f+=1

        read  = open(os.path.join(directory,  file), 'r').read()
        
        # The search destroys read in the process, so grab this now
        total_stanzas    = read.count(   '<//>'  )
        internal_stanzas = read.count(')  <//> (')
        stanza_breaks    = match_brackets(read,'<//>')
        line_breaks      = match_brackets(read,'</>')

        thispoem = Poem(total_stanzas, internal_stanzas)

        stanzas = []
        # Do while loop
        do_condition = True
        while do_condition:
            split = read.partition('<//>')
            if split[2] == '':                              # if: End of the file
                do_condition = False
            else:                                           # else: continue
                read = split[2]                             # delete the processed part of the file
                stanzas.append(split[0].lstrip() + '\n')    # Add new stanza to list




        # Stanzas now is a list of every stanza 
        i = 0
        for stanza in stanzas:
            # Add stanza objects to poem
            thispoem.add_stanza( Stanza(i, stanza) )
            i += 1

        # Put the inline line breaks in their stanza
        extracted_lines = line_breaks
        j = 0
        k = 0
        lines_per_stanza = []
        for stanza in thispoem.stanzas:
            k = k + stanza.lines
            stanza.linebreaks= extracted_lines[j:k]
            j = k

        # Attach stanza ends to lines_per_stanza
        map( (lambda x,y: x.endswith(y)),  thispoem.stanzas , stanza_breaks   )


        write = open(os.path.join(directory, file), 'a') 
        write.write('\n\n\n\n\n' + str(thispoem))
        write.close()
print
