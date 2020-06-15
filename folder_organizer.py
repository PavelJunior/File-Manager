#!/usr/bin/python3
import os
import shutil
import mimetypes
import time
from datetime import datetime, timedelta


class FolderOrganizer:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.marking_file_name = '.marking_file'
        self.file_types = {
            'image': 'Images',
            'video': 'Video',
            'text': 'Text',
            'audio': 'Audio',
            'font': 'Fonts'
        }

    def sort_files(self, sort_order=['d'], time_period='m', qty_of_periods=1):
        list_of_files = os.listdir(self.directory_path)

        for file_name in list_of_files:
            file_path = os.path.join(self.directory_path, file_name)

            if file_name.startswith('.'):
                continue
            if os.path.isdir(file_path) and self.marking_file_name in os.listdir(file_path):
                continue

            new_file_path = self.directory_path

            for step in sort_order:
                if step == 'd':
                    file_bd = os.stat(file_path).st_birthtime
                    file_time_frame = self._get_folder_name_by_date(file_bd, time_period, qty_of_periods)
                    new_file_path = os.path.join(new_file_path, file_time_frame)
                elif step == 'e':
                    file_extension = self._get_folder_name_by_extention(file_path, file_name)
                    new_file_path = os.path.join(new_file_path, file_extension)
                elif step == 't':
                    file_type = self._get_folder_name_by_type(file_name)
                    new_file_path = os.path.join(new_file_path, file_type)
                else:
                    raise ValueError("Used wrong letters for sort order. Only letters 'd','e','t' are acceptable.")

                if not os.path.exists(new_file_path):
                    os.mkdir(new_file_path)
                    hidden_file_path = os.path.join(new_file_path, self.marking_file_name)
                    open(hidden_file_path, 'w+').close()

            if os.path.exists(os.path.join(new_file_path, file_name)):
                file_name = self._alter_file_name(file_name, new_file_path)

            new_file_path = os.path.join(new_file_path, file_name)
            shutil.move(file_path, new_file_path)

    def _alter_file_name(self, file_name, new_file_path):
        counter = 2
        new_name = file_name
        while os.path.exists(os.path.join(new_file_path, new_name)):
            if '.' in file_name:
                file_parts = file_name.rsplit('.')
                new_name = file_parts[0] + f" ({counter})." + file_parts[1]
            else:
                new_name = file_name + f" ({counter})"
            counter += 1
        return new_name

    def _get_folder_name_by_type(self, obj):
        mime = mimetypes.guess_type(obj)[0]
        try:
            file_type = mime.split('/')[0]
            return self.file_types.get(file_type, 'Other')
        except AttributeError:
            return 'Other'

    def _get_folder_name_by_date(self, file_bd, time_period, qty_of_periods):
        if time_period == 'm':
            return self.__get_folder_name_by_month(file_bd, qty_of_periods)
        elif time_period == 'd' or time_period == 'w':
            return self.__get_folder_name_by_day_or_week(file_bd, time_period == 'd', qty_of_periods)
        else:
            raise ValueError("Selected time period is not supported. "
                             "Choose one of the following values: 'd', 'w', 'm'")

    def _get_folder_name_by_extention(self, file_path, file_name):
        if os.path.isdir(file_path):
            file_extension = 'folders'
        elif '.' in file_name:
            file_extension = file_name.split('.')[-1]
        else:
            file_extension = 'other'
        return file_extension

    def __get_folder_name_by_month(self, file_bd, qty_of_months):
        if qty_of_months not in [1, 2, 3, 4, 6]:
            raise ValueError("Selected month quantity is not supported. "
                             "Choose one of the following values: 1,2,3,4,6")
        file_bd_date = datetime.fromtimestamp(file_bd)
        start_month = (file_bd_date.month // qty_of_months * qty_of_months) + 1
        period_start_date = file_bd_date.replace(day=1, month=start_month)
        end_month = period_start_date.month + qty_of_months - 1
        period_start_date_formatted = period_start_date.strftime("%B")
        if qty_of_months == 1:
            return "{} {}".format(period_start_date_formatted, period_start_date.year)
        period_end_date = period_start_date.replace(month=end_month)
        period_end_date_formatted = period_end_date.strftime("%B")
        return "{} - {} {}".format(period_start_date_formatted, period_end_date_formatted, period_end_date.year)

    def __get_folder_name_by_day_or_week(self, file_bd, isDay, qty_of_periods):
        shift_to_monday = 259200
        timezone_difference = self.__get_timezone_difference()
        day_in_seconds = 86400
        week_in_seconds = day_in_seconds * 7

        if isDay:
            current_period_in_seconds = day_in_seconds * qty_of_periods
            current_period_in_days = qty_of_periods
        else:
            current_period_in_seconds = week_in_seconds * qty_of_periods
            current_period_in_days = qty_of_periods * 7
        raw_period_start_date_in_seconds = file_bd // current_period_in_seconds * current_period_in_seconds
        period_start_date_in_seconds = raw_period_start_date_in_seconds + timezone_difference - shift_to_monday
        period_start_date = datetime.fromtimestamp(period_start_date_in_seconds)
        if isDay and qty_of_periods == 1:
            period_start_date_formatted = period_start_date.strftime("%d %B")
            return "{} {}".format(period_start_date_formatted, period_start_date.year)
        period_start_date_formatted = period_start_date.strftime("%d %b")
        period_end_date = period_start_date + timedelta(days=current_period_in_days-1)
        period_end_date_formatted = period_end_date.strftime("%d %b")
        return "{} - {} {}".format(period_start_date_formatted, period_end_date_formatted, period_end_date.year)

    def __get_timezone_difference(self):
        t = time.localtime()
        if t.tm_isdst == 0:
            return time.timezone
        else:
            return time.altzone