from graphics import *
from userKey import *
from audio import *
import videos



# this will clear all the list, so you can run another file
# shapes, audios, triggers, input triggers
def restart(doObjects = True, doTriggers = True, doSongs = True, doVideos = True, doFuncList = True, doNon_FPS_triggerList = True):
    global objects
    global triggerList
    global funcList
    global songs
    global videos
    global non_FPS_triggerList

    if doObjects:
        objects.clear()

    if doTriggers:
        triggerList.clear()

    if doFuncList:
        funcList.clear()

    if doSongs:
        clearSongs()

    if doVideos:
        videos.videoList.clear()

    if doNon_FPS_triggerList:
        non_FPS_triggerList.clear()
    gameGraphics.videoBackground = False


# group of shapes that are scrollable, as a list of shapes
# it is useful when elements in the page are more than the page's size, so we can scroll down and see the rest of
# the elements
class Scrollable:
    def __init__(self, object_list, scroll_sensitivity, scroll_area, motion=1, create=True):
        self.object_list = object_list
        self.scroll_sensitivity = scroll_sensitivity
        self.scroll_area = scroll_area
        self.motion = motion
        if create:
            self.create()

    # create triggers for the scrollable object, and make the scroll function work
    def create(self):
        scrolling_event = pygame.MOUSEBUTTONDOWN

        self.going_down = True
        self.going_up = True

        motion = self.motion
        object_list = self.object_list
        scroll_sensitivity = self.scroll_sensitivity
        scroll_area = self.scroll_area
        print(scroll_area)

        def scrolling(event):
            going_down = self.going_down
            going_up = self.going_up
            scroll_area = self.scroll_area

            if scroll_area.collidepoint(pygame.mouse.get_pos()):

                if event.button == scroll["up"] and self.going_up:
                    self.going_down = True
                    self.going_up = True
                    for shape in object_list:
                        try:
                            shape.animations.remove(shape.getAnimationByName("scrolling"))
                        except ValueError:
                            pass

                        shape.addAnimation([[0, -scroll_sensitivity, 0, 0, motion]], False, "scrolling", True)
                        # button.y += scroll_sensitivity
                if event.button == scroll["down"] and self.going_down:
                    self.going_down = True
                    self.going_up = True
                    for shape in object_list:
                        try:
                            shape.animations.remove(shape.getAnimationByName("scrolling"))
                        except ValueError:
                            pass

                        shape.addAnimation([[0, scroll_sensitivity, 0, 0, motion]], False, "scrolling", True)

        def fixPos():
            if object_list[len(object_list) - 1].y < screenH - object_list[len(object_list) - 1].h:
                minus = (screenH - object_list[len(object_list) - 1].h) - object_list[len(object_list) - 1].y
                self.going_up = False
                for shape in object_list:
                    try:
                        shape.animations.remove(shape.getAnimationByName("scrolling"))
                    except ValueError:
                        pass
                    shape.y += minus
            if object_list[0].y > 0:
                minus = object_list[0].y
                self.going_down = False
                for shape in object_list:
                    try:
                        shape.animations.remove(shape.getAnimationByName("scrolling"))
                    except ValueError:
                        pass
                    shape.y -= minus

        addTrigger(fixPos)
        newEventableFunc(scrolling_event, scrolling)


class TextBox:
    waiting_event = pygame.MOUSEBUTTONDOWN
    def __init__(self, x, y, boxW, boxH, text_color, box_color, center_it=False, box=None, getting_input=False):
        self.x = x
        self.y = y

        self.text_color = text_color
        self.box_color = box_color
        self.center_it = center_it
        self.box = box
        self.generate_rect = False
        self.getting_input = getting_input
        if getting_input == True:
            self.wait_for_click(done=True)
        if self.box == None:
            self.generate_rect = True

    def make_text_box(self):
        addTrigger(self.wait_for_click)


    def wait_for_click(self, done=False):
        if not done:
            newKeyIfFunc(self.waiting_event)

