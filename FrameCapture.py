import cv2


class PreParameters():
    def __init__(self):
        # pictureSize
        self.w = 1280
        self.h = 720

        # rotate angle
        self.rotate = 0

        # frame capture frequency
        self.freq = 30

        # face detection models
        self.cascPath = "haarcascade_frontalface_default.xml"
        self.scaleFactor = float(1.3)
        self.minNeighbors = 5
        self.flag = cv2.cv.CV_HAAR_SCALE_IMAGE

    def setParameters(self, scalfactor,minnum):
        self.scaleFactor = float(scalfactor)
        self.minNeighbors = int(minnum)
        # self.minNeighbors = float(raw_input("plsease enter minNeighbors:"))
        # self.freq = float(raw_input("plsease enter frame capture frequency:"))

    def setRoate(self, rotate):
        self.rotate = rotate


def detectFace(p, image):
    # detect faces in the current frame
    faceCascade = cv2.CascadeClassifier(p.cascPath)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    faces = faceCascade.detectMultiScale(gray, p.scaleFactor, p.minNeighbors, p.flag)
    if len(faces) == 0:
        return None
    else:
        return faces


def saveFrame(filename, img):
    cv2.imwrite(filename, img)


def rotateFrame(frame, rotateAng):
    # rotate frames if necessary
    if rotateAng == "90":
        return cv2.flip(cv2.transpose(frame), 1)
    elif rotateAng == "180":
        return cv2.flip(frame, -1)
    elif rotateAng == "270":
        return cv2.transpose(cv2.flip(frame, 1))
    else:
        return frame



