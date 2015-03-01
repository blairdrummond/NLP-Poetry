# Finds the number of line (and stanza breaks), as well as their context, and appends them onto the file

# Blair bdrum047@uottawa.ca

import os, re, sys

directory = 'output/'

# Better to compile these ahead of time (They get used a lot)
head = re.compile('(?<=\()[A-Z$]+')
line_sibl = re.compile('[A-Z$]+(?= ((\(. .)|[^\(])+\)+  </>)')
line_sibr = re.compile('(?<=</> )(?:.*?)([A-Z$]+)')
stan_sibl = re.compile('[A-Z$]+(?= ((\(. .)|[^\(])+\)+  <//>)')
stan_sibr = re.compile('(?<=<//> )(?:.*?)([A-Z$]+)')
punct     = re.compile("""(?<=\([;:.,\?!-] )[;:.,\?!-](?=(\( ["'`]{1,2} ["'`]{1,2}\))?\)+  (<EOS> )?<//?>)""")

################# Find subtree ######################

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

    htoken = head.search(s).group(0)
    ltoken = sibl.search(s).group(0)
    rtoken = sibr.search(s).group(1)
    punkt  = punct.search(s)

    if punkt == None:
        return  ( htoken,  ltoken,  rtoken ) 
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
        internal_stanzas = read.count(')  <//> (')
        total_stanzas    = read.count(   '<//>'  )
        stanza_breaks    = match_brackets(read,'<//>')
        line_breaks      = match_brackets(read,'</>')


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
        # ends = [ ( #of'</>' , #of'<EOS>', #of'<EOS> </>')]   
        ends   = []
        for stanza in stanzas:
            #print stanza
            ends.append((stanza.count('</>'),    stanza.count('<EOS>'),    stanza.count('<EOS> </>')))

        # Put the inline line breaks in the bin of their stanza number
        extracted_lines = line_breaks
        j = 0
        k = 0
        lines_per_stanza = []
        for end in ends:
            k = k+end[0]
            lines_per_stanza.append(extracted_lines[j:k])
            j = k

        # Attach stanza ends to lines_per_stanza
        map( (lambda x,y: x.append(y)),  lines_per_stanza , stanza_breaks   )

        for i in range(0, len(ends)):
            if lines_per_stanza[i][-1] == None:
                ends[i] = (ends[i][0] + 1 , ends[i][1], ends[i][2] + 1)
            else:
                ends[i] = (ends[i][0] + 1 , ends[i][1], ends[i][2])           

             
        # All Data gathered, do a little post-proccessing and write to file.
        write_string = "total # of stanzas : "     + str(total_stanzas)    + '\n' + \
                       "inline     stanzas : "+ str(internal_stanzas) + '\n' + \
                       "break environments : ( HEAD, LEFT, RIGHT, Punctuation ) \n\n"     + \
                       str(stanza_breaks) + '\n\nstanzas #\n ( # of </> , # of End , # of End </>, Punctuation )\n[ List of linebreak environments ]\n\n' 

        # append this new information, once per stanza
        for i in range(0, len(ends)):
            write_string += 'stanza ' + str(i) + '\n' + str(ends[i]) + '\n' + str(lines_per_stanza[i]) + '\n\n'

        write = open(os.path.join(directory, file), 'a') 
        write.write('\n\n\n\n\n' + write_string)
        write.close()
print
