#!/usr/bin/python3
import os
import shutil
import mimetypes
import time
from datetime import datetime, timedelta


class FolderOrganizer:
    MARKING_FILE_NAME = '.marking_file'
    ALLOWED_MONTHS_QTY = [1, 2, 3, 4, 6]
    SHIFT_TO_MONDAY = 259200
    DAY_IN_SECONDS = 86400
    WEEK_IN_SECONDS = DAY_IN_SECONDS * 7
    DEFAULT_FOLDER_NAME = 'Other'
    FILE_TYPES = {
            'image': 'Images',
            'video': 'Video',
            'text': 'Text',
            'audio': 'Audio',
            'font': 'Fonts'
        }

    def __init__(self, directory_path):
        self.directory_path = directory_path

    def sort_files(self, sort_order=['d'], time_period='m', qty_of_periods=1):
        """
        The function to distribute files in different folders by selected rules.

        Parameters:
            sort_order (List): Types and order of sorting we want to use. The following values
            are accepted: 'd'(date), 'e'(extension), 't'(type).
            time_period (String): Time period. he following values are accepted: 'd'(day), 'w'(week), 'm'(month)
            qty_of_periods (Integer): quantity of periods.

        Raises:
            ValueError: in case when sort_order contains not accepted letters

        """
        list_of_files = os.listdir(self.directory_path)

        # Iterate over all files in directory
        for file_name in list_of_files:
            file_path = os.path.join(self.directory_path, file_name)

            # Skip hidden files or directories that contain marking file (created by this class).
            if file_name.startswith('.'):
                continue
            if os.path.isdir(file_path) and self.MARKING_FILE_NAME in os.listdir(file_path):
                continue

            new_file_path = self.directory_path

            # Iterate over all elements from sort_order, and create new path for file according to sort properties.
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

                # If folder in new_file_path is not exist in our system we need to create it and mark.
                if not os.path.exists(new_file_path):
                    os.mkdir(new_file_path)
                    hidden_file_path = os.path.join(new_file_path, self.MARKING_FILE_NAME)
                    open(hidden_file_path, 'w+').close()

            # If file with the same name already in destination folder we need to change file name to avoid
            # errors and files overwriting.
            if os.path.exists(os.path.join(new_file_path, file_name)):
                file_name = self._alter_file_name(file_name, new_file_path)

            # Creating a final file path, and move the file.
            new_file_path = os.path.join(new_file_path, file_name)
            shutil.move(file_path, new_file_path)

    def _alter_file_name(self, file_name, file_path):
        """
        The function to add index number to file name if there is file with
        the same name in a destination folder.

        Parameters:
            file_name (String): Name of the file.
            file_path (String): Path to the folder where we want to move the file.

        Returns:
            String: New name of the file
        """
        counter = 2
        new_name = file_name
        while os.path.exists(os.path.join(file_path, new_name)):
            if '.' in file_name:
                file_parts = file_name.rsplit('.')
                new_name = file_parts[0] + f" ({counter})." + file_parts[1]
            else:
                new_name = file_name + f" ({counter})"
            counter += 1
        return new_name

    def _get_folder_name_by_type(self, obj):
        """
        The function to get name of file type (mimetype).

        Parameters:
            obj (String): Name of the object.

        Returns:
            String: One of the values from FILE_TYPES constant, or DEFAULT_FOLDER_NAME
        """
        print(obj)
        mime = mimetypes.guess_type(obj)[0]
        try:
            file_type = mime.split('/')[0]
            return self.FILE_TYPES.get(file_type, self.DEFAULT_FOLDER_NAME)
        except AttributeError:
            return self.DEFAULT_FOLDER_NAME

    def _get_folder_name_by_date(self, file_bd, time_period, qty_of_periods):
        """
        The intermediate function to get folder name, depending on file creation
        time and selected time period and quantity of that period.

        Parameters:
            file_bd (Float): Unix time of creation of file in seconds.
            time_period (String): Selected time period ('d', 'w', 'm')
            qty_of_periods (Integer): quantity of periods.

        Returns:
            String: Name of a folder for a file in chosen time range.

        Raises:
            ValueError: if was provided incorrect time_period
        """
        if time_period == 'm':
            return self.__get_folder_name_by_month(file_bd, qty_of_periods)
        elif time_period == 'd' or time_period == 'w':
            return self.__get_folder_name_by_day_or_week(file_bd, time_period == 'd', qty_of_periods)
        else:
            raise ValueError("Selected time period is not supported. "
                             "Choose one of the following values: 'd', 'w', 'm'")

    def _get_folder_name_by_extention(self, file_path, file_name):
        """
        The function to extract extension of the file.

        Parameters:
            file_path (String): Path to the file.
            file_name (String): Name of the file.

        Returns:
            String: 'Folder' if provided object was folder,
            extension if provided object has extension,
            DEFAULT_FOLDER_NAME if neither above are true.
        """
        if os.path.isdir(file_path):
            file_extension = 'Folders'
        elif '.' in file_name:
            file_extension = file_name.split('.')[-1]
        else:
            file_extension = self.DEFAULT_FOLDER_NAME
        return file_extension

    def __get_folder_name_by_month(self, file_bd, qty_of_months):
        """
        The function to generate name of folder, depending on
        selected month quantity and file creation time.

        Parameters:
            file_bd (Float): Unix time of a creation of the file in seconds.
            qty_of_months (Integer): quantity of months.

        Returns:
            String: Name of a folder for a file in chosen time range.

        Raises:
            ValueError: if qty_of_months is not in ALLOWED_MONTHS_QTY
        """
        if qty_of_months not in self.ALLOWED_MONTHS_QTY:
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
        """
        The function to generate name of folder, depending on
        file creation time and selected time period (days or weeks)
        and quantity of that period.

        Parameters:
            file_bd (Float): Unix time of creation of file in seconds.
            isDay (Bool): True if period is day, False if period is week.
            qty_of_periods (Integer): quantity of periods.

        Returns:
            String: Name of folder for file in chosen time range.
        """
        timezone_difference = self.__get_timezone_difference()

        if isDay:
            current_period_in_seconds = self.DAY_IN_SECONDS * qty_of_periods
            current_period_in_days = qty_of_periods
        else:
            current_period_in_seconds = self.WEEK_IN_SECONDS * qty_of_periods
            current_period_in_days = qty_of_periods * 7
        raw_period_start_date_in_seconds = file_bd // current_period_in_seconds * current_period_in_seconds
        period_start_date_in_seconds = raw_period_start_date_in_seconds + timezone_difference - self.SHIFT_TO_MONDAY
        period_start_date = datetime.fromtimestamp(period_start_date_in_seconds)
        if isDay and qty_of_periods == 1:
            period_start_date_formatted = period_start_date.strftime("%d %B")
            return "{} {}".format(period_start_date_formatted, period_start_date.year)
        period_start_date_formatted = period_start_date.strftime("%d %b")
        period_end_date = period_start_date + timedelta(days=current_period_in_days-1)
        period_end_date_formatted = period_end_date.strftime("%d %b")
        return "{} - {} {}".format(period_start_date_formatted, period_end_date_formatted, period_end_date.year)


    def __get_timezone_difference(self):
        """
        The function to get time difference for different timezones.

        Returns:
            Integer: Quantity of seconds.
        """
        t = time.localtime()
        if t.tm_isdst == 0:
            return time.timezone
        else:
            return time.altzone