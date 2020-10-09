import pytest
import json

import System
import Student

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
    password2 = "imoutofpasswordnames   "
    password3 = "   imoutofpasswordnames"

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
    beforeGrade = 22
    afterGrade = 50

    grading_system.login(staffName, staffPassword)
    grading_system.usr.change_grade(studentName, course, assignment, afterGrade)

    with open("Data/users.json") as f:
        users = json.load(f)

    assert users[studentName]['courses'][course][assignment]['grade'] == afterGrade

# 4. create_assignment Staff.py
# This function allows the staff to create a new assignment. Verify that an assignment is created with the correct due date in the correct course in the database.


# 5. add_student - Professor.py
# This function allows the professor to add a student to a course. Verify that a student will be added to the correct course in the database.

# 6. drop_student Professor.py
# This function allows the professor to drop a student in a course. Verify that the student is added and dropped from the correct course in the database.

# 7. submit_assignment - Student.py
# This function allows a student to submit an assignment. Verify that the database is updated with the correct assignment, submission, submission dateand in the correct course.

# 8. check_ontime - Student.py
# This function checks if an assignment is submitted on time. Verify that it will return true if the assignment is on time, and false if the assignment is late.

# 9. check_grades - Student.py
# This function returns the users grades for a specific course. Verify the correct grades are returned for the correct user.

# 10. view_assignments - Student.py
# This function returns assignments and their due dates for a specific course. Verify that the correct assignments for the correct course are returned.


@pytest.fixture
def grading_system():
    gs = System.System()
    gs.load_data()
    return gs