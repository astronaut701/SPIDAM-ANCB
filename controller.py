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
                    self.view.displayWaveform(self.model)
            else:
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

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    controller = AudioController(root)
    root.mainloop()
