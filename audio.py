import subprocess

# a class that stores audio information
class Audio():
    def __init__(self, fileName, name, repeat, state):
        self.fileName = fileName
        self.name = name
        self.repeat = repeat
        self.state = state
        self.thread = None
        self.played = None

    def play(self):
        self.state = True
        self.played = subprocess.Popen(["afplay", self.fileName])

    def stop(self):
        self.played.kill()
        self.state = False

# list of all audios
songs = []

# add a new audio to the list and start it if it is suppose to be playing
def addSong(audio):
    global songs
    songs.append(audio)
    if audio.state == True:
        audio.play()

# clear all the audios in the list
# it stops them and then clears the list
def clearSongs():
    global songs
    for audio in songs:
        if audio.played != None:
            audio.played.kill()
    songs.clear()

# if an audio is over, but it needs to repeat, this will start it again
# it is added to fps file
def audioRepeatCheck():
    global songs
    for audio in songs:
        try:
            if audio.played.poll() != None and audio.state == True and audio.repeat == True:
                audio.play()
        except AttributeError:
            print("some errors")

