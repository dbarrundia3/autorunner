"""
Execute a unittest or any python script in every student directory based on Georgia Tech's T-Square Download Architecture

Overall structure of T-Square Download Assignment
    +---------------------------------------+
    | /HW # - Description                   |
    |    /last, first(128-bit ID)           |
    |        /Submission attachment(s)      |
    |           ...                         |
    |    /last, first(128-bit ID)           |
    |        /Submission attachment(s)      |
    |           ...                         |
    |     /last, first(128-bit ID)          |
    |         /Submission attachment(s)     |
    |           ...                         |
    |     .                                 |
    |     .                                 |
    |     .                                 |
    +---------------------------------------+
"""

import os
import csv
import getopt
import sys
import argparse
import textwrap

__author__  = "Daniel Barrundia"
__version__ = "2.1"
__email__   = "dbarrundia3@gatech.edu"
__date__    = "October, 2016"

class AutoRunner(object):
    def __init__(self, test_file, file_with_id, dependencies):
        """
            Parameters:
                test_file:     is the filename of the tester/autograder.
                file_with_id:  is the filename of student's information.
        """
        self.test_file = test_file
        self.file_with_id = file_with_id
        self.dependencies = dependencies
        self.parent_directory = self.clean_path(os.getcwd())
        self.directories = self.add_subdir()

    def run(self):
        count = 0.0
        for index in range(len(self.directories)):
            # Progress report #
            sys.stdout.write("Progress: {:.2f}%\r".format((count / len(self.directories)) * 100))
            sys.stdout.flush()
            count += 1
            path =  os.path.join(self.parent_directory,self.directories[index])
            if index == 0:
            # To start, move the test file to the first directory. (1st stud) #
                os.system('mv {0} {1}'.format(self.test_file, path))
                for dependency in self.dependencies:
                    os.system('mv {0} {1}'.format(dependency, path))

            os.system('cd {0} && python3 {1}'.format(path, self.test_file))
            for dependency in self.dependencies:
                os.system('cd {0} && python3 {1}'.format(path, dependency))
            if index == len(self.directories) - 1:
            # If last directory, move test file back to parentt directory. #
                os.system('cd {0} && mv {1} {2}'.format(path, self.test_file, self.parent_directory))
                for dependency in self.dependencies:
                    os.system('cd {0} && mv {1} {2}'.format(path, dependency, self.parent_directory))

            else:
                # Just move the test to the next student #
                next_path = os.path.join(self.parent_directory, self.directories[index + 1])
                os.system('cd {0} && mv {1} {2}'.format(path, self.test_file, os.path.join(next_path,self.test_file)))
                for dependency in self.dependencies:
                    os.system('cd {0} && mv {1} {2}'.format(path, dependency, os.path.join(next_path,dependency)))

    def add_subdir(self):
        """
        Return: list[str] contains the names of the clean directories for each student based on how t-square formats the directories, add the sub directory of Submission attachment(s):
                last, first(128-bit ID) / Submission attachment(s)
        """
        directories = []
        sub_dir = 'Submission attachment(s)'
        for name in self.make_students_directories():
            # -------------  our directory name looks like: ------------- #
            #     Burdell, George(3b6499dca6f092bbbfaf2d4ab2c89836)      #
            # ----------------------------------------------------------- #
            _dir = os.path.join(name,sub_dir)
            _dir = self.clean_path(_dir)
            # --------  our directory name should look like: ------------ #
            #     Burdell\,\ George\(3b6499dca6f092bbbfaf2d4ab2c89836)/   #
            #                                Submission\ attachment\(s\)/ #
            # ----------------------------------------------------------- #
            directories.append(_dir)
        return directories

    def clean_path(self, path):
        """
        Parameters:
        path: str - path to clean

        Return: str which is the path cleaned, by adding a backslash to special characters.
        """
        path = path.replace(',','\,')
        path = path.replace(' ', '\ ')
        path = path.replace('(', '\(').replace(')', '\)')
        return path

    def make_students_directories(self):
        """
        Return: list[str] with the names of the directories for each student
        based on how T-square formats the directories: last, first(128-bit ID)
        """
        with open(self.file_with_id, 'rt') as f:
            csvReader = csv.reader(f)
            namesList = []
            if next(csvReader) and len(next(csvReader))==0:
                # Skip headers from grades.csv if headers exist
                next(csvReader)
            else:
                # Headers have been removed, read from start
                f.seek(0)
            for row in csvReader:
            # --------------  file_with_id looks like: ------------------ #
            # gburdel3,3b6499dca6f092bbbfaf2d4ab2c89836,Burdell, George   #
            # ----------------------------------------------------------- #
                first = str(row[3])
                last = str(row[2]) + ','
                _id = '({0})'.format(row[1])
                name = '{0}{1}{2}'.format(last, first, _id)
            # --------  our directory name should look like: ------------ #
            #     /Burdell, George(3b6499dca6f092bbbfaf2d4ab2c89836)      #
            # ----------------------------------------------------------- #
                namesList.append(name)
        return namesList

def get_args():
    """"""
    parser = argparse.ArgumentParser(
        description = "How to execute autorunner?",
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Example Usages:
            python3 autorunner.py -t hw4_autograder.py
            python3 autorunner.py -t hw4_autograder.py -d helper1.py -d helper2.py
            python3 autorunner.py -t hw4_autograder.py -g rename_grades.csv
        """)
    )

    # required argument
    parser.add_argument('-t', action="store", required=True,
        help='filename of the tester/autograder', dest = 'test_filename')
    # optional arguments
    parser.add_argument('-g', help="csv filename of student's information", default= 'grades.csv', dest = 'grades_filename')
    parser.add_argument('-d', help='filename of a dependency', default = [], action = "append", dest = 'dependencies')
    return (parser.parse_args())

if __name__ == "__main__":
    args = get_args()
    runner = AutoRunner(test_file = args.test_filename, file_with_id = args.grades_filename, dependencies = args.dependencies)
    runner.run()