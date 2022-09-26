
import os
import re
from tabulate import tabulate


cwd = os.getcwd()


def init() -> None:
    """
    Print user information 
    """

    print('-'*60)
    print('CLI Application to sanitize the delimiter in csv files')
    print('-'*60)
    print(f'CWD: {cwd}')
    print('-'*60)
    
    table_information = [['Parameter', 'Description', 'Value'], 
    ['Path', 'Provide the file path', '/file.csv or C:/.../file.csv'], 
    ['Flag', 'Absolute or relative path', 'a or r'],
    ['Delimiter', 'Delimiter used in csv file', 'semicolon']]

    print(tabulate(table_information, headers='firstrow', tablefmt='grid'))

    print('\n')

    export_file()


def get_file_path() -> str:
    """
    Get either the relative or absolute file path as a character string
    """

    while True:
        try:

            file_path = str(input('File Path: '))
            path_flag = str(input('Absolute or relative path: '))

            if not isinstance(file_path, str):
                raise TypeError('File path needs to be a string')

            if not re.match('', file_path):
                raise ValueError('Provide a valid file name')

            if len(file_path) == 0:
                raise ValueError('Provide a file path')

            if path_flag not in ['a', 'r']:
                raise ValueError('Provide a valid flag (a or r)')

            if path_flag == 'a':
                if not os.path.exists(file_path):
                    raise FileNotFoundError('No file found')

            if path_flag == 'r':
                if not os.path.exists(f'{cwd}\{file_path}'):
                    raise FileNotFoundError('No file found')


        except (TypeError, ValueError, FileNotFoundError) as e:
            print(e)

        else:
            break


    if path_flag == 'a':
        return file_path
    else:
        return f'{cwd}\{file_path}'


def sanitize_file() -> list[str]:
    """
    Sanitize the files content from unnecessary delimiters
    The problem with multiple delimiters occurs during the export 
    of excel files (xls) to csv files within excel
    """

    file_path = get_file_path()

    with open(file=file_path, mode='r') as file:

        readableStream = list(file.read())

        letter_count = 0
        counter = 0
        dic = {
            "count": [],
            "action": []
        }
        tmp = []


        for index, letter in enumerate(readableStream):

            if letter == ';':
                letter_count += 1
                dic['action'].append(f'Count: {counter}')

            if letter_count >= 1 and letter != ';':
                letter_count = 0
                dic['action'].append(f'Stop: {counter}')

            if letter_count > 1 and letter == ';':
                dic['action'].append(f'Remove: {counter}')
                
                tmp.append(index)
            

        sanitized_list = [i for j, i in enumerate(readableStream) if j not in tmp]


        print('-'*60)
        print(f'Removed {len(dic["count"])} from {len(readableStream)} data entries')
        print('-'*60)


        return sanitized_list


def export_file() -> None:

    data = sanitize_file()

    try:

        with open('./san_file.csv', 'x') as file:

            file.write(' '.join(data))

    except FileExistsError as e:
        print(f'Cannot export: {e}')     


if __name__ == '__main__':

    init()