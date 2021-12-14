import os
from zipfile import ZipFile
import os.path
import shutil


class FileOps:
    def __init__(self, addons_path, downloads_path):
        self.addons_path = addons_path.replace("/", "\\")
        self.downloads_path = downloads_path
        

    def unzip_to_addons_dir(self, addon):
        '''Unzips the new addon from the downloads folder into the addon folder
        :param addon: A addon tuple like (id, local_name, web_name, local_vesion, web_version)
                    that was downloaded from ESOUI.com
        :retrun: True if successful, else False'''
        addon_zip = os.path.join(self.downloads_path, (addon + ".zip"))
        # addons_path = os.path(self.addons_path)
        local_addon_folder = os.path.join(self.addons_path, addon)
        self._delete_old_files(local_addon_folder)
        if os.path.isfile(addon_zip):
            with ZipFile(addon_zip, 'r') as zipObj:
                zipObj.extractall(path=self.addons_path)
            self._delete_old_files(addon_zip)
            return True
        return False
        

    def _delete_old_files(self, path):
        '''Deletes the unneeded files or folers
        :param path: The path to the file or folder'''
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            else:
                raise Exception(IOError)
        except Exception as e:
            print(f"Addon was not deleted: {e}")

            
if __name__ == '__main__':
    pass