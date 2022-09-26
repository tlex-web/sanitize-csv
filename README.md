
# CLI Application to sanitize CSV files from duplicate delimiters

How to use this application?

run `python -3 -m sanitize_csv.py` 

Select the file that you want to sanitize and clarify, if your path is a relative or absolute path.
Then provide the delimiter used in the csv file.


| Argument   | Description                          | Example                     |
| -----------| ------------------------------------ | --------------------------- |
| Filename   | Name of the file including extension | file.csv or C:\...\file.csv |
| Path       | absolute or relative path            | a or r                      |
| Delimiter  | Delimiter used in the csv file       | e.g. semicolon              |


Beware: This software cannot distinguish between the semantics and the syntax. 
Check if the removal of the delimiter lowers the information of the file

1. Dependencies:
    - Python version 3.10
    - Modules:
        - os
        - re
        - tabulator

