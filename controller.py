import constants
import os
import configparser
from database import db
from web_modules.scraper import Scraper

class Controller:

    ############   CONFIG FILE METHODS     ###################
    @staticmethod
    def read_config():
        ''' Create a config object from the config.ini file
        :return: The config.ini file as a ConfigParser object
        '''
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config
    

    @staticmethod
    def update_config(key, value):
        ''' Updated a key value pair in the config.ini file
        :para key: Name of the key in the config.ini file
        :para value: The value to set for the key in the config.ini file'''
        config = Controller.read_config()
        config['SETUP'][key] = value
        with open('config.ini', 'w') as cf:
            config.write(cf)


    @staticmethod
    def is_initial():
        '''Checks the config.ini file to see if this is the first time loading
        :returns: True is initial_load == True, False if not'''
        config = Controller.read_config()
        if config['SETUP']['initial_load'] == 'True':
            return True
        return False
    
        
    @staticmethod
    def get_local_addon_path_config():
        '''Used to retrieve the local addon path from the config.ini file
        :return: The path to the local Addons folder as a string'''
        config = Controller.read_config()
        return config['SETUP']['local_addon_path']
    

    @staticmethod
    def get_constants():
        '''Used to send the contants data to the GUI
        :returns: the constants data'''
        return constants

    ####################   LOCAL ADDON METHODS    ##############################
    @staticmethod
    def get_downloads_dir():
        '''Creates a path object from the local user profile path plus their downloads folder
        :return: the path to the local users downloads folder'''
        return os.path.join(os.getenv('USERPROFILE'), 'Downloads')
    
    @staticmethod
    def find_local_addon_folder():
        '''Attempts to find a "Addons" folder in the users documents or onedrive/documnets folder
        :returns: the path to the local Addons folder or an empty string if not found '''
        user_base_path = os.getenv('USERPROFILE')
        doc_addons_path = os.path.join('Documents', 'Elder Scrolls Online', 'live', 'Addons')
        full_local_addons_path = ""
        if os.path.isdir(os.path.join(user_base_path, doc_addons_path)):
            full_local_addons_path = os.path.join(user_base_path, doc_addons_path)
            Controller.update_config('local_addon_path', full_local_addons_path)
        elif os.path.isdir(os.path.join(user_base_path, 'OneDrive', doc_addons_path)):
            full_local_addons_path = os.path.join(user_base_path, 'OneDrive', doc_addons_path)
            Controller.update_config('local_addon_path', full_local_addons_path)

        return full_local_addons_path


    @staticmethod
    def get_local_addon_dirs():
        '''Used to get all local addon folder names
        :returns: A list of all locally installed addon folder names '''
        return os.listdir(Controller.get_local_addon_path_config())

    @staticmethod
    def get_addon_version(addon_name):
        '''Used to get the version of the locally installed addon. 
            The addon folder will normally have the same name as the txt info file that contains the version
        :returns: The version number as a string'''
        path = os.path.join(Controller.get_local_addon_path_config(), addon_name,  (addon_name + ".txt"))
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                if "## Version" in line:
                    line = line.split(":")
                    return line[1].strip()

    @staticmethod
    def find_local_addons():
        for name in Controller.get_local_addon_dirs():
            try:
                version = Controller.get_addon_version(name)
            except Exception as e:
                version = f"{name} threw Exception: {e}"
            db.insert_local_addon((name, version))

    ##############################   DB METHODS   ######################################
    @staticmethod
    def create_initial_db():
        '''Creates the database and tables if they do not exist
        :return: True if there was no exception thrown, False otherwise'''
        try:
            db.create_connection()
            db.create_tables()
            return True
        except Exception as e:
            return False 

    @staticmethod
    def rebuild_local_addons_table():
        db.rebuild_local_table()
    
    @staticmethod
    def get_local_db_addons():
        return db.get_all_local_addons()

    @staticmethod
    def get_web_db_addons():
        return db.get_all_web_addons()

    @staticmethod
    def add_correction_to_db(local_name, web_name):
        db.insert_correction(local_name, web_name)
    # @staticmethod
    # def get_matching_addons(local_addons_list):
    #     found_list = []
    #     all_db_addons = Controller.get_all_addons()
    #     for local_addon in local_addons_list:
    #         search_name = Controller.create_search_name(local_addon)
    #         try:
    #             result = db.get_one_addon('search_name', search_name)
    #             if len(result) == 1:
    #                 found_list.append(result[0])
    #             else:
    #                 found_list.append(Controller.try_match(search_name, all_db_addons))
    #         except Exception as e:
    #             print(f"There was an exception: {e} on {search_name}")
    #     return found_list


    # @staticmethod
    # def get_unmatched_addons(local_addons_list):
    #     not_found = []
    #     for local_addon in local_addons_list:
    #         search_name = Controller.create_search_name(local_addon)
    #         try:
    #             result = db.get_one_addon('search_name', search_name)
    #             if result == None:
    #                 not_found.append(search_name)
    #         except Exception as e:
    #             print(f"There was an exception: {e} on {search_name}")
    #     return not_found


    # @staticmethod
    # def update_addon_info(search_field, search_name, update_field, new_data):
    #     if db.update_one_addon(search_field, search_name, update_field, new_data):
    #         return "Record was updated"
    #     return "There was a problem updating the search_name"

    # @staticmethod
    # def get_all_addons():
    #     return db.get_all_addons()

    # @staticmethod
    # def set_all_to_uninstalled():
    #     db.set_all_to_uninstalled()

   ########################  SCRAPER METHODS   ##########################

    @staticmethod
    def get_scraper():
        return Scraper()


    @staticmethod
    def get_current_addon_version(name, scraper):
        addon_info = db.get_one_addon('search_name', name)
        print(addon_info[0])
        return scraper.scrape_single_addon_version(addon_info[0])


    ##########################   NAME MATCHING METHODS   ############################
    @staticmethod
    def list_lower(list_to_lower):
        return [x.lower() for x in list_to_lower]
    

    @staticmethod
    def get_matching_list():
        db.preform_correction()
        local_addons = db.get_all_local_addons()
        web_addons = db.get_all_web_addons()
        matched_list = []
        for addon in local_addons:
            esoui_id, web_name = Controller.try_match(addon[1], web_addons)
            matched_list.append((esoui_id, web_name, addon[1]))
        return matched_list
  
            
    @staticmethod
    def _get_match_score(addon_name, name_to_search):
        '''Compares two names and derives a score of how close they are
        :param addon_name: The name of the local addon
        :param name_to_search: An addon name from the website
        :return: A score of how closely the two names matched
        '''
        if addon_name in name_to_search and len(addon_name) == len(name_to_search):
            return 100 # 100% match :)
        name_to_search_list = list(name_to_search)
        matched_count = 0
        for char in list(addon_name):
            if char in name_to_search_list:
                name_to_search_list.pop(name_to_search_list.index(char))
                matched_count += 1
                
        return matched_count - len(name_to_search_list)


    @staticmethod
    def try_match(name, all_addons_list):
        '''Attempts to find a addon from the list that most closly matches name
        :param name: The name of the local addon folder.
        :param all_addons_list: A full list of addon names for the website
        :return: The name of the closest match from the web_addons (highest score wins)
        '''
        match = (0, 0)
        for index, addon in enumerate(all_addons_list):
            score = Controller._get_match_score(name, addon[1])
            if index == 0:
                match = (score, index)
            elif score > match[0]:
                    match = (score, index)
        return all_addons_list[match[1]]