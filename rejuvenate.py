from gui.rejuv_gui import RejuvGUI
from controller import Controller

'''
Program:            Rejuvenate
Author:             Drew Crawford
Last Date Modified: 12/14/21
Purpose:            The is program will update installed addons
                    from the game The Elder Scrolls Online.
Input:              The uesr will select the Addon folder if not 
                    found, they will also correct any incorrectly 
                    matched addons by selecting them and then selecting
                    the correct addon match from the complete list.
Output:             Various screens of feedback, lists of installed
                    addons with web name matches, installed addons 
                    with versions and installed addons with web versions.
'''

root = RejuvGUI()


if Controller.is_initial():
    root.create_setup_screen()
    local_addon_path = Controller.find_local_addon_folder()
    if local_addon_path == '':
        root.create_not_found_screen()
    else:
        root.create_db_update_screen()

else:
    root.create_compare_msg_screen()
    
if __name__ == '__main__':
    root.mainloop()