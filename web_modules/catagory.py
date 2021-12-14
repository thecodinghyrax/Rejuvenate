from constants import ADDON_PAGE_TEMPLATE as template
from web_modules.addon import Addon
import re


class Catagory:
    '''Catagory will represent all information for a single addon catagory'''

    def __init__(self, name, link, scraper):
        ''' Initialize the class 
        :name: The catagory name
        :link: The link to the catagory page
        :scraper: An instance of the Scraper class
        '''
        self.name = name
        self.catagory_link = link
        self.scraper = scraper
        self.catagory_number = self.catagory_link.split("downloads/cat")[1].split(".")[0]
        # Example catagory_link: 'https://www.esoui.com/downloads/cat147.html'
        self.number_of_pages = self.get_number_of_pages()
        self.page_links = self.create_cat_links()
        self.addon_list = self.create_addon_list()


    def get_number_of_pages(self):
        ''' Discovers how many pages of addons are listed for this catagory
        :returns: The number of pages this catagory has. 1 if not found
        '''
        catagory_page = self.scraper.parse_page(self.catagory_link)
        for data in catagory_page.find_all('td'):
            if "Page " in str(data.find(text=True)):
                # Example data: <td class="vbmenu_control" style="font-weight:normal">Page 1 of 4</td>
                return int(data.find(text=True).strip()[-2:])
        return 1


    def create_cat_links(self):
        ''' Creates links for each addon page for this catagory
        :returns: A list of all links to addon pages for this catagory
        '''
        if self.number_of_pages:
            cat = self.catagory_link.split("downloads/cat")[1].split(".")[0]
            pages = []
            for page in range(self.number_of_pages):
                pages.append(template.replace('<cat>', cat).replace('<page>', str(page + 1)))
                # Example page: https://www.esoui.com/downloads/index.php?cid=21&sb=dec_date&so=desc&pt=f&page=1
            return pages


    def create_addon_list(self):
        ''' Creates a list of Addon objects assoicated with this catagory
        :returns: A list of Addon objects for this catagory
        '''
        addons =[]
        for page in self.page_links:
            resuts_page = self.scraper.parse_page(page)
            file_re = re.compile('^file\_[0-9]*')
            for file_div in resuts_page.find_all('div', {"id" : file_re}):
                '''
                Example file_div:
                <div class="file" id="file_3228">
                <div class="preview">
                <a class="lightbox" href="//cdn-eso.mmoui.com/preview/pvw11006.png" rel="filepics" title="Vestige's Epic Quest"><img alt="Click to enlarge." src="//cdn-eso.mmoui.com/preview/tiny/pvw11006.png"/></a></div>
                <div class="title"><div style="float:right;font-size:10px;margin-top:5px">7.2.5</div><a href="fileinfo.php?s=a2d1413d30c0428e2a62afe5e29ca67e&amp;id=3228">Vestige's Epic Quest</a>   <img alt="Updated less than 3 days ago!" border="0" src="//cdn-eso.mmoui.com/images/style_esoui/downloads/updated_3.gif"/> </div>
                <div class="stats">
                <div class="downloads">707 Downloads (674 Monthly) <img alt="" height="11" src="//cdn-eso.mmoui.com/images/style_esoui/downloads/filelist-dlicon.png" width="11"/></div>
                <div class="favorites">6 Favorites <img alt="" height="11" src="//cdn-eso.mmoui.com/images/style_esoui/downloads/filelist-favicon.png" width="11"/></div>
                <div class="updated">Updated 11/25/21 02:03 PM <img alt="" height="11" src="//cdn-eso.mmoui.com/images/style_esoui/downloads/filelist-updatedicon.png" width="11"/></div>
                </div>
                <div class="author">By: Masteroshi430</div>
                </div>
                '''
                id = file_div['id'].split('_')[1]
                # updated_div = file_div.find('div', {"class" : "updated"})
                # updated = updated_div.find(text=True).replace('Updated ', "").strip()
                for link in file_div.find_all('a'):
                    if "fileinfo.php?s" in str(link):
                        addons.append(Addon(id, link.find(text=True)))
        return addons


    def get_all_addons(self):
        ''' Gets all Addon objects for this catagory in a list
        :returns: A list of all addon objects for this catagory
        '''
        return self.addon_list


    def __display__(self):
        ''' Displays the catagory information
        :returns: Human readable information about this catagory
        '''
        return f"Name: {self.name}\nLink: {self.catagory_link}\n" + \
                f"Catagory Number: {self.catagory_number}\nNumber of pages: {self.number_of_pages}\n" +\
                f"Addons: {self.addon_list}\n"


    def __str__(self):
        ''' Displays all catagory information
        :returns: All variables used in this catagory instance
        '''
        return f"{self.name}, {self.catagory_link}, {str(self.scraper)}, " + \
        f"{self.catagory_number}, {self.number_of_pages}, " + \
        f"{self.page_links}, {self.addon_list}"


    def __repr__(self):
        ''' Displays the call to create this Catagory instance
        :returns: Information about how the class was instantiated 
        '''
        return f"Catagory(name={self.name}, link={self.catagory_link}, scraper={repr(self.scraper)}"