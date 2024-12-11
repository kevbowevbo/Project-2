from PyQt6.QtWidgets import *
from gui import *
import csv

class Logic(QMainWindow, Ui_MainWindow):
    """
    Class to set up the logic for a grading application and has class variables to use within the class 
    """
    MIN_ATTEMPTS :int = 0
    MAX_ATTEMPTS :int = 4
    MIN_SCORE :int = 0
    MAX_SCORE :int = 100

    def __init__(self)->None:
        """
        Function Initializes the layout of the ui and hides the score labels and line edits
        :return: None
        """
        super().__init__()
        self.setupUi(self)
        self.Submit_Button.clicked.connect(lambda: self.submit())
        self.Submit_Button.setEnabled(False)
        self.Next_Button.clicked.connect(lambda: self.next())
        self.hiding(4)

    def clearing(self) -> None:
        """
        Function used to clear input text after scores are submitted
        :return: None
        """
        self.StudentName_lineEdit.clear()
        self.Attempts_lineEdit.clear()
        self.Score1_lineEdit.clear()
        self.Score2_lineEdit.clear()
        self.Score3_lineEdit.clear()
        self.Score4_lineEdit.clear()
        self.Outcome_label.clear()

    def hiding(self, num_attempts:int) -> None:
        """
        Function is used to hide the line editors as well as labels depending on the number of attempts are entered
        :param num_attempts: Number of attempts/scores that a student has
        :return:None
        """
        if num_attempts ==1:
            self.Score4_label.hide()
            self.Score4_lineEdit.hide()
        elif num_attempts ==2:
            self.Score4_label.hide()
            self.Score3_label.hide()
            self.Score4_lineEdit.hide()
            self.Score3_lineEdit.hide()
        elif num_attempts == 3:
            self.Score2_label.hide()
            self.Score3_label.hide()
            self.Score4_label.hide()
            self.Score2_lineEdit.hide()
            self.Score3_lineEdit.hide()
            self.Score4_lineEdit.hide()
        elif num_attempts ==4:
            self.Score1_label.hide()
            self.Score2_label.hide()
            self.Score3_label.hide()
            self.Score4_label.hide()
            self.Score1_lineEdit.hide()
            self.Score2_lineEdit.hide()
            self.Score3_lineEdit.hide()
            self.Score4_lineEdit.hide()

    def showing(self, num:int) -> None:
        """
        Function shows the appropriate amount of score labels and score line edit boxes depending on the number that is entered
        :param num: Number of Scores that are put in for a student
        :return:
        """
        if num == 1:
            self.Score1_label.show()
            self.Score1_lineEdit.show()
        if num == 2:
            self.Score1_label.show()
            self.Score2_label.show()
            self.Score1_lineEdit.show()
            self.Score2_lineEdit.show()
        if num == 3:
            self.Score1_label.show()
            self.Score2_label.show()
            self.Score3_label.show()
            self.Score1_lineEdit.show()
            self.Score2_lineEdit.show()
            self.Score3_lineEdit.show()
        if num == 4:
            self.Score1_label.show()
            self.Score2_label.show()
            self.Score3_label.show()
            self.Score4_label.show()
            self.Score1_lineEdit.show()
            self.Score2_lineEdit.show()
            self.Score3_lineEdit.show()
            self.Score4_lineEdit.show()

    def finalscore(self,s1=0,s2=0,s3=0,s4=0) -> float:
        """
        Function takes in 4 scores, if not it is automatically assigned a 0, and finds the average
        :param s1: 1st Score that's input
        :param s2: 2nd Score that's input
        :param s3: 3rd Score that's input
        :param s4: 4th Score that's input
        :return: An average as the Final Score
        """
        final = (s1+s2+s3+s4)/4
        return final

    def read(self,student:str,score1=0, score2=0, score3=0, score4=0) -> None:
        """
        Function takes in the student's name and checks to see if they are already in the csv, and as well to check if
        the csv exist, if not it will create a csv with the students' grades. Otherwise, function read calls the function
        wr if it sees that the name of the student isn't in the csv
        :param student: Name of the student
        :param score1: 1st Score that's input
        :param score2: 2nd Score that's input
        :param score3: 3rd Score that's input
        :param score4: 4th Score that's input
        :return: None
        """
        try:
            repeat = False
            with open("studentdata.csv", "r", newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if student in row:
                        repeat = True
                        raise NameError
                if repeat == False:
                    self.wr(student,score1,score2, score3, score4)
        except FileNotFoundError:
            FinalScore = self.finalscore(score1,score2,score3,score4)
            with open("studentdata.csv", "w+", newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Name", "Score1","Score2","Score3","Score4","Final"])
                csv_writer.writerow([student,score1,score2,score3,score4,FinalScore])

    def wr(self, student:str, score1:float, score2=0, score3=0, score4=0) -> None:
        """
        Function is called in the read function and is used to write the name and scores of a student into the csv file
        :param student: Name of Student
        :param score1: 1st Score that's input
        :param score2: 2nd Score that's input
        :param score3: 3rd Score that's input
        :param score4: 4th Score that's input
        :return: None
        """
        with open("studentdata.csv", "a", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            Finalscore = self.finalscore(score1, score2, score3, score4)
            row = student,score1,score2,score3,score4,Finalscore
            csv_writer.writerow(row)

    def validating(self,s1=99.9,s2=99.9,s3=99.9,s4=99.9) -> None:
        """
        Function validates if the scores are inbetween the range of 0-100 or whatever the class variables are set as
        :param s1: The first score input
        :param s2: The second score input
        :param s3: The third score input
        :param s4: The fourth score input
        :return: None
        """
        if ((s1 < self.MIN_SCORE or s1 > self.MAX_SCORE) or (s2 < self.MIN_SCORE or s2 > self.MAX_SCORE)
                or (s3 < self.MIN_SCORE or s3 > self.MAX_SCORE) or (s4 < self.MIN_SCORE or s4 > self.MAX_SCORE)):
            raise ValueError

    def next(self) -> None:
        """
        Function is the logic that is called whenever the 'next' button is pushed;validates number of attempts,
        sees if student and attempts inputs are correct, calls functions hiding and showing, and if all input are
        correct, it disables the 'attempts' line edit and 'next' button while enabling the 'submit' button
        :return: None
        """
        student = self.StudentName_lineEdit.text().strip()
        attempts = self.Attempts_lineEdit.text().strip()
        try:
            if attempts == '':
                raise UnboundLocalError
            elif student == '':
                raise UnboundLocalError
            attempts = int(attempts)
            if attempts <= self.MIN_ATTEMPTS or attempts > self.MAX_ATTEMPTS:
                raise ValueError
            if attempts == 1:
                self.hiding(3)
                self.showing(1)
            elif attempts == 2:
                self.hiding(2)
                self.showing(2)
            elif attempts == 3:
                self.hiding(1)
                self.showing(3)
            elif attempts == 4:
                self.showing(4)
            self.Next_Button.setEnabled(False)
            self.Attempts_lineEdit.setEnabled(False)
            self.Submit_Button.setEnabled(True)
        except ValueError:
            self.Outcome_label.setText("Enter valid number of Attempts[1-4]")
            self.Outcome_label.setStyleSheet("color: red;")
        except UnboundLocalError:
            if student == '' and attempts == '':
                self.Outcome_label.setText("Enter name and number of Attempts")
                self.Outcome_label.setStyleSheet("color: red;")
            elif student == '':
                self.Outcome_label.setText("Enter Student Name")
                self.Outcome_label.setStyleSheet("color: red;")
            elif attempts == '':
                self.Outcome_label.setText("Enter number of Attempts[1-4]")
                self.Outcome_label.setStyleSheet("color: red;")

    def submit(self) -> None:
        student = self.StudentName_lineEdit.text().strip()
        attempts = int(self.Attempts_lineEdit.text().strip())
        try:
            if attempts==1:
                s1 = float(self.Score1_lineEdit.text().strip())
                self.validating(s1)
                self.read(student,s1)
            elif attempts ==2:
                s1 = float(self.Score1_lineEdit.text().strip())
                s2 = float(self.Score2_lineEdit.text().strip())
                self.validating(s2)
                self.read(student,s1,s2)
            elif attempts == 3:
                s1 = float(self.Score1_lineEdit.text().strip())
                s2 = float(self.Score2_lineEdit.text().strip())
                s3 = float(self.Score3_lineEdit.text().strip())
                self.validating(s1,s2,s3)
                self.read(student,s1,s2,s3)
            elif attempts == 4:
                s1 = float(self.Score1_lineEdit.text().strip())
                s2 = float(self.Score2_lineEdit.text().strip())
                s3 = float(self.Score3_lineEdit.text().strip())
                s4 = float(self.Score4_lineEdit.text().strip())
                self.validating(s1,s2,s3,s4)
                self.read(student,s1,s2,s3,s4)
            self.hiding(4)
            self.clearing()
            self.Outcome_label.setText("Submitted Student Scores")
            self.Outcome_label.setStyleSheet('color: green;')
            self.Next_Button.setEnabled(True)
            self.Attempts_lineEdit.setEnabled(True)
            self.Submit_Button.setEnabled(False)

        except NameError:
            self.Outcome_label.setText("Student already entered")
            self.Outcome_label.setStyleSheet("color: red;")
        except ValueError:
            self.Outcome_label.setText("Enter appropriate score(s) [0-100]")
            self.Outcome_label.setStyleSheet("color: red;")
