from HW11_Zihao_Kang import Repository
import unittest


class TestRepository(unittest.TestCase):
    def test_HW011(self):
        """test for homework11"""

        self.assertEqual(str(Repository('./', print_pt=False).pt_instructors_db),
                         str("+-------+------------+------+---------+----------+\n\
|  CWID |    Name    | Dept |  Course | Students |\n\
+-------+------------+------+---------+----------+\n\
| 98762 | Hawking, S |  CS  |  CS 501 |    1     |\n\
| 98762 | Hawking, S |  CS  |  CS 546 |    1     |\n\
| 98764 |  Cohen, R  | SFEN |  CS 546 |    1     |\n\
| 98762 | Hawking, S |  CS  |  CS 570 |    1     |\n\
| 98763 | Rowland, J | SFEN | SSW 555 |    1     |\n\
| 98763 | Rowland, J | SFEN | SSW 810 |    4     |\n\
+-------+------------+------+---------+----------+"))

        self.assertEqual(str(Repository('./', print_pt=False).pt_major),
                         str("\
+------+-----------------------------------+------------------------+\n\
| DEPT |              Required             |       Electives        |\n\
+------+-----------------------------------+------------------------+\n\
| SFEN | ['SSW 540', 'SSW 810', 'SSW 555'] |  ['CS 501', 'CS 546']  |\n\
|  CS  |        ['CS 570', 'CS 546']       | ['SSW 810', 'SSW 565'] |\n\
+------+-----------------------------------+------------------------+"))

        self.assertEqual(str("+-------+------------+------+---------+----------+\n\
|  CWID |    Name    | Dept |  Course | Students |\n\
+-------+------------+------+---------+----------+\n\
| 98762 | Hawking, S |  CS  |  CS 501 |    1     |\n\
| 98762 | Hawking, S |  CS  |  CS 546 |    1     |\n\
| 98764 |  Cohen, R  | SFEN |  CS 546 |    1     |\n\
| 98762 | Hawking, S |  CS  |  CS 570 |    1     |\n\
| 98763 | Rowland, J | SFEN | SSW 555 |    1     |\n\
| 98763 | Rowland, J | SFEN | SSW 810 |    4     |\n\
+-------+------------+------+---------+----------+"),
                         str(Repository('./', print_pt=False).pt_instructors_db))

        self.assertEqual(str("+-------+----------+-------+---------------------------------+------------------------+----------------------+\n\
|  CWID |   Name   | Major |        Completed Courses        |   Remaining Required   |  Remaining Elective  |\n\
+-------+----------+-------+---------------------------------+------------------------+----------------------+\n\
| 10103 | Jobs, S  |  SFEN |      ['SSW 810', 'CS 501']      | ['SSW 540', 'SSW 555'] |         None         |\n\
| 10115 | Bezos, J |  SFEN |           ['SSW 810']           | ['SSW 540', 'SSW 555'] | ['CS 501', 'CS 546'] |\n\
| 10183 | Musk, E  |  SFEN |      ['SSW 555', 'SSW 810']     |      ['SSW 540']       | ['CS 501', 'CS 546'] |\n\
| 11714 | Gates, B |   CS  | ['SSW 810', 'CS 546', 'CS 570'] |          None          |         None         |\n\
+-------+----------+-------+---------------------------------+------------------------+----------------------+"),
                         str(Repository('./', print_pt=False).pt_student))

if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
