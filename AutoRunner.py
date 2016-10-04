import os
import csv
import getopt
import sys
"""
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
class AutoRunner(object):
    def __init__(self, test_file, file_with_id):
        """
            Parameters:
                test_file:     is the filename of the tester.
                file_with_id:  is where we have our info for each student
        """
        self.test_file = test_file
        self.file_to_test = file_to_test
        self.file_with_id = file_with_id
        self.parent_directory = os.getcwd()
        self.directories = self.clean_directories()

    def run(self):
        count = 0.0
        for index in range(len(self.directories)):
            # Progress report #
            sys.stdout.write("Progress: {:.2f}%\r".format((count / len(self.directories)) * 100))
            sys.stdout.flush()
            count += 1
            path =  os.path.join(self.parent_directory,self.directories[index])
            if index == 0:
                # To start, move the test file to the first directory. #
                os.system('mv {0} {1}'.format(self.test_file, path))

            os.system('cd {0} && python3 {1}'.format(path, self.test_file))

            if index == len(self.directories) - 1:
                # If it's the last directory, move the test file back to the first directory. #
                #first_path = os.path.join(self.parent_directory,self.directories[0])
                os.system('cd {0} && mv {1} {2}'.format(path, self.test_file, self.parent_directory))
            else:
                # Just move the test to the next student #
                next_path = os.path.join(self.parent_directory, self.directories[index + 1], self.test_file)
                os.system('cd {0} && mv {1} {2}'.format(path, self.test_file, next_path))

    def clean_directories(self):
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
            _dir = _dir.replace(',','\,')
            _dir = _dir.replace(' ', '\ ')
            _dir = _dir.replace('(', '\(').replace(')', '\)')
            # --------  our directory name should look like: ------------ #
            #     Burdell\,\ George\(3b6499dca6f092bbbfaf2d4ab2c89836)/   #
            #                                Submission\ attachment\(s\)/ #
            # ----------------------------------------------------------- #
            directories.append(_dir)
        return directories

    def make_students_directories(self):
        """
        Return: list[str] with the names of the directories for each student based on how T-square formats the directories: last, first(128-bit ID)
        """
        with open(self.file_with_id, 'rt') as f:
            csvReader = csv.reader(f)
            namesList = []
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
            f.close()
            return namesList


if __name__ == "__main__":
    argv = sys.argv[1:]
    test_filename     = ''
    grades_filename   = 'grades.csv'

    options, r = getopt.getopt(argv, 't:g', ['test=','grades='])
    for opt, arg in options:
        if opt in ('-t', '--test'):
            test_filename = arg
        elif opt in ('-g', '--grades'):
            grades_filename = arg

    runner = AutoRunner(test_file = test_filename, file_with_id = grades_filename)
    runner.run()