class Addon:
    ''' The class will represent a single addon and will be used by the Catagory class'''
    
    def __init__(self, esoui_id, name):
        ''' Initialize the class 
        :esoui_id: The id assoicated with an addon on esoui.com
        :name: The displayed name of the addon on esoui.com
        '''
        self._esoui_id = esoui_id
        self._name = name
        

    def get_esoui_id(self):
        ''' Gets the esoui.com id for this addon
        :return: The addon ID
        '''
        return self._esoui_id


    def get_name(self):
        ''' Gets the displayed name of this addon from esoui.com
        :return: The addon name
        '''
        return self._name
    
    
    def get_addon_tuple(self):
        ''' Creates a tuple of the addon infomation, used for storing in the db
        :retrun: A tuple of the addon wil the id as a string and name
        '''
        return (self._esoui_id, self._name)


    def display(self):
        ''' Displays the Addon information
        :returns: Human readable information about this addon
        '''
        return f"ESOUI ID: {self._esoui_id}\nName: {self._name}\n"


    def __str__(self):
        ''' Displays all catagory information
        :returns: All variables used in this Addon instance
        '''
        return f"{self._esoui_id}, {self._name}"
        
        
    def __repr__(self):
        ''' Displays the call to create this Addon instance
        :returns: Information about how the class was instantiated 
        '''
        return f"Addon(esoui_id={self._esoui_id}, name={self._name})"