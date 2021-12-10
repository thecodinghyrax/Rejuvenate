import unittest
import configparser
from controller import Controller
import constants


###########################
# https://youtu.be/_OyuFg9pGQg
#############################
# MOCK.PATCH INFO
############################

class TestController(unittest.TestCase):
    # def setUp(self):
    #     config = configparser.ConfigParser()

    #     return self.something

    # def tearDown(self):
    #     del self.something

    def test_get_constants(self):
        # Arrange
        expected = constants
        # Act
        actual = Controller.get_constants()
        # Assert
        self.assertEqual(expected, actual)

    def test_get_downloads_dir(self):
        # Arrange
        expected = 'C:\\Users\\drewc\\Downloads'
        # Act
        actual = Controller.get_downloads_dir()
        # Assert
        self.assertEqual(expected, actual)

    def run_tests(self):
        unittest.main(self)


if __name__ == '__main__':
    unittest.main()