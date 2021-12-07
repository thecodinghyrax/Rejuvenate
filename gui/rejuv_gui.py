import tkinter as tk
from tkinter.font import Font
from tkinter.filedialog import askdirectory
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
            # Controller.add_search_names()
            self.display_frame.destroy()
            self.create_welcome_screen('Rejuvenate is ready!')
        else:
            self.display_frame.destroy()
            self.create_error_screen()
            self.update()
            time.sleep(5)
            quit()


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

        self.local_addons_display = tk.Listbox(self.display_frame, height=28, width=45, 
                                                bg='#333333', font=self.font10, fg="#FFFFFF")
        self.local_addons_display.place(x=30, y=30)
        self.get_local_addons_btn = tk.Button(self.display_frame, text='Find installed addons', 
                                                command=self.show_installed)
        self.get_local_addons_btn.place(x=120, y=520)

        self.get_updates_btn = tk.Button(self.display_frame, text='Check for updates')


    def show_installed(self):
        self.local_addons_display.delete(0, tk.END)
        addons = Controller.get_local_addon_dirs()
        unmatched_addons = Controller.get_unmatched_addons(addons)
        while len(unmatched_addons) > 0:
            self.create_not_found_popup(unmatched_addons[0])
            self.local_addons_display.delete(0, tk.END)
            self.local_addons_display.insert(0, 'Please press "Find installed addons" again')
            unmatched_addons.pop[0]
        matched_addons = Controller.get_matching_addons(Controller.get_local_addon_dirs())
        Controller.set_all_to_uninstalled()
        for count, addon in enumerate(matched_addons):
            print(addon)
            try:
                addon_info = f"{addon[1]} - Version: {Controller.get_addon_version(addon[2])}"
            except Exception as e:
                addon_info = f"{addon[1]} threw error {e}"
            Controller.update_addon_info('esoui_id', addon[0], 'installed', 1)
            self.local_addons_display.insert(count, addon_info)
        self.local_addons_display.place(x=30, y=30)
        self.get_local_addons_btn.destroy()
        self.get_updates_btn.place(x=120, y=520)

    
    def create_not_found_popup(self, not_found_addon):
        popup = tk.Toplevel(self, bg='#333333')
        popup.geometry("300x300")
        popup.title(f"Addon Not found - {not_found_addon}")
        match_result = Controller.try_match(not_found_addon, Controller.get_all_addons())
        msg = f"{not_found_addon} was not found!\n\n" + \
                f"Is this the addon you are using?\n\n{match_result[1]}"
        tk.Label(popup, text=msg, bg='#333333', font=self.font10, fg="#FFFFFF").place(x=30, y=50)
        tk.Button(popup, text="Yes", font=self.font10,
                    command=lambda: update_addon_name(match_result[2], not_found_addon)
                    ).place(x=125, y=200)
        def update_addon_name(old_name, new_name):
            Controller.update_addon_info('search_name', old_name, 'user_updated', 1)
            Controller.update_addon_info('search_name', old_name, 'search_name', new_name)
            popup.destroy()
        #TODO make logic for manually updating addon name




    # Trying to get a loading gif to work here
    # def create_loading_canvas(self, parent):
    #     self.loading_gif = tk.Canvas(parent, width=200, height=200, background='#333333')
    #     self.loading_gif.place(x=150, y=400)
    #     self.sequence = []
    #     for count in range(0, 36):
    #         self.sequence.append(ImageTk.PhotoImage(Image.open(f'assets/eso{count}.gif')))
    #     self.image = self.loading_gif.create_image(100,100, image=self.sequence[0])
    #     self.animate(1)


    # def animate(self, counter):
    #     self.loading_gif.itemconfig(self.image, image=self.sequence[counter])
    #     self.db_update_frame.after(50, lambda: self.animate((counter+1) % len(self.sequence)))
