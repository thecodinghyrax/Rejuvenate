from gui.rejuv_gui import RejuvGUI
from controller import Controller


root = RejuvGUI()


if Controller.is_initial():
    root.create_setup_screen()
    local_addon_path = Controller.find_local_addon_folder()
    if local_addon_path == '':
        root.create_not_found_screen()
    else:
        root.create_db_update_screen()

else:
    root.create_welcome_screen('Time to Rejuvenate your ESO Addons!')
root.mainloop()