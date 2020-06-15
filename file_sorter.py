import time
from watchdog.observers import Observer
from folder_observer import FolderObserver
from folder_organizer import FolderOrganizer
import argparse

parser = argparse.ArgumentParser(description='Process some arguments.')

parser.add_argument('order', help='Choose from one to three of sorting types in any order you prefer '
                                  '(t - by type, e - by extension, d - by date) [Ex: "det", "d", "et"]')
parser.add_argument('-period', '--time-period', choices=['d', 'w', 'm'], default='m', metavar='\b',
                    help='Time period used for date sorting (d - day, w = week, m = month)')
parser.add_argument('-qty', '--quantity-of-periods',  default=1, metavar='\b',
                    help='Amount of time periods used for date sorting')
parser.add_argument('-o', '--observer',  default=False, action='store_true')
parser.add_argument('folder_path', help='Folder that you want to sort')

args = parser.parse_args()

if args.observer:
    event_handler = FolderObserver(args.folder_path, args.order, args.time_period, int(args.quantity_of_periods))
    observer = Observer()
    observer.schedule(event_handler, args.folder_path)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
else:
    file_sorter = FolderOrganizer(args.folder_path)
    file_sorter.sort_files(args.order, args.time_period, int(args.quantity_of_periods))







