#!/usr/bin/python3

from watchdog.events import FileSystemEventHandler
from folder_organizer import FolderOrganizer


class FolderObserver(FileSystemEventHandler):
    def __init__(self, folder_path, sort_order=['d'], time_period='m', amount_of_periods=1):
        self.folder_to_track = folder_path
        self.sort_order = sort_order
        self.time_period = time_period
        self.amount_of_periods = amount_of_periods
        self.on_modified(None)

    def on_modified(self, event):
        file_sorter = FolderOrganizer(self.folder_to_track)
        file_sorter.sort_files(self.sort_order, self.time_period, self.amount_of_periods)

    def on_created(self, event):
        file_sorter = FolderOrganizer(self.folder_to_track)
        file_sorter.sort_files(self.sort_order, self.time_period, self.amount_of_periods)


