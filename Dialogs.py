import os

from kivy.utils import platform
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.lang import Builder

main = Builder.load_file("dialogs.kv")

class LoadVideoDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoadVideoDialog, self).__init__(**kwargs)
        self.ids.drives_list.adapter.bind(on_selection_change = self.drive_selection_changed)

    def get_win_drives(self):
        if platform == 'win':
            import win32api
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            return drives
        else:
            return []

    def drive_selection_changed(self, *args):
        selected_item = args[0].selection[0].text
        self.ids.filechooser.path = selected_item


class SaveDialog(FloatLayout):
    choose = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SaveDialog, self).__init__(**kwargs)
        self.ids.drives_list.adapter.bind(on_selection_change = self.drive_selection_changed)

    def get_win_drives(self):
        if platform == 'win':
            import win32api
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            return drives
        else:
            return []

    def drive_selection_changed(self, *args):
        selected_item = args[0].selection[0].text
        self.ids.filechooser1.path = selected_item

    def is_dir(self, directory, filename):
        return os.path.isdir(os.path.join(directory, filename))


class LoadPictureDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(LoadPictureDialog, self).__init__(**kwargs)
        self.ids.drives_list.adapter.bind(on_selection_change = self.drive_selection_changed)

    def get_win_drives(self):
        if platform == 'win':
            import win32api

            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            return drives
        else:
            return []

    def drive_selection_changed(self, *args):
        selected_item = args[0].selection[0].text
        self.ids.filechooser2.path = selected_item

    def is_dir(self, directory, filename):
        return os.path.isdir(os.path.join(directory, filename))


class SettingDialog(FloatLayout):
    set = ObjectProperty(None)
    cancel = ObjectProperty(None)
    checkActive0 = ObjectProperty(None)
    checkActive1 = ObjectProperty(None)
    checkActive2 = ObjectProperty(None)
    checkActive3 = ObjectProperty(None)


class SetDateDialog(FloatLayout):
    confirm = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SelectCSVDialog(FloatLayout):
    select = ObjectProperty(None)
    create = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SelectCSVDialog, self).__init__(**kwargs)
        self.ids.drives_list.adapter.bind(on_selection_change = self.drive_selection_changed)

    def get_win_drives(self):
        if platform == 'win':
            import win32api
            drives = win32api.GetLogicalDriveStrings()
            drives = drives.split('\000')[:-1]
            return drives
        else:
            return []

    def drive_selection_changed(self, *args):
        selected_item = args[0].selection[0].text
        self.ids.filechooser3.path = selected_item

class MessageDialog(FloatLayout):
    confirm = ObjectProperty(None)
    message = StringProperty(None)
