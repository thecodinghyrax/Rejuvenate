import unittest
import configparser
from controller import Controller


class TestControllerEstablished(unittest.TestCase):
    # def setUp(self):
    #     config = configparser.ConfigParser()

    #     return self.something

    # def tearDown(self):
    #     del self.something

    def test_is_initial(self):
        '''This test will only pass after I've ran this app once'''
        # Arrange
        expected = False
        # Act
        actual = Controller.is_initial()
        # Assert
        self.assertEqual(expected, actual)

    def test_get_local_addon_path_config(self):
        '''This test will only pass after I've ran this app once'''
        # Arrange
        expected = 'C:/Users/drewc/OneDrive/Documents/Elder Scrolls Online/live/AddOns1'
        # Act
        actual = Controller.get_local_addon_path_config()
        # Assert
        self.assertEqual(expected, actual)


    def run_tests(self):
        unittest.main(self)


if __name__ == '__main__':
    unittest.main()