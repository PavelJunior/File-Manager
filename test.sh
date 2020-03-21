#!/bin/bash

dr='/Users/pavelpysenkin/Desktop/'
cd $dr
rm -R test/
mkdir test
cd 'Projects/fileSorter'
bash folder_filler.sh "$dr/test"
python3 file_sorter.py