#!/usr/bin/python3

import os

def sort_files(link):
    list_of_files = os.listdir(link)
    for file in list_of_files:
        print(file)

sort_files('/Users/pavelpysenkin/Desktop/test/')