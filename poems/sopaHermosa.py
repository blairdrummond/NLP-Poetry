#############################################
#Script that crawls the Poetry Foundation's #
#poetry archive and retrieves each poem     #
#embedded in the html of each webpage in the#
#archive                                    #
#############################################

from bs4 import BeautifulSoup # pip install beautifulsoup4
import urllib.request, urllib.error
import re

def checkURL(url):
    try:
        urllib.request.urlopen(url)
        return True
    except urllib.error.URLError:
        return False

##contNoSubs=0
##contSubs=0
for i in range(2400000,250000):
    
    url='http://www.poetryfoundation.org/poem/'+str(i)#input('URL:')
    if  checkURL(url)==True:
        poemPage=urllib.request.urlopen(url)
        if  url == poemPage.geturl():                                       #For some reason any redirects to 'article' pages break bs 
            #bool(re.findall(re.compile('poem'),poemPage.geturl()))==True:  #so we need to ensure the url we get contains the word 'poem' or that the current url and the target match
            soup = BeautifulSoup(poemPage)                                  
            title=str(soup.title.get_text()).split(' by')[0]
            if len(soup.title.get_text().split(' by '))!=0 and len(soup.title.get_text().split(' by ')[1].split(' : '))!=0:
                authorSpaced=str(soup.title.get_text().split(' by ')[1].split(' : ')[0])    #Within the html the author's name is often spaced with
                author=' '.join(authorSpaced.split()) #two spaces so we need to remove one before writing
                poem=BeautifulSoup(str(soup('div',class_="poem")))
                text=poem.get_text()[1:-1]+'\n\n'

            subject=soup.find_all(href=re.compile("#subject"))
            subjectsDup=BeautifulSoup(str(subject)).get_text().split(', ')
            subjectsDup.remove('[Seasonal Poems')                   #'Seasonal Poems' and 'Love Poems' would always be included
            subjectsDup.remove('Love Poems]')                       #in the 'Subjects' section regardless of the poem so they need
            subjects=[]                                             #to be removed by default
            for j in subjectsDup:
                if not j in subjects:
                    subjects.append(j)

            if subjects==[]:
    ##            contNoSubs+=1
                poemLocation='/home/feasinde/Dropbox/NLP/Project/poems_no_subjects/%d.txt'
                with open(str(poemLocation%i),'w') as poema:
                    poema.write('title : '+title+'\n\n')
                    poema.write('author : '+author+'\n\n')
                    poema.write('text :'+text+'\n\n')
                    poema.write('subjects : '+', '.join(subjects))
            elif subjects!=[]:
    ##            contSubs+=1
                poemLocation='/home/feasinde/Dropbox/NLP/Project/poems/%d.txt'
                with open(str(poemLocation%i),'w') as poema:
                    poema.write('title : '+title+'\n\n')
                    poema.write('author : '+author+'\n\n')
                    poema.write('text : '+text+'\n\n')
                    poema.write('subjects : '+', '.join(subjects))
        #else: print('Not a URL I care for')


