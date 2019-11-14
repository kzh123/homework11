"""
    HW08
    @author:10456094
"""

from datetime import datetime, timedelta
from prettytable import PrettyTable
import os as os


def date_arithmetic():
    """
    return
    three_days_after_02272000,
    three_days_after_02272017,
    days_passed_01012017_10312017(between these date)
    """
    dt1 = datetime.strptime("February 27, 2000", "%B %d, %Y")
    three_days_after_02272000 = dt1 + timedelta(days=3)
    dt2 = datetime.strptime('February, 27, 2017', "%B, %d, %Y")
    three_days_after_02272017 = dt2 + timedelta(days=3)
    dt3 = datetime.strptime('January 1, 2017', "%B %d, %Y")
    dt4 = datetime.strptime('October 31, 2017', "%B %d, %Y")
    days_passed_01012017_10312017 = dt4 - dt3
    return f"{three_days_after_02272000:%m/%d/%y}, " \
           f"{three_days_after_02272017:%m/%d/%y}, " \
           f"{days_passed_01012017_10312017.days}"


def file_reading_gen(path, field, sep=',', header=False):
    """field separated file reader"""
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        raise FileNotFoundError("No such file or can not open the file!")
    else:
        with fp:
            flag = 0
            for line in fp:
                if header:
                    flag += 1
                    header = False

                else:
                    flag += 1
                    list1 = line.rstrip("\n").split(sep)
                    if len(list1) == field:
                        yield list1
                    else:
                        raise ValueError(f'"{path}" has {len(list1)} fields on line {flag} but expected {field}')


class FileAnalyzer:
    """return a pretty table, the files' info is stored in a dict"""

    def __init__(self, directory):
        """initialization"""
        self.directory = dict()
        try:
            list_file = os.listdir(directory)
        except FileNotFoundError:
            raise FileNotFoundError
        else:
            list_file_py = [item for item in list_file if item[-3:] == ".py"]
            os.chdir(directory)
            for file in list_file_py:
                count_line = 0
                count_word = 0
                count_def = 0
                count_class = 0
                try:
                    fp = open(file, 'r')
                except FileNotFoundError:
                    raise FileNotFoundError

                else:
                    with fp:
                        for line in fp:
                            count_line += 1
                            count_word += len(line)
                            if line.strip()[0:4] == 'def ':
                                count_def += 1

                            if line.strip()[0:6] == 'class ':
                                count_class += 1
                self.files_summary(directory, file, count_class, count_def, count_line, count_word)

    def files_summary(self, dire, filename, class_num, func_num, line_num, char_num):
        """
            The keys of dictionary will be the filename of a python file,
            the value of each key will be a dict as well
        """

        self.directory.update({dire + '/' + filename: {'class': class_num, 'function': func_num, 'line': line_num, 'char': char_num}})

    def pretty_print(self):
        """draw a table"""
        pt = PrettyTable(field_names=['File Name', "Classes", "Functions", "Lines", "Characters"])
        for key, value in self.directory.items():
            pt.add_row([key, value['class'], value['function'], value['line'], value['char']])
        return pt

