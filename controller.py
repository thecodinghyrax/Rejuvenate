import constants
import os
import configparser
from database import db
from web_modules.scraper import Scraper
from local_modules import file_operations

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
        '''Used to send the constants data to the GUI
        :returns: the constants data
        '''
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
        '''Finds all locally installed addons and adds them to the db'''
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
        '''Drops and rebuilds the local_addons table to start fresh'''
        db.rebuild_local_table()
    
    @staticmethod
    def get_local_db_addons():
        '''Gets all local addons from the db
        :return: All addons from the db as (esoui_id,folder_name,web_name,local_version,web_version)'''
        return db.get_all_local_addons()
    
    @staticmethod
    def get_addons_to_check():
        '''Gets all locally install addons. Used for checking the curent versions
        :return: All locally installed addons as (folder_name,local_version,web_version,esoui_id)'''
        return db.get_addons_to_check()

    @staticmethod
    def get_web_db_addons():
        '''Gets all addons listed on the website from the db
        :retruns: Add web addons as (esoui_id,name)'''
        return db.get_all_web_addons()

    @staticmethod
    def add_correction_to_db(local_name, web_name):
        '''Add the user defined matching local and web addon names to the db'''
        db.insert_correction(local_name, web_name)


   ########################  SCRAPER METHODS   ##########################

    @staticmethod
    def get_scraper():
        '''Returns an instance of the Scraper class for the GUI'''
        return Scraper()

    
    @staticmethod
    def check_for_updates(local_addons, scraper):
        '''Grabs the current version of each installed addon and updates the db
        :param local_addons: A list of tuples like (local_addon_name, esoui_id)
        :param scraper: An instance of the scraper object from the GUI
        '''
        for addon in local_addons:
            current_version = scraper.scrape_single_addon_version(addon[1])
            db.update_addon_by_id('local_addon', addon[1], 'web_version', current_version)


    @staticmethod
    def update_all(addons_needing_updates, scraper):
        addon_path = Controller.get_local_addon_path_config()
        downloads_dir = Controller.get_downloads_dir()
        file_ops = file_operations.FileOps(addon_path, downloads_dir)
        download_dir = str(Controller.get_downloads_dir())
        for old_addon in addons_needing_updates:
            scraper.download_addon(old_addon[0], old_addon[1], download_dir)
            db.update_addon_by_id('local_addon', old_addon[0], 'local_version', old_addon[4])
            file_ops.unzip_to_addons_dir(old_addon[1])
        
        
    ##########################   NAME MATCHING METHODS   ############################
    @staticmethod
    def list_lower(list_to_lower):
        '''Takes a list of strings and make all elements lowercase
        :param list_to_lower: A list of strings that needs to be converted to lowercase
        :return: The supplied list coverted to lowercase
        '''
        return [x.lower() for x in list_to_lower]
    

    @staticmethod
    def get_matching_list():
        '''Matches a list of local addons to the addons found on the website.
            Runs the preform_correction method to utilize any user defined changes.
            Adds the esoui_id to the local_addons table'''
        db.preform_correction()
        local_addons = db.get_all_local_addons()
        web_addons = db.get_all_web_addons()
        matched_list = []
        for addon in local_addons:
            if addon[2] == "":
                esoui_id, web_name = Controller.try_match(addon[1], web_addons)
            else:
                esoui_id, web_name = Controller.try_match(addon[2], web_addons)
            
            matched_list.append((esoui_id, web_name, addon[1]))
            db.update_one_addon('local_addon','folder_name', addon[1], 'esoui_id', esoui_id)
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