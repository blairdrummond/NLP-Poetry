# Crawl through the corpus and extract all of the data from poems.
# This will need to expand as we start attaching values from our results

import os, re

inpath  = 'corpus'
outpath = 'database' 

regexnames  = re.compile('[a-zA-Z\.]+')
regexbirth  = re.compile('((?=b\.)\d{3,4})|((?=\d{4}\-)\d{4})')
regexdeathD = re.compile('(?=\-)\d{4}')
regexcatego = re.compile("[\w\.'][\w\. &']*[\w\.']") # Note the space

all_poets          = set()
all_poems          = set()
all_categories     = set()
all_has_categories = set() 

titles  = ['Mr.', 'Mrs.', 'Miss', 'Dr.', 'Ms.', 'Sir', 'Lady', 'Lord', 'By'  ]

def clean(s):
    return s.strip(""" ' "  """).replace("'","''").replace(',','')

def getNumber(s):
    return int(s[5:-4])

def orNull(s):
    if s == 'NULL':
        return 'NULL'
    else:
        return "'" + s + "'"

class Poem_Type:
    def __init__(self, name, categories, region, subregion, number):
        self.name       = "'" + clean(name) + "'"
        self.categories =  categories 
        self.region     = orNull( clean(region)    )
        self.subregion  = orNull( clean(subregion) )
        self.number     = number 

    def __str__(self):
        return self.name

    def __eq__(self,other):
        return self.name == other.name

    def __hash__(self):
        return hash(str(self))



class Poet_Type:

    # set of Poems
    # first name, middle name(s), last name
    # birthyear
    # death

    def __init__(self, firstname , 
                       middlename,
                       lastname  ,
                       birthyear ,
                       death     ):

        
        self.middlename  = "'" + middlename.title() + "'"
        self.firstname   = "'" + firstname.title()  + "'" 
        self.lastname    = "'" + lastname.title()   + "'"  

        self.birthyear   = birthyear
        self.death       = death      
        self.poemset     = set()
    


    # Equality with side effect of updating information
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        if (self.firstname.lower() != other.firstname.lower() 
            or
            self.lastname.lower()  != other.lastname.lower()):
            return False

        if self.middlename == other.middlename:
            self.poemset    = self.poemset.union(other.poemset)
            other           = self
            return True

        if (len(self.middlename) == 0) ^ (len(other.middlename) == 0):
            return False

        if (len(self.middlename) == 2):
            if (other.middlename[0] == self.middlename[0]) and (self.middlename[1] == '.'):
                self.middlename = other.middlename
                self.poemset    = self.poemset.union(other.poemset)
                other           = self
                return True

        elif (len(self.middlename) == 2):
            if (other.middlename[0] == self.middlename[0]) and (other.middlename[1] == '.'):
                other.middlename = self.middlename
                self.poemset     = self.poemset.union(other.poemset)
                other            = self
                return True
        else:
            return False



    def __str__(self):
        return self.firstname + ' ' + self.lastname




    def __hash__(self):
        return hash(str(self))



    def add_poem(self, poem):
        if not isinstance(poem, Poem_Type):
            return False
        else:
            self.poemset.add(poem)
            return True



####################### Actual Code ##########################

for poem in os.listdir(inpath):
    if poem.startswith('poem.'):
        with open(os.path.join(inpath, poem), 'r') as read:
            text = read.readlines()[:13]
        
        # Weird Glitch gets fixed by this. Hopefully this becomes unneccesary
        if text[1] == '\n':
            text = [text[0]]+text[2:]



        poemTitle  = text[0][:-1] 
        poet       = [pname for pname in regexnames.findall(text[1]) if pname not in titles] 
        bornin     = regexbirth.search(text[2])
        diedin     = regexdeathD.search(text[2])
        region     = regexcatego.findall(text[4])
        categories = regexcatego.findall(','.join(text[5:9]))
        number     = getNumber(poem)

        # TEST BAD DATA
        if bornin == None:
            bornin = 'NULL'
        else:
            bornin = bornin.group(0)

        if diedin == None:
            diedin = 'NULL'
        else:
            diedin = diedin.group(0)

        if poet[1:-1] == []:
            middlename = ''
        else:
            middlename = ' '.join(poet[1:-1])
        

        if poet[0].lower() == 'anonymous':
            firstname = 'Anonymous'
            lastname  = 'Anonymous'
        else:
            firstname = poet[0]
            lastname  = poet[-1]

            
        if region == []:
            region = 'NULL'
            subregion = 'NULL'
        elif len(region) == 1:
            region = region[0]
            subregion = 'NULL'
        else:
            subregion = region[1]
            region    = region[0]


        


        thispoem = Poem_Type(poemTitle, categories, region, subregion, number)
        thispoet = Poet_Type(firstname, middlename, lastname, bornin, diedin)

        thispoet.add_poem(thispoem)
        all_poets.add(thispoet)
        

# for every poet, for every poem, add that poem      
map( 
    (lambda x: map( 
                   (lambda z: all_poems.add( (x,z) )), 
                   x.poemset
    )), 
    all_poets
)
# (poet, poem)

# for every poem, for every category, add that category to the set.
map( 
    (lambda x: map( 
                   (lambda y: all_has_categories.add( (x,y) )), 
                   x[1].categories
    )), 
    all_poems
)  
# ( (poet,poem), category )


# add all categories
map(
    lambda x: all_categories.add(x[1]),
    all_has_categories
)

# Open files to write resulting values into
Wcategories    = open(os.path.join(outpath, 'Categories.txt')      , 'w')
WhasCategories = open(os.path.join(outpath, 'HasCategories.txt')   , 'w')
Wpoets         = open(os.path.join(outpath, 'Poets.txt')           , 'w')
Wpoems         = open(os.path.join(outpath, 'Poems.txt')           , 'w')

Wcategories.write( 'INSERT INTO Categories VALUES ' + ';\n\nINSERT INTO Categories VALUES '.join( map( (lambda s: "('" + clean(s) + "')"),  all_categories))  + ';')

Wpoems.write( 'INSERT INTO Poems VALUES ' + ';\n\nINSERT INTO Poems VALUES '.join( map( (lambda p: '(' + 
                                                                         p[1].name             + ', ' + 
                                                                         p[0].firstname        + ', ' +
                                                                         p[0].middlename        + ', ' +
                                                                         p[0].lastname         + ', ' +
                                                                         p[1].region           + ', ' +
                                                                         p[1].subregion        + ', ' +
                                                                         str(p[1].number)      + ')' ),  
                                                                all_poems   )   ) + ';')

WhasCategories.write( 'INSERT INTO HasCategories VALUES ' + ';\n\nINSERT INTO HasCategories VALUES '.join( map( (lambda p: '(' + 
                                                          p[0][1].name + ', ' + 
                                                          p[0][0].firstname + ', ' + 
                                                          p[0][0].middlename + ', ' + 
                                                          p[0][0].lastname + ', ' + "'" + 
                                                          clean(p[1]) + "'" + ')' ),  
                                         all_has_categories )) + ';')

Wpoets.write( 'INSERT INTO Poets VALUES ' + ';\n\nINSERT INTO Poets VALUES '.join( map( (lambda p: '(' +  
                                                 p.firstname  + ', ' +
                                                 p.middlename + ', ' + 
                                                 p.lastname   + ', ' + 
                                                 p.birthyear  + ', ' + 
                                                 p.death  + ')'),
                                                                                        all_poets) ) + ';' )




# Close all the files
Wcategories.close()
WhasCategories.close()
Wpoets.close()      
Wpoems.close()      



# Re open them and 
# Compile into sql file
tables         = open(os.path.join(outpath, 'poems.sql')           , 'r')
Wcategories    = open(os.path.join(outpath, 'Categories.txt')      , 'r')
WhasCategories = open(os.path.join(outpath, 'HasCategories.txt')   , 'r')
Wpoets         = open(os.path.join(outpath, 'Poets.txt')           , 'r')
Wpoems         = open(os.path.join(outpath, 'Poems.txt')           , 'r')

create_db      = open(os.path.join(outpath, 'create_db.sql')       , 'w')

# Write
create_db.write( tables.read()           + '\n' +
                 Wpoets.read()           + '\n\n' +
                 Wcategories.read()      + '\n\n' +
                 Wpoems.read()           + '\n\n' +
                 WhasCategories.read())

# Close
tables.close()
Wcategories.close()
WhasCategories.close()
Wpoets.close()      
Wpoems.close()      
create_db.close()
