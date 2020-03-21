#!/usr/bin/python3
import os
import shutil
import mimetypes
import time
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


def get_folder_name_by_month(file_bd, amount):
    file_bd_date = datetime.fromtimestamp(file_bd)
    start_month = (file_bd_date.month // amount * amount) + 1
    period_start_date = file_bd_date.replace(day=1, month=start_month)
    end_month = period_start_date.month + amount - 1
    period_start_date_formatted = period_start_date.strftime("%B")
    if amount == 1:
        return "{} {}".format(period_start_date_formatted, period_start_date.year)
    period_end_date = period_start_date.replace(month=end_month)
    period_end_date_formatted = period_end_date.strftime("%B")
    return "{} - {} {}".format(period_start_date_formatted, period_end_date_formatted, period_end_date.year)


def get_folder_name_by_day_or_week(file_bd, isDay, amount):
    shift_to_monday = 259200
    timezone_difference = get_timezone_difference()
    day_in_seconds = 86400
    week_in_seconds = day_in_seconds * 7

    if isDay:
        current_period_in_seconds = day_in_seconds * amount
        current_period_in_days = amount
    else:
        current_period_in_seconds = week_in_seconds * amount
        current_period_in_days = amount * 7
    raw_period_start_date_in_seconds = file_bd // current_period_in_seconds * current_period_in_seconds
    period_start_date_in_seconds = raw_period_start_date_in_seconds + timezone_difference - shift_to_monday
    period_start_date = datetime.fromtimestamp(period_start_date_in_seconds)
    if isDay and amount == 1:
        period_start_date_formatted = period_start_date.strftime("%d %B")
        return "{} {}".format(period_start_date_formatted, period_start_date.year)
    period_start_date_formatted = period_start_date.strftime("%d %b")
    period_end_date = period_start_date + timedelta(days=current_period_in_days-1)
    period_end_date_formatted = period_end_date.strftime("%d %b")
    return "{} - {} {}".format(period_start_date_formatted, period_end_date_formatted, period_end_date.year)


def get_folder_name_by_dates(file_bd, frame, amount):
    if frame == 'm':
        return get_folder_name_by_month(file_bd, amount)
    elif frame == 'd' or frame == 'w':
        return get_folder_name_by_day_or_week(file_bd, frame == 'd', amount)
    else:
        raise ValueError("Frame is not correct!")


def sort_files_by_dates(directory_path, frame, amount):
    marking_file_name = '.marking_file'
    list_of_files = os.listdir(directory_path)
    for file in list_of_files:
        file_path = os.path.join(directory_path, file)
        if file.startswith('.'):
            continue
        if os.path.isdir(file_path) and marking_file_name in os.listdir(file_path):
            continue
        file_bd = os.stat(file_path).st_birthtime
        folder_name = get_folder_name_by_dates(file_bd, frame, amount)

        file_type = get_file_type(file)
        related_period_path = os.path.join(directory_path, folder_name)
        related_directory_path = os.path.join(related_period_path, file_type)
        file_path = os.path.join(directory_path, file)
        new_file_path = os.path.join(related_directory_path, file)

        if not os.path.exists(related_period_path):
            os.mkdir(related_period_path)
            hidden_file_path = os.path.join(related_period_path, marking_file_name)
            open(hidden_file_path, 'w+').close()
        if not os.path.exists(related_directory_path):
            os.mkdir(related_directory_path)
        shutil.move(file_path, new_file_path)


sort_files_by_dates('/Users/pavelpysenkin/Desktop/test/', 'd', 1)


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