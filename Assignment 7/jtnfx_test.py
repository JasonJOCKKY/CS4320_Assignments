import pytest
import json

import System
import Student
import RestoreData

# 1. login - System.py
# The login function takes a name and password and sets the user for the program. Verify that the correct user is created with this test, and use the json files to check that it adds the correct data to the user.
def test_login(grading_system):
    username = "yted91"
    password = "imoutofpasswordnames"
    grading_system.login(username, password)

    with open("Data/users.json") as f:
        users = json.load(f)

    with open("Data/courses.json") as f:
        courses = json.load(f)

    assert grading_system.usr.name == username
    assert grading_system.usr.users == users
    assert grading_system.usr.all_courses == courses
    assert grading_system.usr.courses == users[username]["courses"]
    assert grading_system.usr.password == password
    assert isinstance(grading_system.usr, Student.Student)

# 2. check_password - System.py
# This function checks that the password is correct. Enter several different formats of passwords to verify that the password returns correctly if the passwords are the same.
def test_checkPassword(grading_system):
    username = "yted91"
    password1 = "imoutofpasswordnames"
    password2 = "IMOUTOFPASSWORDNAMES"
    password3 = "imout   ofpasswordnames"

    assert grading_system.check_password(username, password1)
    assert grading_system.check_password(username, password2)
    assert grading_system.check_password(username, password3)

# 3. change_grade - Staff.py
# This function will change the grade of a student and updates the database. Verify that the correct grade is changed on the correct user in the database.
def test_changeGrade(grading_system):
    staffName = "goggins"
    staffPassword = "augurrox"
    course = "software_engineering"
    assignment = "assignment2"
    studentName = "yted91"
    afterGrade = 50

    grading_system.login(staffName, staffPassword)
    grading_system.usr.change_grade(studentName, course, assignment, afterGrade)

    with open("Data/users.json") as f:
        users = json.load(f)
    
    RestoreData.restoreData()

    assert users[studentName]['courses'][course][assignment]['grade'] == afterGrade

# 4. create_assignment Staff.py
# This function allows the staff to create a new assignment. Verify that an assignment is created with the correct due date in the correct course in the database.
def test_createAssignment(grading_system):
    staffName = "goggins"
    staffPassword = "augurrox"
    course = "software_engineering"
    newAssignment = "assignment_jtnfx"
    newDueDate = "9/20/2020"

    grading_system.login(staffName, staffPassword)
    grading_system.usr.create_assignment(newAssignment, newDueDate, course)

    with open("Data/courses.json") as f:
        courses = json.load(f)

    RestoreData.restoreData()

    assert courses[course]['assignments'][newAssignment]['due_date'] == newDueDate

# 5. add_student - Professor.py
# This function allows the professor to add a student to a course. Verify that a student will be added to the correct course in the database.
def test_addStudent(grading_system):
    staffName = "goggins"
    staffPassword = "augurrox"
    course = "software_engineering"
    newStudent = "akend3"

    grading_system.login(staffName, staffPassword)
    grading_system.usr.add_student(newStudent, course)

    with open("Data/users.json") as f:
        users = json.load(f)
    
    RestoreData.restoreData()

    assert course in users[newStudent]['courses']

# 6. drop_student Professor.py
# This function allows the professor to drop a student in a course. Verify that the student is added and dropped from the correct course in the database.
def test_dropStudent(grading_system):
    staffName = "goggins"
    staffPassword = "augurrox"
    course = "software_engineering"
    student = "yted91"

    grading_system.login(staffName, staffPassword)
    grading_system.usr.drop_student(student, course)

    with open("Data/users.json") as f:
        users = json.load(f)
    
    RestoreData.restoreData()

    assert course not in users[student]['courses']

# 7. submit_assignment - Student.py
# This function allows a student to submit an assignment. Verify that the database is updated with the correct assignment, submission, submission date and in the correct course.
def test_submitAssignment(grading_system):
    studentName = "akend3"
    studentPassword = "123454321"
    course = "databases"
    assignment = "assignment1"
    submission = assignment + "resubmission"
    submissionDate = "8/4/2021"

    grading_system.login(studentName, studentPassword)
    grading_system.usr.submit_assignment(course, assignment, submission, submissionDate)

    with open("Data/users.json") as f:
        users = json.load(f)
    
    RestoreData.restoreData()

    assert users[studentName]['courses'][course][assignment]['submission'] == submission
    assert users[studentName]['courses'][course][assignment]['submission_date'] == submissionDate
    

# 8. check_ontime - Student.py
# This function checks if an assignment is submitted on time. Verify that it will return true if the assignment is on time, and false if the assignment is late.
def test_checkOntime(grading_system):
    studentName = "akend3"
    studentPassword = "123454321"
    dueDate = "1/3/2020"
    ontimeSubmissionDate = "1/2/2020"
    lateSubmissionDate = "1/5/2020"

    grading_system.login(studentName, studentPassword)

    assert grading_system.usr.check_ontime(ontimeSubmissionDate, dueDate) == True
    assert grading_system.usr.check_ontime(lateSubmissionDate, dueDate) == False

# 9. check_grades - Student.py
# This function returns the users grades for a specific course. Verify the correct grades are returned for the correct user.
def test_checkGrades(grading_system):
    studentName = "akend3"
    studentPassword = "123454321"
    course = "databases"

    grading_system.login(studentName, studentPassword)
    usrGrades = grading_system.usr.check_grades(course)

    with open("Data/users.json") as f:
        users = json.load(f)
    
    for [assignment, grade] in usrGrades:
        assert grade == users[studentName]['courses'][course][assignment]['grade']


# 10. view_assignments - Student.py
# This function returns assignments and their due dates for a specific course. Verify that the correct assignments for the correct course are returned.
def test_viewAssignments(grading_system):
    studentName = "akend3"
    studentPassword = "123454321"
    course = "databases"

    grading_system.login(studentName, studentPassword)
    usrAssignments = grading_system.usr.view_assignments(course)

    with open("Data/courses.json") as f:
        courses = json.load(f)

    for [assignment, dueDate] in usrAssignments:
        assert dueDate == courses[course]['assignments'][assignment]['due_date']

# Custom tests
# 11. add_student - Professor.py
# A professor should not be able to add a student to the course that he is not teaching.  Verify that the course does not appear on the student's course list.
def test_addStudent_jtnfx(grading_system):
    staffName = "goggins"
    staffPassword = "augurrox"
    course = "comp_sci"
    newStudentName = "yted91"

    grading_system.login(staffName, staffPassword)
    grading_system.usr.add_student(newStudentName, course)

    with open("Data/users.json") as f:
        users = json.load(f)
    
    RestoreData.restoreData()

    assert course not in users[newStudentName]['courses']

# 12. view_assignments - Student.py
# A student can not view assignments from courses that he is not in.  Verify that the function returns nothing.
def test_viewAssignments_jtnfx(grading_system):
    studentName = "akend3"
    studentPassword = "123454321"
    course = "cloud_computing"

    grading_system.login(studentName, studentPassword)
    assert grading_system.usr.view_assignments(course) == []

# 13. change_grade - Staff.py
# Staffs can only change grades in the courses they are teaching.  Verify that the grade remains unchanged.
def test_changeGrade_jtnfx(grading_system):
    staffName = "goggins"
    staffPassword = "augurrox"
    course = "comp_sci"
    student = "akend3"
    assignment = "assignment1"
    newGrade = 57

    with open("Data/users.json") as f:
        users = json.load(f)

    odlGrade = users[student]['courses'][course][assignment]['grade']

    grading_system.login(staffName, staffPassword)
    grading_system.usr.change_grade(student, course, assignment, newGrade)

    with open("Data/users.json") as f:
        users = json.load(f)
    
    RestoreData.restoreData()
    
    assert odlGrade == users[student]['courses'][course][assignment]['grade']

# 14. change_grade - Staff.py
# Grade can not be changed for a student who is not in the course.
def test_changeGrade2_jtnfx(grading_system):
    staffName = "goggins"
    staffPassword = "augurrox"
    course = "software_engineering"
    student = "akend3"
    assignment = "assignment1"
    newGrade = 57

    grading_system.login(staffName, staffPassword)
    grading_system.usr.change_grade(student, course, assignment, newGrade)

# 15. login - System.py
# Test if the system can handle a wrong username
def test_login_jtnfx(grading_system):
    username = "randomName"
    password = "randomPassword"

    grading_system.login(username, password)

@pytest.fixture
def grading_system():
    gs = System.System()
    gs.load_data()
    return gs