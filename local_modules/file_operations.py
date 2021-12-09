import os
from zipfile import ZipFile
import os.path
'''
Th3 unzip_to_addons_dir works however, it does not update the date the folder
was modified due to the name being the same. The contents do get updated though.
Next need to delete the zip folders in the downloads and call it good (I think) :D
'''

class FileOps:
    def __init__(self, old_addons, addons_path, downloads_path):
        self.old_addons = old_addons
        self.addons_path = addons_path
        self.downloads_path = downloads_path
        
        


    def unzip_to_addons_dir(self, addon):
        addon_zip = os.path.join(self.downloads_path, (addon + ".zip"))
        with ZipFile(addon_zip, 'r') as zipObj:
            zipObj.extractall(path=self.addons_path)
            
            
            
    def check_config(self):
        print(f"old_addons = {self.old_addons}")
        print(f"addons_path = {self.addons_path}")
        print(os.path.join(self.downloads_path, 'LibPhinixFunctions.zip'))
        print(f"downloads_path = {self.downloads_path}")
            
if __name__ == '__main__':
    old_addons = [('2298', 'LibPhinixFunctions', '', '1.0.16', '1.0.16')]
    addons_path = r'C:\Users\drewc\OneDrive\Documents\Elder Scrolls Online\live\AddOns1'
    downloads_path = r'C:\Users\drewc\Downloads'
    f = FileOps(old_addons, addons_path, downloads_path)
    f.check_config()
    f.unzip_to_addons_dir('LibPhinixFunctions')