# File-Manager
The File-manager Command Line Interface (CLI) Tool can be used for managing files in desire folder with selected rools.
You can choose one or many methods of sorting files in any order:
* by file type
* by file creation date (for this method you can specify time period)
* by file extention

# Usage 
    python file_manager.py [-h] [-period] [-qty] [-o] order folder_path

    positional arguments:
      order                           Choose from one to three of sorting methods in any order you prefer 
                                      (t - by type, e - by extension, d - by date) [Ex: "det", "d", "et"]
      folder_path                     Folder that you want to sort

    optional arguments:
      -h, --help                      Show this help message and exit
      -period, --time-period          Time period used for date sorting (d = day, w = week, m = month)
      -qty, --quantity-of-periods     Amount of time periods used for date sorting
      -o, --observer                  Start observer that will keep track and sort new files appear in folder
# Examples
![Image of Examples](https://github.com/PavelJunior/File-Manager/blob/master/project.png)
