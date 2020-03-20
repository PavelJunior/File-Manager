#!/usr/bin/python3
import os
import shutil
import mimetypes
import time
import stat
from datetime import datetime, timedelta


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


def get_timezone_difference():
    t = time.localtime()
    if t.tm_isdst == 0:
        return time.timezone
    else:
        return time.altzone


def sort_files_by_dates(directory_path):
    shift_to_monday = 259200
    timezone_difference = get_timezone_difference()
    week_in_seconds = 604800
    marking_file_name = '.marking_file'

    list_of_files = os.listdir(directory_path)

    for file in list_of_files:
        file_path = os.path.join(directory_path, file)
        if file.startswith('.'):
            continue
        if os.path.isdir(file_path) and marking_file_name in os.listdir(file_path):
            continue
        file_bd = os.stat(file_path).st_birthtime
        period_start_date_in_seconds = (file_bd // week_in_seconds * week_in_seconds) + timezone_difference - shift_to_monday
        period_start_date = datetime.fromtimestamp(period_start_date_in_seconds)
        period_end_date = period_start_date + timedelta(days=7)
        folder_name = "{} - {} {}".format(period_start_date.strftime("%d %b"), period_end_date.strftime("%d %b"), period_end_date.year)

        file_type = get_file_type(file)
        related_timeline_path = os.path.join(directory_path, folder_name)
        related_directory_path = os.path.join(related_timeline_path, file_type)
        file_path = os.path.join(directory_path, file)
        new_file_path = os.path.join(related_directory_path, file)

        if not os.path.exists(related_timeline_path):
            os.mkdir(related_timeline_path)
            hidden_file_path = os.path.join(related_timeline_path, marking_file_name)
            open(hidden_file_path, 'w+').close()
        if not os.path.exists(related_directory_path):
            os.mkdir(related_directory_path)
        shutil.move(file_path, new_file_path)


sort_files_by_dates('/Users/pavelpysenkin/Desktop/test/')


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


# sort_files('/Users/pavelpysenkin/Desktop/test/')