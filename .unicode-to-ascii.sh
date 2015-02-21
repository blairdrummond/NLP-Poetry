#!/usr/bin/env bash

# Takes an argument directory, in which it finds all surface level .txt files and replaces them with strictly ASCII text.
# It deletes the unicode files, though you can replace pieces of code to easily retain those in a .unicode/ folder

# Blair bdrum047@uottawa.ca

cd "$1"

if [ ! -d .ascii/ ]; then
  mkdir .ascii/
fi

#if [ ! -d .unicode/ ]; then
#  mkdir .unicode/
#fi

for file in *.txt; do
    iconv -f utf-8 -t ascii//TRANSLIT < "$file" > "${file%.txt}.utf8.txt"
done

mv *.utf8.txt .ascii/

## Choose One Line #####
rm -rf *.txt
# mv *.txt .unicode/
########################

mv .ascii/*    $(pwd)
rm -rf .ascii/

for file in *.utf8.txt; do
    mv "$file" "`basename $file .utf8.txt`.txt"
done