#!/usr/bin/python3
import os
import shutil
import mimetypes


def get_file_type(obj):
    file_types = {
        'image': 'Images',
        'video': 'Video',
        'text': 'Text',
        'audio': 'Audio',
        'font': 'Fonts'
    }
    mime = mimetypes.guess_type(obj)[0]
    try:
        file_type = mime.split('/')[0]
        return file_types.get(file_type, 'Other')
    except AttributeError:
        return 'Other'

def sort_files(directory_path):
    list_of_files = os.listdir(directory_path)
    reserved_files = ['Images', 'Video', 'Text', 'Audio', 'Fonts', 'Other']
    for file in list_of_files:
        if file.startswith('.') or file in reserved_files:
            continue

        file_type = get_file_type(file)
        related_directory_path = os.path.join(directory_path, file_type)
        file_path = os.path.join(directory_path, file)
        new_file_path = os.path.join(related_directory_path, file)

        if not os.path.exists(related_directory_path):
            os.mkdir(related_directory_path)
        shutil.move(file_path, new_file_path)

sort_files('/Users/pavelpysenkin/Desktop/test/')