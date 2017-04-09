import kivy
import cv2
import util
import Dialogs
import os
import glob
import FrameCapture as fc
import WriteResults as wr
import EmotionDetection as ed

from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import NumericProperty
from kivy.uix.popup import Popup
from kivy.clock import Clock
from functools import partial

kivy.require('1.9.1')


class MainScreen(Screen):
    pass


class CaptureFrame(Screen):
    process_log = StringProperty("Processing Info")
    rotate = StringProperty('0')
    scaleFactor = StringProperty('1.3')
    minNeighbors = StringProperty('5')
    progressTotal = NumericProperty(100)
    progressCurrent = NumericProperty(0)
    count = NumericProperty(0)
    index = NumericProperty(0)
    video_src = util.video_src
    frame_save = util.frame_save
    prep = fc.PreParameters()

    def dismiss_popup(self):
        """
        dismiss the popup dialog
        """
        self._popup.dismiss()

    """
    load the video from disk
    """
    def show_load(self):
        content = Dialogs.LoadVideoDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load Image", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        try:
            self.video_src = filename[0]
            print self.video_src
            self.frame_save = path
            util.video_src = os.path.join(path, filename[0])
            print util.video_src
            util.frame_save = path
            util.emotion_src = path
            util.pathList = glob.glob(util.emotion_src + "/*jpg")
        except Exception:
            self.dismiss_popup()
            util.show_message(self, "Please choose a file!")
        else:
            self.dismiss_popup()

    """
    Set saving path
    """
    def show_saving(self):
        content = Dialogs.SaveDialog(choose=self.choose, cancel=self.dismiss_popup)
        self._popup = Popup(title="Set Saving Path", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def choose(self, path):
        util.frame_save = path
        self.frame_save = util.frame_save
        self.dismiss_popup()

    """
    Set parameters
    """
    def show_setting(self):
        content = Dialogs.SettingDialog(set=self.setting, cancel=self.dismiss_popup,
                                checkActive0=self.check_active0,
                                checkActive1=self.check_active1,
                                checkActive2=self.check_active2,
                                checkActive3=self.check_active3)
        self._popup = Popup(title="Settings", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def setting(self, scal_factor, min_num):
        self.scaleFactor = scal_factor
        self.minNeighbors = min_num
        self.prep.setParameters(self.scaleFactor, self.minNeighbors)
        self.prep.setRoate(self.rotate)
        self.process_log = "Setting parameters successfully."
        self.dismiss_popup()

    """
    Rotate checkbox active check
    setting the rotate angle
    """
    def check_active0(self, *args):
        if args:
            self.rotate = '0'

    def check_active1(self, *args):
        if args:
            self.rotate = '90'

    def check_active2(self, *args):
        if args:
            self.rotate = '180'

    def check_active3(self, *args):
        if args:
            self.rotate = '270'

    """
    Functions used to call the frame capture functions.
    The main processing part of frame capture.
    """

    def update_next_frame(self, v, *largs):
        """
        Process eacb frame, called by kivy clock per 0.01 second
        :param v: frameCapture instance by OpenCV
        :return: If no more frames, return False
        """
        self.index += 1
        print "Frame No.", self.index
        self.process_log = "Processing Frame No." + str(self.index)
        self.progressCurrent = self.index
        retrl, image = v.read()
        if image is None:
            util.show_message(self, "Capture Complete.")
            self.process_log = "Capture Complete."
            self.index = 0
            self.count = 0
            self.progressCurrent = 0
            self.progressTotal = 100
            return False

        if self.count != 0:
            self.count -= 1

        else:
            # rotate frame if necessary
            image = fc.rotateFrame(image, self.prep.rotate)

            # using openCV face detection
            result = fc.detectFace(self.prep, image)

            # print and show results
            if result is None:
                print "No face detected."
                self.process_log += "\nNo face detected"
            else:
                self.count = self.prep.freq
                print "detect {0} faces.".format(len(result))
                # for (x, y, w, h) in result:
                #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                #
                # cv2.imshow("Display images", image)
                # cv2.waitKey(0)
                print "saving frame..."
                self.process_log += "\nSaving frame..."
                filename = "frm_" + str(self.index) + ".JPG"
                try:
                    fc.saveFrame(os.path.join(self.frame_save, filename), image)
                except Exception:
                    self.show_message("Please choose a valid path to save.")
                    return False

    def process_framecapture(self):
        """
        Frame capture main function
        Called by "process_framecapture" button listener.
        :return:
        """
        self.count = 0
        self.index = 0
        v = cv2.VideoCapture()
        v.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.prep.w)
        v.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.prep.h)
        v.open(self.video_src)

        if v.isOpened() is True:
            video_length = int(v.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
            self.progressTotal = video_length
            print "Capturing frames..."
        else:
            print "Fail to open video."
            return util.show_message(self, "Fail to open video.")

        Clock.schedule_interval(partial(self.update_next_frame, v), 0.01)


class DetectEmotion(Screen):
    emotion_src = util.emotion_src
    csv_src = util.csv_src
    progressTotal = NumericProperty(100)
    progressCurrent = NumericProperty(0)
    count = NumericProperty(0)
    location = StringProperty("Room 101")
    date = StringProperty("01/01/2016")
    time = StringProperty("00:00")
    process_log = StringProperty("Processing Info.")


    def dismiss_popup(self):
        """
        dismiss the popup dialog
        """
        self._popup.dismiss()

    """
    Set picture loading path
    """
    def show_load(self):
        content = Dialogs.LoadPictureDialog(load = self.load_picture, cancel = self.dismiss_popup)
        self._popup = Popup(title = "Load Pictures", content = content,
                            size_hint = (0.9, 0.9))
        self._popup.open()

    def load_picture(self, path):
        self.emotion_src = path
        util.emotion_src = path
        util.pathList = glob.glob(self.emotion_src + "/*jpg")
        self.dismiss_popup()

    """
    Select SCV file to save result
    """
    def show_select(self):
        content = Dialogs.SelectCSVDialog(select = self.select, create = self.create, cancel = self.dismiss_popup)
        self._popup = Popup(title = "Select CSV File", content = content,
                            size_hint = (0.9, 0.9))
        self._popup.open()

    def select(self, path, filename):
        try:
            util.csv_src = os.path.join(path, filename[0])
            self.csv_src = util.csv_src
        except Exception:
            self.dismiss_popup()
            util.show_message(self, "Please choose a file!")
        else:
            self.dismiss_popup()

    def create(self, path):
        try:
            util.csv_src = wr.create_csv(path)
        except Exception:
            self.dismiss_popup()
            util.show_message(self, "Fail to create file!")
        else:
            self.csv_src = util.csv_src
            self.dismiss_popup()

    """
    Set parameters
    """
    def show_setting(self):
        content = Dialogs.SetDateDialog(confirm=self.setting, cancel=self.dismiss_popup)
        self._popup = Popup(title="Settings", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def setting(self, location, date, time):
        self.location = location
        self.date = date
        self.time = time
        self.process_log = "Setting parameters successfully."
        self.dismiss_popup()

    def update_next_emotion(self, headers, *largs):
        json = None
        params = None
        try:
            path = util.pathList.pop()
        except Exception:
            self.count = 0
            self.progressTotal = 100
            self.progressCurrent = 0
            self.process_log = "Process Complete."
            util.show_message(self, "Process Complete.")
            return False
        else:
            with open(path, 'rb') as f:
                data = f.read()
            result = ed.process_request(json, data, headers, params)
            self.count += 1
            self.progressCurrent = self.count
            self.process_log = "Processing picture " + str(self.count) + "/" + str(self.progressTotal)
            if len(result) == 0:
                self.process_log = "No face detected"
                return True
            rows = wr.process_results(self.location, self.date, self.time, result)
            print self.csv_src
            isSaved = wr.save_result(rows, self.csv_src)
            if isSaved:
                self.process_log = "Result saved"
            else:
                util.show_message(self, "Cannot save results, \ndid you select/create the saving file?")
                return False


    def process_emotionAPI(self):
        """
        Call emotion API, to process the frames in path: "emotion path"
        Called by "process_emotionAPI" button listener
        :return:
        """
        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = ed.get_key()
        headers['Content-Type'] = 'application/octet-stream'
        self.process_log = "Start processing..."
        try:
            self.progressTotal = len(util.pathList)
        except Exception:
            util.show_message(self, "No pictures were loaded. \nPlease choose a valid path.")
            return False
        else:
            self.count = 0

            Clock.schedule_interval(partial(self.update_next_emotion, headers), 0.01)


class ScreenManagement(ScreenManager):
    pass
main = Builder.load_file("main.kv")


class MainApp(App):
    def build(self):
        return main

if __name__ == '__main__':
    MainApp().run()