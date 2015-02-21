# This is HORRIBLY hacked together. It is operational, but wasn't built with any real plan and should be revised for cleanliness.
# TODO Clean everything

# Read through parse trees and corresponding poem, find all stanza and new line breaks and insert them into the parse tree.
# It works by taking the last "kgram" tokens from the original text, making a regex out of them, and matching against the tree, then inserting.
# If there is an error, it prints the regex that failed, and the file where it occurred.

# Blair bdrum047@uottawa.ca

import os, re, sys

# Test for match using 
kgram = 5

poems   = ".temp/"             # input folder
parses  = ".trees/"            # folder for temporary files
output  = "output/"     # output folder


# Set up regex
pattern     = re.compile(r'(?:[A-Za-z0-9\-]|[^-()a-z&$0-9;.,:\n\r ](?! ))+', re.IGNORECASE) # Tokenize Words and Numbers
contraction = re.compile(r"([a-z0-9]{1,2}\'[a-z0-9;]{1,2})"                , re.IGNORECASE) # Find contractions. Can't -> (Can) (n't)
punctuation = re.compile('[^A-Za-z0-9]')
numbers     = re.compile('([a-z][0-9]|[0-9][a-z])', re.IGNORECASE)

# /===================Convert Line to regex===============================
def regexify(x):

    # Reject Blank Line
    if not x.strip(): 
        return ''

# Mimic Stanford-NLP tokenizing behaviour
# The following list of pairs taken from this site
# https://github.com/nlplab/brat/blob/master/server/src/gtbtokenize.py

    # Break all into seperate POS tokens
    for token in [( 'Cannot'  , 'Can not'  ),
                  ( 'D\'ye'   , 'D\' ye'   ),
                  ( 'Gimme'   , 'Gim me'   ),
                  ( 'Gonna'   , 'Gon na'   ),
                  ( 'Gotta'   , 'Got ta'   ),
                  ( 'Lemme'   , 'Lem me'   ),
                  ( 'More\'n' , 'More \'n' ),
                  ( 'Tis'     , 'T is'     ),
                  ( 'Twas'    , 'T was'    ),
                  ( 'Wanna'   , 'Wan na'   )]:
        x = re.sub(token[0], token[1], x, flags=re.IGNORECASE)
    
    # remove ' and split up word. ["Wouldn't"] -> ["Would","n","'","t"].
    for c in contraction.findall(x):
        x=x.replace(c, ' '+' '.join(c.partition("'")[0]+c.partition("'")[2] )+' ')

    # remove punctuation
    x = x.replace('& ',' &amp; ')
    #for p in ["''",'"','.',',','!','?','-','#','``',':',';',"'"]:
    #    x = x.replace(p,' ')    
    
    x = punctuation.sub(' ',x)

    if not x.strip(): #173312.txt ".... \n" otherwise breaks
        return ''

    for n in numbers.findall(x):
        x = x.replace(n, n[0] + ' ' + n[1])

    # Create list of filtered Tokens
    x = pattern.findall(x)

    # Take up to k Tokens from the end of the list
    if kgram <= len(x):
        x = x[-kgram:]
    else:
        x = x

    x = map(re.escape , x) 
    x = r'(.|\n)*?'.join(x)
        
    x = x + r"(.|\n)*?(?=(\n|\((?![^A-Za-z0-9] .\))))"
    x = x.replace(r'\\\n',r'\n')
    x = x.replace(r'\\',r'\ ')
    return x
# /===================end of method=================================


########################## MAIN PROGRAM ############################

i = 0 # Error counter
j = 0 # File  counter
number_of_files = len([item for item in os.listdir(poems)])

for file in os.listdir(poems):        # iterate through every poem file in input folder
    if file.endswith(".txt"):
        
        # Completion %. Nice for the user.
        sys.stdout.write("\rAdding line-break tags..." + str(int(round((j*100)/float(number_of_files)))) + "%")
        sys.stdout.flush()
        j+=1
        
        with open(os.path.join(parses,'tree_' + file), 'r') as f:
            tree_buffer_A  = f.read()  # Parse Tree of Poem
        tree_buffer_B  = ''                                                     # Buffer for put processed poem
        first          = True                                                   # Needed to prevent accidental <//> on the first line
        breaktype      = ''                                                     # Specifies whether to enter a </> or a <//> (or on the first line, neither)
        tree_buffer_A  = tree_buffer_A.replace("''",'"').replace('``','"').replace('-LRB-','[').replace('-RRB-',']').replace('--','-').replace('...','#')
        
        poems_file =  open(os.path.join(poems, file), 'r')
        for line in poems_file:
            regex = regexify(line)   # Turn end-of-line into a search pattern 
            if regex:                # Line was not blank
                
                # Find first pattern occurence in parse tree
                #print regex
                l = re.search(regex,tree_buffer_A, re.IGNORECASE)

                if l: # Found Occurence:

                    l = l.group(0)                 # Collect the matched String
                    try :        
                        split  = tree_buffer_A.partition(l) # Partition the tree at the match

                    except BaseException:                   # Notify user of any errors, then exit
                        print file
                        print line
                        print l
                        exit()

                                        # Load into the buffer:
                    tree_buffer_B = (
                                        tree_buffer_B + \
                                        # the old buffer itself...  
                                        
                                        breaktype     + \
                                        # The PREVIOUS line's type of break,        
                             
                                        split[0]      + \
                                        # The new content preceeding the match,   
                       
                                        l
                                        # The matched line itself.
                                    )
                                        
                    tree_buffer_A = split[2]                   # Update the lead buffer to the remaining text
                    first         = False                      # This just prevents accidental <//> placement on the first line
                    breaktype     = ' </> '                    # Set the break to line-break, this may be overridden later

                else: # Failed regex  # If failures occur, this
                    print file        # block helps to highlight
                    print regex       # the problem.
                    i=i+1             #

            elif not first:
                breaktype = ' <//> '  # The previous break was a stanza break (Because this is a new line)    
        poems_file.close()
        # Output results
        write = open(os.path.join(output, file), 'w')                  
        write.write(tree_buffer_B + tree_buffer_A[:-2] + " <//> ")
        write.close()

# Print the number of errors
if i == 1:
    print i, "Fail"
elif i>1:
    print i, "Fails"
else:
    print
