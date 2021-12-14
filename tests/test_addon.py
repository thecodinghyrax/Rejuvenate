from web_modules.addon import Addon
import unittest


class TestAddon(unittest.TestCase):
    def setUp(self):
        self.addon = Addon('1234', 'libnotifications')
    
    def tearDown(self):
        del self.addon

    
    def test_get_esoui_id(self):
        # Arrange
        expected = '1234'
        # Act
        actual = self.addon.get_esoui_id()
        # Assert
        self.assertEqual(expected, actual)
        
        
    def test_get_name(self):
        # Arrange
        expected = 'libnotifications'
        # Act
        actual = self.addon.get_name()
        # Assert
        self.assertEqual(expected, actual)
        

    def test_get_addon_tuple(self):
        # Arrange
        expected = ('1234', 'libnotifications')
        # Act
        actual = self.addon.get_addon_tuple()
        # Assert
        self.assertEqual(expected, actual)
        

    def test_display(self):
        # Arrange
        expected = 'ESOUI ID: 1234\nName: libnotifications\n'
        # Act
        actual = self.addon.display()
        # Assert
        self.assertEqual(expected, actual)
        
        
    def test___str__(self):
        # Arrange
        expected = '1234, libnotifications'
        # Act
        actual = self.addon.__str__()
        # Assert
        self.assertEqual(expected, actual)
        
        
    def test___repr__(self):
        # Arrange
        expected = 'Addon(esoui_id=1234, name=libnotifications)'
        # Act
        actual = self.addon.__repr__()
        # Assert
        self.assertEqual(expected, actual)
        
        
    def run_tests(self):
        unittest.main(self)
        
if __name__ == '__main__':
    unittest.main()