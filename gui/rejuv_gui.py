import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.font import Font
from tkinter.filedialog import askdirectory, test
from types import NoneType
from PIL import Image, ImageTk
from controller import Controller
import time

class RejuvGUI(tk.Tk):
    # def __init__(self, conn, scraper):
    def __init__(self):

        super().__init__()
        self.geometry("600x600")
        self.resizable(False, False)
        self.configure(background="#333333")
        self.title("Rejuvenate - Addon updater for ESO")
        self.iconbitmap("assets/esoicon.ico")
        self.bkg_image = tk.PhotoImage(file='assets/bkg.gif')
        self.font20 = Font(family='Segoe', size=20)
        self.font10 = Font(family='Segoe', size=10)
        self.animation_count = 0
        self.animation_cmd = None
        self.returned_path = ""
        self.scraper = Controller.get_scraper()
        self.style = ttk.Style()
        self.style.configure("my_addon.Treeview", font=self.font10, 
                            background="#333333", fg="#000000" )
        self.style.configure("my_addon.Treeview.Heading", font=self.font10)



    def create_display_frame(self, x, y):
        ''' Creates a frame to display messages and list boxes on 
        :param x: The x position to place the frame
        :param y: The y position to place the frame
        '''
        self.display_frame = tk.Frame(background="#333333", height=600, width=600)
        self.display_frame.place(x=x, y=y)

  

    def create_setup_screen(self):
        '''Creates a screen to tell the user the app is being setup, waits 3 seconds and then 
            destroyes it's self'''
        self.create_display_frame(0, 0)
        self.setup_label = tk.Label(self.display_frame, text=Controller.get_constants().INITIAL_MSG,
                        height=10, width=20, pady=2, font=self.font20,
                        fg='#FFFFFF', bg='#333333')
        self.setup_label.place(x=125, y=100)
        self.update()
        time.sleep(3)
        self.display_frame.destroy()
    

            
    def create_not_found_screen(self):
        '''Creates a screen to locate the local addons folder if not found
            The "Browse Folders" button calls the file_search method allowing the user 
                to select the Addons folder with a GUI
            The "Save" button calls the save_path method which save the path to the config file'''
        self.create_display_frame(0, 0)
        self.path_msg = tk.Label(self.display_frame, text=Controller.get_constants().NO_PATH_MSG,
                                font=self.font20, fg='#FFFFFF', bg='#333333')
        self.path_msg.place(x=50, y=10)
        
        self.path_label = tk.Label(self.display_frame, text="",
                                   width=70, font=self.font10)

        self.path_save = tk.Button(self.display_frame, text="Save",
                                   font=self.font20, command=self.save_path)

        self.find_folder_btn = tk.Button(self.display_frame, text="Browse Folders",
                                        command=self.file_search, font=self.font20)
        self.find_folder_btn.place(x=190, y=150)


            
    def save_path(self):
        '''Called from the "create_not_found_screen"
            Updates the config.ini file with the selected path
            Calls the "create_db_update_screen" to proceed with the setup
        '''
        Controller.update_config('local_addon_path', self.path_label['text'])
        self.display_frame.destroy()
        self.update()
        self.create_db_update_screen()


    def file_search(self):
        '''Called from the "create_not_found_screen"
            Uses the asdkirectory method to allow the user to find the 
            Addons folder with a GUI and adds the path to the path_label'''
        file_name = askdirectory(title="Select your ESO Addon folder")
        self.path_label.configure(text=file_name)
        self.returned_path = file_name
        self.path_label.place(x=15, y=200)
        self.path_save.place(x=255, y=250)
        self.find_folder_btn.forget()
        self.find_folder_btn.config(font=self.font10)
        self.find_folder_btn.config(text="Not Correct?")
        self.find_folder_btn.place(x=250, y=140)


    def create_db_update_screen(self):
        '''Creates a screen to tell the user that the DB is being created
            Calls the "create_db" method to start the db creation process
        '''
        self.create_display_frame(0, 0)
        self.setup_label = tk.Label(self.display_frame, text=Controller.get_constants().DB_UPDATE_MSG,
                                height=10, width=26, pady=2, font=self.font20,
                                fg='#FFFFFF', bg='#333333')
        self.setup_label.place(x=80, y=100)
        self.update()
        self.create_db()


    def create_db(self):
        '''Creates and populates the db. This step involves scraping the website and takes up to a minute to complete.
            If there was an exception thrown when loading the db, the error window will
            show for 5 seconds and then the application will exit. 
        '''
        if Controller.create_initial_db():
            Controller.update_config('initial_load', 'False')
            self.scraper.scrape_all_to_db()
            self.display_frame.destroy()
            self.create_find_local_screen()
        else:
            self.display_frame.destroy()
            self.create_error_screen()
            self.update()
            time.sleep(5)
            quit()


    def create_find_local_screen(self):
        '''Creates a screen to tell the user that the local addons are being found
            Rebuilds the local addon table to start freash incase of new addon install
            Calls the "create_db" method to start the db creation process
        '''
        Controller.rebuild_local_addons_table()
        self.create_display_frame(0, 0)
        self.setup_label = tk.Label(self.display_frame, text=Controller.get_constants().LOCAL_FIND_MSG,
                                height=10, width=26, pady=2, font=self.font20,
                                fg='#FFFFFF', bg='#333333')
        self.setup_label.place(x=80, y=100)
        self.update()
        self.find_local_addons()


    def find_local_addons(self):
        '''Calls the "find_local_addons" method to add all installed addon names
            and local version numbers to the db.
            When done, creates the welcome screen.
        '''
        Controller.find_local_addons()
        self.setup_label.destroy()
        self.create_welcome_screen('Rejuvenate is ready!')

    def create_error_screen(self):
        self.create_display_frame(0, 0)
        self.setup_label = tk.Label(self.display_frame, text=Controller.get_constants().DB_ERROR_MSG,
                                height=10, width=22, pady=2, font=self.font20,
                                fg='#FFFFFF', bg='#333333')
        self.setup_label.place(x=100, y=100)


    def create_welcome_screen(self, msg):
        self.addon_frame = tk.Frame(background="#333333", height=600, width=600)
        self.addon_frame.place(x=0, y=0)
        self.setup_label = tk.Label(self.addon_frame, text=msg,
                                width=38, pady=2, font=self.font20,
                                fg='#FFFFFF', bg='#222222')
        self.setup_label.place(x=0, y=2)
        self.create_display_frame(0, 40)
        self.bkg_label = tk.Label(self.display_frame, image=self.bkg_image)
        self.bkg_label.place(x=-2, y=0)

        self.my_addons = ttk.Treeview(self.display_frame, height=23, style="my_addon.Treeview")
        self.my_addons.place(x=0, y=50)

        self.style.configure(self.my_addons)

        self.my_addons['columns'] = ('esoui_id', 'folder_name', 'local_version', 'web_version')
        self.my_addons.column("#0", width=0, stretch=tk.NO)
        self.my_addons.column('esoui_id', anchor=tk.CENTER, width=80)
        self.my_addons.column('folder_name', anchor=tk.W, width=240)
        self.my_addons.column('local_version', anchor=tk.CENTER, width=110)
        self.my_addons.column('web_version', anchor=tk.CENTER, width=110)

        self.my_addons.heading('#0', text="", anchor=tk.CENTER)
        self.my_addons.heading('esoui_id', text="ESOUI ID", anchor=tk.CENTER)
        self.my_addons.heading('folder_name', text="Addon Name", anchor=tk.W)
        self.my_addons.heading('local_version', text="Installed Version", anchor=tk.CENTER)
        self.my_addons.heading('web_version', text="Current Version", anchor=tk.CENTER)

        self.my_addons.tag_configure('odd', background="#303030", foreground="#FFFFFF")
        self.my_addons.tag_configure('even', foreground="#FFFFFF")

        for position, addon in enumerate(Controller.get_local_db_addons()):
            if position % 2 == 0:
                self.my_addons.insert(parent='', index='end', iid=position, text='',
                        values=(addon[0], addon[1], addon[3], addon[4]), tags=('odd',))
            else:
                self.my_addons.insert(parent='', index='end', iid=position, text='',
                        values=(addon[0], addon[1], addon[3], addon[4]), tags=('even',))
        self.my_addons.place(x=25, y=25)

        self.find_current_btn = tk.Button(self.display_frame, text="Find Versions")
        self.find_current_btn.place(x=80, y=525)

        self.update_btn = tk.Button(self.display_frame, text="Update All")
        self.update_btn.place(x=400, y=525)

