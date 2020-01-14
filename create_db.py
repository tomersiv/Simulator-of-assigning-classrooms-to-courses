import sqlite3
import sys
import os;
def main(args):
    databaseexisted = os.path.isfile('schedule.db')
    dbcon = sqlite3.connect('schedule.db')
    with dbcon:
        cursor = dbcon.cursor()
        if not databaseexisted:  # First time creating the database. Create the tables
            cursor.execute("CREATE TABLE courses(ID INTEGER PRIMARY KEY, course_name TEXT NOT NULL, student TEXT NOT NULL, number_of_students INTEGER NOT NULL, class_id INTEGER REFERENCES classrooms(id), course_length INTEGER NOT NULL )")# create table students
            cursor.execute("CREATE TABLE students(grade TEXT PRIMARY KEY, count INTEGER NOT NULL )")  # create table students
            cursor.execute("CREATE TABLE classrooms(id INTEGER PRIMARY KEY , location TEXT NOT NULL, current_course_id INTEGER NOT NULL, current_course_time_left INTEGER NOT NULL )")
            configFile=args[1];
            with open(configFile) as config:
                for line in config:
                    lineByPsik=line.split(',')
                    # cut the /n and the revah from the start and end of the word
                    fixedLineByPsik = [item.strip() for item in lineByPsik]
                    tableName=fixedLineByPsik[0]
                    if(tableName=="S"):
                        cursor.execute("INSERT INTO students VALUES(?,?)", (fixedLineByPsik[1], int (float(fixedLineByPsik[2]))))
                    if(tableName=="C"):
                        cursor.execute("INSERT INTO courses VALUES(?,?,?,?,?,?)", (int (float(fixedLineByPsik[1])), fixedLineByPsik[2],fixedLineByPsik[3],int (float(fixedLineByPsik[4])),int (float(fixedLineByPsik[5])),int (float(fixedLineByPsik[6])) ))
                    if(tableName=="R"):
                        cursor.execute("INSERT INTO classrooms VALUES(?,?,?,?)", (int (float(fixedLineByPsik[1])),fixedLineByPsik[2],0,0))
            cursor.execute("SELECT * FROM courses");
            coursesList = cursor.fetchall()
            print("courses")
            print_table(coursesList)
            cursor.execute("SELECT * FROM classrooms");
            classroomList = cursor.fetchall()
            print("classrooms")
            print_table(classroomList)
            cursor.execute("SELECT * FROM students");
            studentsList = cursor.fetchall()
            print("students")
            print_table(studentsList)


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)

if __name__ == '__main__':
    main(sys.argv)

