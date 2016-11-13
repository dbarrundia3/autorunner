#  AutoRunner
## Georgia Institute of Technology - CS1301
## Author: Daniel Barrundia

So you have decided you want to make an auto-grader, congrats! Why waste our time grading, when we can make a machine do it in seconds?

## ASSUMPTIONS
* You are a College of Computing TA and you have access to your student's submissions.
* You have a Python script that tests another script (a unittest of some sort written in > Python3)

## STEPS
1. Download the Submission you want to grade from T-Square.
  * Make sure to download the **grades.csv** file that comes inside the download.
2. Unzip the download in your working directory (`Documents/CS1301/`)
3. Move the autograder to the homework directory (`Documents/CS1301/HW4`)
4. Download [autorunner.py](https://github.com/dbarrundia3/autorunner/archive/master.zip) and move it to the homework directory (` Documents/CS1301/HW4`)
5. You should see something like this architecture:
   * /HW4
    * test.py [the autograder python file]
    * autorunner.py
    * grades.csv
    * /last, first(128-bit ID)
     * /Submission attachment(s)
      * hw4.py
    * /last, first(128-bit ID)
     * /Submission attachment(s)
      * hw4.py
6. In your terminal go to the submission directory. (`$ cd /Documents/CS1301/HW4`)
7. In your terminal run the command: python3 -t ~the test filename~ (`$ python3 -t test.py`)
8. At this point the autograder has traversed through each of the student's directories and has graded the submission. Assuming your autograder is well written you will be all set at this point. You will see the result of your autograder on each of the student's directories (i.e. an .html file or a .txt about the result of the test)

</br> Happy Grading,
</br>Daniel Barrundia
