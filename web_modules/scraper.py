from bs4 import BeautifulSoup
import requests
import constants
from web_modules.catagory import Catagory
from database import db



class Scraper:
    def __init__(self):
        self._catatories_list = []
        self._addons = []
 
    def parse_page(self, link):
        '''Creates a BS4 object from the supplied link
        :link: The page link to parse
        :returns: A parsed BeautifulSoup object of the page
        '''
        link_page = requests.get(link)
        page = BeautifulSoup(link_page.content, 'html.parser')
        return page
    

    def _get_catagories(self):
        '''Gets all ESOUI addon catagories from the website
        :returns: A unique list of tuples of all addon catagories names and links 
        '''
        downloads_page = self.parse_page(constants.ESOUI_HOME)
        catagories = set()
        for anchor in downloads_page.find_all('a'):
            if "/cat" in str(anchor) and anchor.text != "":
                link = str(anchor).split('"')[1]
                name = anchor.text
                catagories.add((name, link))

        return list(catagories)


    def _create_all_catagories(self):
        '''Creates a Catagory object for each catagory found on the ESOUI website
        and then adds those objects to the catagories_list of this Scraper instances
        :return: Trun for no real reason
        #refactor'''
        catagories_list = []
        catagories = self._get_catagories()
        for catagory in catagories:
            catagories_list.append(Catagory(catagory[0], catagory[1], self))
        self._catatories_list = catagories_list
        return True
        
        
    def _create_all_addons(self, catagories_list):
        ''' Uses the list of Catagory objects to extract all addons found on
        ESOUI.com and save them to the addons list of this Scraper instance 
        :param catagories_list: List of Catagory objects
        :return: True for no real reason
        '''
        addons = []
        for item in catagories_list:
            catagory_addons = item.get_all_addons()
            for addon in catagory_addons:
                addons.append(addon)
        self._addons = addons
        return True

    def scrape_all_to_db(self):
        '''This is the method used to create the catagory and addon lists and then
            write them to the database. This will take a while to run
        :return: List of addons that did not make it to the db
        '''
        self._create_all_catagories()
        self._create_all_addons(self._catatories_list)
   
        skipped_addons = []
        ids = []
        for addon in self._addons:
            id = addon.get_esoui_id()
            try:
                # Remmoving duplicates here. Some addon exist in multiple catagories
                if id in ids:
                    continue
                ids.append(id)
                db.insert_web_addon(addon.get_addon_tuple())
            except Exception as e:
                skipped_addons.append(addon)
                print(f"Failed calling db.insert_web_addon(addon.get_addon_tuple(): {e}")
        return skipped_addons


    def scrape_single_addon_version(self, esoui_id):
        '''Retrieves the version information for an addon on the ESOUI website
        :param esoui_id: The ESOUI Id found in the database
        :return: The text from the version div found on the ESOUI website
        '''
        link = constants.ADDON_INFO_TEMPLATE.replace('<id>', esoui_id)
        addon_page = self.parse_page(link)
        version = addon_page.find(id='version').text
        return version.split(': ')[1]


    def download_addon(self, esoui_id, local_addon_name, downloads_dir):
        '''Downloads the current addon folder from ESOUI.com as a zip file
        :param esoui_id: The id for the addon to download
        :param local_addon_name: The local name of the addon
        :param downloads_dir: The user Downloads directory path
        :retrun: "ok" if it doesn't blow up'''
        out_file_name = f"{downloads_dir}\\{local_addon_name}.zip"
        url = constants.DOWNLOADS_TEMPLATE.replace('<id>', esoui_id)
        with requests.get(url, stream=True) as r:
            with open(out_file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    f.write(chunk)
        return "ok"


# local_filename = 'c:\\Users\\drewc\\downloads\\' + file_name + '.zip'
# download_addon(url, local_filename)    

    def __repr__(self):
        return "Scraper"
