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


    ############################## GENERIC (reusable) COMPONENTS ###########################
    def create_display_frame(self, x, y):
        ''' Creates a frame to display messages and list boxes on. This will be 
            created and destroyed for every other screen (base)
        :param x: The x position to place the frame
        :param y: The y position to place the frame
        '''
        self.display_frame = tk.Frame(background="#333333", height=600, width=600)
        self.display_frame.place(x=x, y=y)


    def create_table_view(self, msg, column_list, data):
        '''Creates a screen to show data in a table (treeview)
        :param msg: A message to be displayed at the top of the screen
        :param column_list: A list of column names to be used in the heading
        :param data: A list of data from the db to be displayed in the table
        '''
        self.addon_frame = tk.Frame(background="#333333", height=600, width=600)
        self.addon_frame.place(x=0, y=0)
        self.setup_label = tk.Label(self.addon_frame, text=msg,
                                width=38, pady=2, font=self.font20,
                                fg='#FFFFFF', bg='#222222')
        self.setup_label.place(x=0, y=2)
        self.create_display_frame(0, 40)
        self.bkg_label = tk.Label(self.display_frame, image=self.bkg_image)
        self.bkg_label.place(x=-2, y=0)

        self.my_addons = ttk.Treeview(self.display_frame, height=23, style="my_addon.Treeview", selectmode='browse')
        self.my_addons.place(x=0, y=50)

        self.style.configure(self.my_addons)

        self.my_addons['columns'] = tuple(column_list)
        self.my_addons.column("#0", width=0, stretch=tk.NO)
        col_width = round(550 / len(column_list))
        for column in column_list:
            self.my_addons.column(column, anchor=tk.CENTER, width=col_width)
        
        self.my_addons.heading('#0', text="", anchor=tk.CENTER)
        for column in column_list:
            self.my_addons.heading(column, text=column, anchor=tk.CENTER)

        self.my_addons.tag_configure('odd', background="#303030", foreground="#FFFFFF")
        self.my_addons.tag_configure('even', foreground="#FFFFFF")
                    
        for position, addon in enumerate(data):
            data_values = [] 
            for index in range(len(column_list)):
                data_values.append(addon[index])
            if position % 2 == 0:
                self.my_addons.insert(parent='', index='end', iid=position, text='',
                        values=(tuple(data_values)), tags=('odd',))
            else:
                self.my_addons.insert(parent='', index='end', iid=position, text='',
                        values=(tuple(data_values)), tags=('even',))
            self.my_addons.place(x=25, y=25)

  
    ##############################  INITIAL SETUP SCREENS #################################
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


    def create_error_screen(self):
            '''Create a screen to show an error message if the database fails to be created'''
            self.create_display_frame(0, 0)
            self.setup_label = tk.Label(self.display_frame, text=Controller.get_constants().DB_ERROR_MSG,
                                    height=10, width=22, pady=2, font=self.font20,
                                    fg='#FFFFFF', bg='#333333')
            self.setup_label.place(x=100, y=100)


    ################################# SETUP GUI METHODS  ###############################
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


    def create_db(self):
        '''Creates and populates the db. This step involves scraping the website and takes up to a minute to complete.
            If there was an exception thrown when loading the db, the error window will
            show for 5 seconds and then the application will exit. 
        '''
        if Controller.create_initial_db():
            Controller.update_config('initial_load', 'False')
            self.scraper.scrape_all_to_db()
            self.display_frame.destroy()
            self.create_compare_msg_screen()
        else:
            self.display_frame.destroy()
            self.create_error_screen()
            self.update()
            time.sleep(5)
            quit()


    ###################################### MAIN UI SCREENS  ##################################
    def create_compare_msg_screen(self):
            '''Create a screen to tell the user to check the addons and update if needed'''
            self.create_display_frame(0, 0)
            self.setup_label = tk.Label(self.display_frame, text=Controller.get_constants().CHECK_ADDONS_MSG,
                                    height=10, width=22, pady=2, font=self.font20,
                                    fg='#FFFFFF', bg='#333333')
            self.setup_label.place(x=120, y=100)
            self.update()
            time.sleep(5)
            self.display_frame.destroy()
            self.create_compare_addons_screen()


    def create_compare_addons_screen(self):
        '''Creates a screen that show the user all the installed addons and the addons that
            were matched to them. There may be error and should be reviewed. The user can 
            select the row that is incorrect and press the "Update Selected" btn to fix.'''
        self.display_frame.destroy()
        Controller.rebuild_local_addons_table()
        Controller.find_local_addons()
        msg = "Please update any addon that does not match"
        column_list = ['ESOUI ID', 'Web Version', 'Local Version']
        data = Controller.get_matching_list()
        self.create_table_view(msg, column_list, data)
        self.create_selected_btn()
        self.create_view_local_addons_btn()


    def create_select_correct_screen(self, local):
        '''Creates a screen that shows all addons listed on the website so the user
            can select the proper one that actually matches the local addon listed 
            in the message box at the top of the screen
            :param local: The name of the locally install addon that was not matched correctly'''
        self.display_frame.destroy()
        msg = f"Select the correct addon for {local}"
        column_list = ['ESOUI ID', 'Web Version']
        data = Controller.get_web_db_addons()
        data.sort(key=lambda y: y[1])
        self.create_table_view(msg, column_list, data)
        self.create_update_match_btn(data, local) # passing data down to avoid another db call

    
    def create_installed_addons_screen(self):
        '''Creates a screen that displays all the locally installed addons in a table'''
        self.display_frame.destroy()
        msg = 'Let\'s check for some updates!'
        column_list = ['Local Addon', 'Local Version', 'Web Version']
        data = Controller.get_addons_to_check()
        self.create_table_view(msg, column_list, data)
        self.create_check_for_updates_btn(data)


    def create_version_check_screen(self):
        '''Creates a screen to tell the user that current addon version are being checked
 
        '''
        self.create_display_frame(0, 0)
        self.setup_label = tk.Label(self.display_frame, text=Controller.get_constants().CHECK_UPDATE_MSG,
                                height=10, width=26, pady=2, font=self.font20,
                                fg='#FFFFFF', bg='#333333')
        self.setup_label.place(x=80, y=100)
        self.update()

        
    ################################# MAIN GUI BUTTONS  #################################
    def create_selected_btn(self):
        '''Creates a button that calls the update selected method'''
        self.selected_btn = tk.Button(self.display_frame, text='Update Selected', command=self.update_selected)
        self.selected_btn.place(x=150, y=520)


    def create_compare_btn(self):
        '''Creates a button that calls the create_compare_addons_screen'''
        self.compare_btn = tk.Button(self.display_frame, text='Compare addons', command=self.create_compare_addons_screen)
        self.compare_btn.place(x=250, y=520)


    def create_update_match_btn(self, data, local):
        '''Creates a button that calls the update_match method
        :param data: The db call containing all web addons
        :param local: The name of the local addon that did not match'''
        self.update_match_btn = tk.Button(self.display_frame, text='Update Match', command=lambda: self.update_match(data, local))
        self.update_match_btn.place(x=250, y=520)

    
    def create_view_local_addons_btn(self):
        '''Creates a button that calls the create_installed_addon_screen method'''
        self.view_local_addons_btn = tk.Button(self.display_frame, text='Addons All Match', command=self.create_installed_addons_screen)
        self.view_local_addons_btn.place(x=350, y=520)

    
    def create_check_for_updates_btn(self, data):
        '''Creates a button that calls the create_installed_addon_screen method'''
        self.check_for_updates_btn = tk.Button(self.display_frame, text='Check for Updates', command=lambda: self.check_for_updates(data))
        self.check_for_updates_btn.place(x=250, y=520)
        
            
    def create_update_all_btn(self):
        '''Creates a button that calls the create_installed_addon_screen method'''
        self.update_all_btn = tk.Button(self.display_frame, text='Update All Addons', command=self.update_all)
        self.update_all_btn.place(x=250, y=520)
    

    def create_exit_btn(self):
        '''Creates a button that calls the create_installed_addon_screen method'''
        self.update_all_btn = tk.Button(self.display_frame, text='Exit', command=quit)
        self.update_all_btn.place(x=350, y=520)


    ########################################## MAIN GUI METHODS  #########################
    def update_selected(self):
        '''Gets the currently selected row and passes the data to the create_select_correct_screen'''
        curent_item = self.my_addons.focus()
        matching_list = Controller.get_matching_list()
        self.create_select_correct_screen(matching_list[int(curent_item)][2])


    def find_local_addons(self):
        '''Calls the "find_local_addons" method to add all installed addon names
            and local version numbers to the db.
            When done, creates the welcome screen.'''
        self.setup_label.destroy()
        self.create_installed_addons_screen()


    def update_match(self, data, local):
        '''Calls the update to fix the bad match
        :param data: The db call containing all web addons
        :param local: The name of the local addon that did not match'''
        curent_item = self.my_addons.focus()
        Controller.add_correction_to_db(local, data[int(curent_item)])
        self.create_compare_msg_screen()
  
  
    def check_for_updates(self, local_addons):
        '''Calls the find_updates method and displays the results'''
        addons = []
        self.create_version_check_screen()
        for addon in local_addons:
            addons.append((addon[0], addon[3]))
        updates = Controller.check_for_updates(addons, self.scraper)
        self.setup_label.destroy()
        self.create_installed_addons_screen()
        print(updates)
        self.check_for_updates_btn.destroy()
        self.create_update_all_btn()
        
        
    def update_all(self):
        '''Calls the update_all method, displays the results and adds an exit button'''
        local_addons = Controller.get_local_db_addons()
        old_addons = []
        for addon in local_addons:
            if addon[3] != addon[4]:
                old_addons.append(addon)
        Controller.update_all(old_addons, self.scraper)
        self.update_all_btn.destroy()
        self.create_installed_addons_screen()
        self.create_exit_btn()
            