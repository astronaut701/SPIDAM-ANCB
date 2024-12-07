from model import AudioModel
from tkinter import filedialog

#Used for restarting the program
import sys
import subprocess

class AudioController:
    def __init__(self, view):
        self.model = AudioModel()
        self.view = view
        self.graphNum = 0

    def load_file(self):
        # Store the path of the audio file we wish to open
        path = filedialog.askopenfilename(title="Select a WAV/MP3/M4A audio file.", filetypes=[("WAV, MP3, M4A", "*.*")])

        # Check the file type to see if it's MP3 or WAV
        file_type = path[path.rfind(".") + 1:]
        #If it's neither, then throw an error to the user and try again
        if file_type.lower() != "mp3" and file_type.lower() != "wav" and file_type.lower() != "m4a":
            #If the user cancels, quit the program.
            if (not self.view.messages(1, 'Warning!', 'Please load a MP3, WAV, or M4A file!', 'warning')):
                self.view.exitRun()
        else:
            #Check the number of channels in the origin file
            self.model.org_num_channels(path)
            #Provide a warning that a conversion to mono will occur if continued
            if self.model.numChannels != 1:
                if self.view.messages(2, "Warning!", "There are multiple channels in this audio file, it will converted to mono! Do you wish to continue?",'warning') == False:
                    exit(0)
            #Convert the MP3 to WAV
            self.model.audiofilename = path[path.rfind("/") + 1:]
            if file_type == "mp3":
                self.model.audioToWav(path)
                path = "tempconvert.wav"
            # Store the converted WAV file
            self.model.placeConvert(path)
            # Read the file
            self.model.readWav()
            # Display waveform
            self.view.displayWaveform(self.model)
            # Generate the figure for low, mid, high frequencies
            self.view.genRT60figure(0)
            self.view.genRT60figure(1)
            self.view.genRT60figure(2)
            # Generate the combined figure
            self.view.combinedFigure()
            # Generate the figure for amplitude vs frequency
            self.view.amplitudeVsFreq()

    def Restart(self):
        # Restart the script using subprocess, not the cleanest way, but it works.
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit()  # Exit the current script

    def Waveform(self):
        self.view.drawNextCanvas(0)

    def combineFigures(self):
        self.view.drawNextCanvas(4)

    def amplitudeVsFrequencyPlot(self):
        self.view.drawNextCanvas(5)

    # Button that swaps between the figures
    def nextPlot(self):
        # 0 -> Amplitude Figure
        # 1 -> Low RT60
        # 2 -> Mid RT60
        # 3 -> High RT60
        self.graphNum += 1
        if self.graphNum == 4:
            self.graphNum = 1
        if self.graphNum == 1:
            self.view.SwapRTGraph.config(text="Mid")
        elif self.graphNum == 2:
            self.view.SwapRTGraph.config(text="High")
        elif self.graphNum == 3:
            self.view.SwapRTGraph.config(text="Low")

        self.view.drawNextCanvas(self.graphNum)
