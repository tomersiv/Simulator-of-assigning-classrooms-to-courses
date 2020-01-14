import sqlite3
import sys
import os;

dbcon = None
scheduleExisted = os.path.isfile('schedule.db')
dbcon = sqlite3.connect('schedule.db')


def assign_newcourse(id, loc, iterNum):
    cursor = dbcon.cursor()
    cursor.execute(" SELECT * FROM courses WHERE class_id=(?)", (id,))
    course = cursor.fetchone()
    if (course != None):
        print('(' + iterNum.__str__() + ') ' + loc + ': ' + course[1] + ' is schedule to start')
        cursor = dbcon.cursor()
        #Update classroom column
        cursor.execute('UPDATE classrooms SET current_course_id={},current_course_time_left={} where id={}'
                       .format(course[0], course[5], course[4]))
        #Updating student ammount
        update_studentammount(course[2], course[3])


def update_studentammount(grade, decreaseammount):
    cursor = dbcon.cursor()
    cursor.execute("SELECT count  FROM students  WHERE grade=(?)", (grade,))
    Studentnum = cursor.fetchone()[0]
    #Ensuring a positive number of students
    if (decreaseammount <= Studentnum):
        cursor = dbcon.cursor()
        cursor.execute(" UPDATE students SET count = (?) WHERE grade = (?) ", (Studentnum - decreaseammount, grade))
        return True
    return False


def delete_course(course_id):
    cursor = dbcon.cursor()
    cursor.execute("DELETE FROM courses WHERE id=(?)", (course_id,))
    cursor.execute(" UPDATE classrooms SET current_course_id = 0 WHERE current_course_id = (?) ", (course_id,))


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


def get_course_name(course_id):
    cursor = dbcon.cursor()
    cursor.execute(" SELECT course_name FROM courses WHERE id =(?)", (course_id,))
    return cursor.fetchone()[0]


def decrease_course(classroom):
    cursor = dbcon.cursor()
    cursor.execute(" UPDATE classrooms SET current_course_time_left = (?) WHERE id = (?) ",
                   (classroom[3] - 1, classroom[0],))


def close_db():
    dbcon.commit()
    dbcon.close()


def main(args):
    if (dbcon != None):
        iternum = 0
        isdone = False
        while scheduleExisted & isdone == False:
            cursor = dbcon.cursor()
            cursor.execute("SELECT * FROM courses")
            courses = cursor.fetchall()
            cursor = dbcon.cursor()
            cursor.execute(" SELECT * FROM classrooms")
            classrooms = cursor.fetchall()
            cursor = dbcon.cursor()
            cursor.execute(" SELECT * FROM students")
            students = cursor.fetchall()
            for classroom in classrooms:
                #Checking if class is free
                if (classroom[2] == 0):
                    assign_newcourse(classroom[0], classroom[1], iternum)
                else:
                    #Checking if course is done
                    if (classroom[3] == 0):
                        print('(' + iternum.__str__() + ') ' + classroom[1] + ' : ' + get_course_name(
                            classroom[2]) + ' is done')
                        delete_course(classroom[2])
                        assign_newcourse(classroom[0], classroom[1], iternum)
                    else:
                        print('(' + iternum.__str__() + ') ' + classroom[1] + ' : occupied by ' + get_course_name(
                            classroom[2]))
            cursor = dbcon.cursor()
            cursor.execute("SELECT * FROM courses")
            courses = cursor.fetchall()
            cursor = dbcon.cursor()
            #Checking if all courses has been deleted from the database
            if (courses.__len__() < 1):
                isdone = True
            cursor = dbcon.cursor()
            cursor.execute("SELECT * FROM courses")
            courses = cursor.fetchall()
            cursor = dbcon.cursor()
            cursor.execute(" SELECT * FROM classrooms")
            classrooms = cursor.fetchall()
            cursor = dbcon.cursor()
            cursor.execute(" SELECT * FROM students")
            students = cursor.fetchall()
            print("courses")
            print_table(courses)
            print("classrooms")
            print_table(classrooms)
            print("students")
            print_table(students)
            iternum = iternum + 1
            for classroom in classrooms:
                if classroom[3] > 0:
                    decrease_course(classroom)
    close_db()


if __name__ == '__main__':
    main(sys.argv)
