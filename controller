from model import AudioModel
from tkinter import filedialog

class AudioController:
    def __init__(self, view):
        self.model = AudioModel()
        self.view = view
        self.graphNum = 0

    def load_file(self):
        # Store the path of the audio file we wish to open
        path = filedialog.askopenfilename(title="Select a WAV/MP3 audio file.", filetypes=[("All Files", "*.*")])

        # Check the file type to see if it's MP3 or WAV
        file_type = path[path.rfind(".") + 1:]
        #If it's neither, then throw an error to the user and start over
        if file_type.lower() != "mp3" and file_type.lower() != "wav":
            self.view.messages(1, 'Warning!', 'Please load a mp3 or wav file!', 'warning')
        else:
            #Convert the MP3 to WAV
            self.model.audiofilename = path[path.rfind("/") + 1:]
            if file_type == "mp3":
                self.model.audioToWav(path)
                path = "tempconvert.wav"
            # Store the converted WAV file
            self.model.placeConvert(path)
            if self.model.numChannels != 1:
                if self.view.messages(2, "Warning!", "There are multiple channels in this audio file, only the audio waveform can be displayed! Do you wish to continue?",'warning') == False:
                    exit(0)
                else:
                    # If we're all set with that, read the file (and do something else)
                    self.model.readWav()
