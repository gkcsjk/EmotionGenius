import Dialogs
from kivy.uix.popup import Popup
from kivy.properties import ListProperty
from kivy.properties import StringProperty

"""
global variables initializing
"""
video_src = StringProperty("Video File Path Display")
frame_save = StringProperty("Frame Saving Path Display")
emotion_src = StringProperty("Emotion Sources Load Path Display")
csv_src = StringProperty("CSV File Chosen Display")
process_content = StringProperty("Process Content Display")
resultList = ListProperty()
pathList = ListProperty()
message = StringProperty()
"""
General used functions
"""
def show_message(mScreen, msg):
    """
    Show  message when necessary
    """
    global message
    message = msg
    content = Dialogs.MessageDialog(confirm=mScreen.dismiss_popup, message=message)
    mScreen._popup = Popup(title="Message", content=content, size_hint=(0.4, 0.3))
    mScreen._popup.open()

