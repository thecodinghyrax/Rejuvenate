import unittest
from controller import Controller
import constants


class TestController(unittest.TestCase):

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
        
        
    def test_local_addon_folder(self):
        # Arrange
        expected = "C:\\Users\\drewc\\OneDrive\\Documents\\Elder Scrolls Online\\live\\Addons"
        # Act
        actual = Controller.find_local_addon_folder()
        # Assert
        self.assertEqual(expected, actual)


    def test_list_lower(self):
        # Arrange
        expected = ['car', 'house', 'taco']
        # Act
        actual = Controller.list_lower(['CAR', 'House', 'TaCo'])
        # Assert
        self.assertEqual(expected, actual)


    def test_get_match_score_differnet_names(self):
        # Arrange
        addon_name = "libnotifications"
        name_to_search = 'circonians libnotifications'
        expected = 5
        # Act
        actual = Controller._get_match_score(addon_name, name_to_search)
        # Assert
        self.assertEqual(expected, actual)
        
        
    def test_get_match_score_same_names(self):
        # Arrange
        addon_name = "libnotifications"
        name_to_search = 'libnotifications'
        expected = 100
        # Act
        actual = Controller._get_match_score(addon_name, name_to_search)
        # Assert
        self.assertEqual(expected, actual)
        
        
    def test_try_match_exact_find(self):
        # Arrange 
        name = "drew"
        all_addons_list = ["drew", "bob", "larry", "yoda"]
        expected = "drew"
        # Act 
        actual = Controller.try_match(name, all_addons_list)
        # Assert
        self.assertEqual(expected, actual)
        
        
    def test_try_match_close_find(self):
        # Arrange 
        name = "drew"
        all_addons_list = ["andrew", "bob", "larry", "yoda"]
        expected = "andrew"
        # Act 
        actual = Controller.try_match(name, all_addons_list)
        # Assert
        self.assertEqual(expected, actual)
        
        
    def run_tests(self):
        unittest.main(self)


if __name__ == '__main__':
    unittest.main()