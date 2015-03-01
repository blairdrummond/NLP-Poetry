#!/usr/bin/env bash
#
# Runs Stanford CoreNLP.
#
# Place annotated poems in /poems/, run this, recieve poems with appended statistics in /output/ TODO
#
# Blair bdrum047@uottawa.ca
#
# WARNING: I used regex and I don't really know regex. The code SHOULD allow you to update jar versions in the 
# stanford-core folder without out-dating this script, but if something goes awry they should be investigated.
#
# place="$(pwd)"
#
#
#
# The script runs a python file (remove-tags.py) to remove annotations for the Core to read

# It sets these in /.temp/, and it also lists all the poem names in a hidden .PoemList.txt file for the java system

# Then the script copies a settings file out of the CORE-NLP folder into the /.trees/xml/ bin for .xml output. 

# then the system switches directories and loads the java system with all the files. Annotated poems go to /.trees/

# The parse trees are then ripped out of the xml and set in the same folder by .xml-to-penn.py

# The xmls are moved into a seperate folder

# (The trees are then stripped of all unicode)

# .mark-breaks.py adds the line-break data that was lost in CORE processing

# .EOS-tags.py adds some usefull tags to indicate sentence endings (useful in the next step)

# .count-breaks.py then tabulates the statistics of the line-breaks.

# finally the system flushes all temporary folders. TODO 

OS=`uname`
# Macs (BSD) don't support readlink -e
if [ "$OS" == "Darwin" ]; then
  scriptdir=`dirname $0`
else
  scriptpath=$(readlink -e "$0") || scriptpath=$0
  scriptdir=$(dirname "$scriptpath")
fi


if [ "$#" -ne 3 ]; then
    echo "Illegal number of parameters"
    echo "./run.sh <Your Folder> <-ram> <Xg or Xm>"
    exit 1
fi

# Choose Folder
if [ -d $1 ]; then
    input=$1
else
    echo "That directory does not exist."
    exit 1
fi


# Take input ram
if [[ $2 =~ ^\-ram$ && $3 =~ ^[1-9][0-9]*(m|g)$ ]]; then
    echo
    echo "Using $3 of RAM"
    RAM=$3
else
    echo
    echo "./run.sh <Your Folder> <-ram> <Xg or Xm>"
    exit 1
fi


rm -rf .temp/*
rm -rf .temp/.unicode/*
rm -rf output/*
rm -rf .trees/*

mkdir .trees/xml/


#Run a few things in the current directory to prepare, then switch to the CORE-NLP folder
python .remove-tags.py "$input"
#convert unicode to ascii
sh ./.unicode-to-ascii.sh .temp/


# Copy a file from stanford to output, then enter that directory
# If statement checks whether the directory is immediately available, or if it needs to go through its parent directory.

cp stanford\-corenlp*/CoreNLP-to-HTML.xsl .trees/xml/
cd stanford\-corenlp* $*


#Start the tool
echo
echo Loading all .txt files in /"$input"/
echo

core=( $(find stanford\-corenlp\-[0-9]\.[0-9]\.[0-9]\.jar) )
models=( $(find stanford\-corenlp\-[0-9]\.[0-9]\.[0-9]\-models\.jar) )
ejml=( $(find ejml\-[0-9]\.*[0-9]\.jar) )

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# IF SOMETHING IS WRONG, CHECK THE REGEX IN THE JAVA LINE
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

java -cp "${core[0]}":"${models[0]}":xom.jar:joda-time.jar:jollyday.jar:"${ejml[0]}" -Xmx"$RAM" edu.stanford.nlp.pipeline.StanfordCoreNLP [ -props ../StanfordSettings.properties ] -filelist ../.PoemsList.txt -replaceExtension -outputDirectory ../.trees/

echo "Finished building parse trees."

cd ../

python .xml-to-penn.py
mv .trees/*.xml .trees/xml/
sh ./.unicode-to-ascii.sh .trees/

python .mark-breaks.py
python .EOS-tags.py
python .count-breaks.py
