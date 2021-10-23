import pygame
import cv2
import graphics

videoList = []
gametfps = graphics.gameGraphics.tfps


def convertToPygameImage(image):
    return pygame.image.frombuffer(image.tobytes(), image.shape[1::-1], "RGB")


class Video:
    def __init__(self, name, filename, screen, x, y, state, repeat):
        self.screen = screen
        self.filename = filename
        self.name = name
        self.x = x
        self.y = y
        self.video = cv2.VideoCapture(filename)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.counter = 0
        self.sizeChanged = False
        self.newW = 0
        self.newH = 0
        self.onFrame = None
        self.state = state
        self.repeat = repeat
        self.stayOnLastFrame = False

    def changeSize(self, newSize):
        self.sizeChanged = True
        self.newW = newSize[0]
        self.newH = newSize[1]


    def drawFrame(self, tfps):
        try:
            if self.state:
                self.counter += 1
                rate = int(tfps/self.fps)
                if rate == 0:
                    rate = 1
                if self.counter % rate == 0 or self.counter == 1:
                    ret, frame = self.video.read()
                    cvImage = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    self.onFrame = convertToPygameImage(cvImage)
                    if self.sizeChanged:
                        self.onFrame = pygame.transform.scale(self.onFrame, (self.newW, self.newH))

                self.screen.blit(self.onFrame, (self.x, self.y))

                if self.counter >= tfps:
                    self.counter = 0
        except cv2.error:
            if not self.repeat:
                self.state = False
            if self.repeat:
                self.video = cv2.VideoCapture(self.filename)


def addVideo(video):
    global videoList
    videoList.append(video)

def drawVideos():
    global videoList
    global gametfps

    for video in videoList:
        video.drawFrame(gametfps)