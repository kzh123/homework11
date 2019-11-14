"""
summarize student and instructor data
@author:10456094
"""

from HW08_Zihao_Kang import file_reading_gen
from collections import defaultdict
from prettytable import PrettyTable
import os as os
import sqlite3


class Repository:
    """hold the students, instructors and grades for a single University"""

    def __init__(self, dir_path, print_pt=False):
        """read all the things from all the place"""

        self.grade_course_cwid, self.grade_course_student = Grades(
            os.path.join(dir_path, 'grades.txt')).cwid_course_student()
        """ {course:ins_CWID}        {course:students number(int)}"""
        self.instructor_dict = Instructor(os.path.join(dir_path, 'instructors.txt')).instructor_dict_CW()
        """ {CWID:[name:DEPT]}"""

        self.student_dict = Student(os.path.join(dir_path, 'students.txt')).student_dict_CW()
        """{CWID:[name,DEPT]}"""
        self.student_id_course_dict = Grades(os.path.join(dir_path, 'grades.txt')).student_id_course()
        """{CWID:[course1,course2...]}"""

        self.major_R_dict = Major(os.path.join(dir_path, 'majors.txt')).major_required()
        self.major_E_dict = Major(os.path.join(dir_path, 'majors.txt')).major_elective()

        self.pt_instructors = PrettyTable(field_names=['CWID', "Name", "Dept", "Course", "Students"])
        self.pt_student = PrettyTable(
            field_names=["CWID", "Name", "Major", "Completed Courses", "Remaining Required", "Remaining Elective"])
        self.pt_major = PrettyTable(field_names=["DEPT", "Required", "Electives"])
        self.pt_instructors_db = PrettyTable(field_names=['CWID', "Name", "Dept", "Course", "Students"])

        self.print_instructor_pt()
        self.print_student_pt()
        self.print_major_pt()
        self.instructor_table_db('810_startup.db')

        if print_pt:
            print("Instructor Summary")
            print(self.pt_instructors)
            print("Student Summary")
            print(self.pt_student)
            print("Major Summary")
            print(self.pt_major)
            print("Instructor Summary(database)")
            print(self.pt_instructors_db)

    def print_instructor_pt(self):
        """
        dict:
        Course(key):CWID-name-DEPT-student
        """
        instructor_dict_pt = dict()
        for key, value in self.grade_course_cwid.items():
            try:
                instructor_dict_pt.update(
                    {key: {'CWID': value, 'name': self.instructor_dict[value][0],
                           'DEPT': self.instructor_dict[value][1],
                           'student': self.grade_course_student[key]}})
            except KeyError:

                print("Data conflict in multiple data")

        for key, value in instructor_dict_pt.items():
            self.pt_instructors.add_row([value['CWID'], value['name'], value['DEPT'], key, value['student']])

    def print_student_pt(self):
        """print student pretty table"""

        for key, value in self.student_dict.items():
            try:
                self.pt_student.add_row([key, value[0], value[1], self.student_id_course_dict[key],
                                         None if len(set(self.major_R_dict[value[1]]) - set(
                                             self.student_id_course_dict[key])) < 1
                                         else sorted(set(self.major_R_dict[value[1]]) - set(self.student_id_course_dict[key])),
                                         None if len(set(self.major_E_dict[value[1]]) - set(
                                             self.student_id_course_dict[key])) < 2
                                         else sorted(set(self.major_E_dict[value[1]]) - set(self.student_id_course_dict[key]))])
            except KeyError:
                print("Data conflict in multiple data")

    def print_major_pt(self):
        """print major pretty table"""

        for key, value in self.major_R_dict.items():
            try:
                self.pt_major.add_row([key, value, self.major_E_dict[key]])
            except KeyError:
                print("Data conflict in multiple data")

    def instructor_table_db(self, db_path):
        try:
            db_instructor = sqlite3.connect(db_path)
        except sqlite3.OperationalError:
            print("Can not open the database!")

        for row in db_instructor.execute('select InstructorCWID, Name, Dept, Course, count(g.StudentCWID) as StudentsNumber\
                                    from instructors i\
                                        join grades g\
                                             on i.CWID = g.InstructorCWID\
                                                    group by g.Course, g.InstructorCWID'):
            self.pt_instructors_db.add_row(row)
        return self.pt_instructors_db


class Student:
    """hold all of the details of a student"""

    def __init__(self, path):
        """read file"""
        try:
            self.student_list = list(file_reading_gen(path, 3, sep='\t', header=True))
        except ValueError:
            """can be changed in future homework"""
            print("Dirty data in students.txt")
        except FileNotFoundError:
            """Data not found"""
            print("Can not found students.txt")

        self.student_dict = defaultdict(dict)

    def student_dict_CW(self):
        """CWID(key)-name-DEPT"""
        for item in self.student_list:
            self.student_dict.update({item[0]: [item[1], item[2]]})
        return self.student_dict


class Instructor:
    """hold all of the details of an instructor"""

    def __init__(self, path):
        """read file"""
        try:
            self.instructor_list = list(file_reading_gen(path, 3, sep='\t', header=True))
        except ValueError:
            """can be changed in future homework"""
            print("Dirty data in instructor.txt")
        except FileNotFoundError:
            """Data not found"""
            print("Can not found instructor.txt")

        self.instructor_dict = defaultdict(dict)

    def instructor_dict_CW(self):
        """CWID(key)-name-DEPT"""
        for item in self.instructor_list:
            self.instructor_dict.update({item[0]: [item[1], item[2]]})
        return self.instructor_dict


class Grades:
    """info from grades.txt"""

    def __init__(self, path):
        try:
            self.grade_list_pre = list(file_reading_gen(path, 4, sep='\t', header=True))
        except ValueError:
            """can be changed in future homework"""
            print("Dirty data in grades.txt")
        except FileNotFoundError:
            """Data not found"""
            print("Can not found grades.txt")

        self.grade_list = [item for item in self.grade_list_pre if item[2] not in ['D', 'E', 'F']]

    def cwid_course_student(self):
        """return ins_cwid-course and course-student(number) dict"""
        ins_cwid_course_dict = defaultdict(str)
        course_student_dict = defaultdict(int)

        for item in self.grade_list:
            ins_cwid_course_dict[item[1]] = (item[3])
            course_student_dict[item[1]] += 1

        return ins_cwid_course_dict, course_student_dict

    def student_id_course(self):
        """CWID(stu)-course"""
        student_id_course_dict = defaultdict(list)
        for item in self.grade_list:
            student_id_course_dict[item[0]].append(item[1])

        return student_id_course_dict


class Major:
    """info from major.txt"""

    def __init__(self, path):
        try:
            self.major_list = list(file_reading_gen(path, 3, sep='\t', header=True))
        except ValueError:
            """Dirty data"""
            print("Dirty data in majors.txt")
        except FileNotFoundError:
            """Data not found"""
            print("Can not found majors.txt")

    def major_required(self):
        """return required courses for every major"""
        major_required_dict = defaultdict(list)
        for major, RE, course in self.major_list:
            if RE == 'R':
                major_required_dict[major].append(course)

        return major_required_dict

    def major_elective(self):
        """return required courses for every major"""
        major_elective_dict = defaultdict(list)
        for major, RE, course in self.major_list:
            if RE == 'E':
                major_elective_dict[major].append(course)

        return major_elective_dict


if __name__ == '__main__':
    try:
        stevens = Repository('./', print_pt=True)
    except AttributeError:
        print("Please check the file or make sure the path is right!")
