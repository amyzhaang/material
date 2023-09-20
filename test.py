import unittest
from file_system import FileSystem

class FileSystemTest(unittest.TestCase):

    def test_make_dir_and_change_current(self):
        test = FileSystem()

        test.make_directory("school")
        test.change_directory("school")
        self.assertEqual(test.get_working_directory(), "/school")

        test.make_directory("homework")
        self.assertEqual(test.get_working_directory(), "/school")
        test.change_directory("homework")
        self.assertEqual(test.get_working_directory(), "/school/homework")

    def test_example_in_assignment(self):
        test = FileSystem()

        test.make_directory("school")
        test.change_directory("school")
        self.assertEqual(test.get_working_directory(), "/school")

        test.make_directory("homework")
        test.change_directory("homework")
        test.make_directory("math")
        test.make_directory("lunch")
        test.make_directory("history")
        test.make_directory("spanish")
        test.remove("lunch")
        self.assertCountEqual(test.get_working_directory_contents(), ["math", "history", "spanish"])
        self.assertEqual(test.get_working_directory(), "/school/homework")

        test.change_directory_to_parent()
        test.make_directory("cheatsheet")
        self.assertCountEqual(test.get_working_directory_contents(), ["homework", "cheatsheet"])

        test.remove("cheatsheet")
        test.change_directory_to_parent()
        self.assertEqual(test.get_working_directory(), "/")

    def test_make_file(self):
        test = FileSystem()

        test.make_file("assignment")
        test.write_file_contents("assignment", "problem 1")

        self.assertEqual(test.get_file_contents("assignment"), "problem 1")

    def test_move_file(self):
        test = FileSystem()
        test.make_directory("homework")
        test.change_directory("homework")

        test.make_directory("math")
        test.make_directory("science")
        test.change_directory("math")
        test.make_file("assignment")

        test.move_file("assignment", "/homework/science")

        self.assertCountEqual(test.get_working_directory_contents(), [])
        test.change_directory_to_parent()
        test.change_directory("science")
        self.assertCountEqual(test.get_working_directory_contents(), ["assignment"])

    def test_move_file_collision(self):
        test = FileSystem()
        test.make_directory("math")
        test.change_directory("math")
        test.make_file("hw")

        test.change_directory_to_parent()
        test.make_directory("science")
        test.change_directory("science")
        test.make_file("hw")

        test.move_file("hw", "/math")

        self.assertCountEqual(test.get_working_directory_contents(), [])
        test.change_directory_to_parent()
        test.change_directory("math")
        self.assertCountEqual(test.get_working_directory_contents(), ["hw", "hw_2"])

    def test_move_dir(self):
        test = FileSystem()
        test.make_directory("school")
        test.make_directory("work")
        test.change_directory("school")
        test.make_directory("taxes")
        test.change_directory("taxes")
        test.make_file("w2")
        test.change_directory_to_parent()

        test.move_directory("taxes", "/work")

        self.assertCountEqual(test.get_working_directory_contents(), [])
        test.change_directory_to_parent()
        self.assertCountEqual(test.get_working_directory_contents(), ["school", "work"])
        test.change_directory("work")
        self.assertCountEqual(test.get_working_directory_contents(), ["taxes"])
        test.change_directory("taxes")
        self.assertCountEqual(test.get_working_directory_contents(), ["w2"])

    def test_move_dir_collision(self):
        test = FileSystem()
        test.make_directory("work")
        test.change_directory("work")
        test.make_directory("taxes")
        test.change_directory("taxes")
        test.make_file("paystub")
        test.change_directory_to_parent()
        test.change_directory_to_parent()
        self.assertEqual(test.get_working_directory(), "/")

        test.make_directory("school")
        test.change_directory("school")
        test.make_directory("taxes")
        test.change_directory("taxes")
        test.make_file("w2")
        test.change_directory_to_parent()
        self.assertEqual(test.get_working_directory(), "/school")

        test.move_directory("taxes", "/work")

        self.assertEqual(test.get_working_directory(), "/school")
        self.assertCountEqual(test.get_working_directory_contents(), [])
        test.change_directory_to_parent()
        self.assertEqual(test.get_working_directory(), "/")
        self.assertCountEqual(test.get_working_directory_contents(), ["school", "work"])
        test.change_directory("work")
        self.assertCountEqual(test.get_working_directory_contents(), ["taxes"])
        test.change_directory("taxes")
        self.assertCountEqual(test.get_working_directory_contents(), ["w2", "paystub"])

    def test_move_dir_and_file_collision(self):
        test = FileSystem()
        test.make_directory("work")
        test.change_directory("work")
        test.make_directory("taxes")
        test.change_directory("taxes")
        test.make_file("paystub")
        test.change_directory_to_parent()
        test.change_directory_to_parent()
        self.assertEqual(test.get_working_directory(), "/")

        test.make_directory("school")
        test.change_directory("school")
        test.make_directory("taxes")
        test.change_directory("taxes")
        test.make_file("paystub")
        test.change_directory_to_parent()
        self.assertEqual(test.get_working_directory(), "/school")

        test.move_directory("taxes", "/work")

        self.assertEqual(test.get_working_directory(), "/school")
        self.assertCountEqual(test.get_working_directory_contents(), [])
        test.change_directory_to_parent()
        self.assertEqual(test.get_working_directory(), "/")
        self.assertCountEqual(test.get_working_directory_contents(), ["school", "work"])
        test.change_directory("work")
        self.assertCountEqual(test.get_working_directory_contents(), ["taxes"])
        test.change_directory("taxes")
        self.assertCountEqual(test.get_working_directory_contents(), ["paystub", "paystub_2"])

if __name__ == '__main__':
    unittest.main()
