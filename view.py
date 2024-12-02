import tkinter as tk
from tkinter import messagebox
from controller import AudioController

class AudioView:
    def __init__(self):
        # Pull the controller in
        self.controller = AudioController(self)
        # Setup Tkinter GUI, release the cursor
        self.root = tk.Tk()
        self.canvas = None
        self.root.withdraw()
        # Create an instance of the button used to load files
        self.LoadButton = tk.Button(self.root, text="Load Audio File (WAV/MP3)", command=self.controller.load_file)
        # Setup the list for the graphs
        self.figures = []
        # Setup the instance that will later be used to swap RT60 graphs
        self.SwapRTGraph = None

    # Starts the show, used after the GUI is called
    def startRun(self):
        # Begin the program
        self.root.mainloop()

    # Function that will exit the program, used when the window is closed.
    def exitRun(self):
        exit(0)

    def startGui(self):
        # Reminder -> self.root = tk.Tk()
        # Setup the window that will prompt the user to load a WAV/MP3 file
        self.root.deiconify()
        self.root.title("RT60 Analyzer")
        self.root.geometry("200x50")
        # Stop the program if the window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.exitRun)
        # Create the button used to load files as was setup in the controller (see __init__)
        self.LoadButton.pack(pady=10)

    # Sets up user message prompts in a safer way
    def messages(self, type, title, message, icon):
        # Create the two types of message boxes used for user prompts
        types = {
            1: messagebox.askokcancel,
            2: messagebox.askyesno,
        }

        # If either of the types are called, then we can setup a message and return it
        if type in types:
            r = types[type](
                title=title,
                message=message,
                icon=icon,
            )
            return r
            
    def createButtons(self):
        # When called, create the extra buttons used for interaction with the graphs
        btn_Frame = tk.Frame(self.root)
        btn_Frame.pack(side=tk.TOP, pady=20)

        # Waveform button
        waveformButton = tk.Button(self.root, text="Waveform", command=self.controller.Waveform)
        waveformButton.pack(padx=5, in_=btn_Frame, side=tk.LEFT)

        # Swappable RT graph button
        self.SwapRTGraph = tk.Button(self.root, text="Low", command=self.controller.nextPlot)
        self.SwapRTGraph.pack(padx=5, in_=btn_Frame, side=tk.LEFT)

        # Combined RT graph button
        combineButton = tk.Button(self.root, text="Combine Plots", command=self.controller.combineFigures)
        combineButton.pack(padx=5, in_=btn_Frame, side=tk.LEFT)

        # Amplitude vs Frequency figure button
        amplitudeVsFrequencyButton = tk.Button(self.root, text="Amplitude vs Frequency", command=self.controller.amplitudeVsFrequencyPlot)
        amplitudeVsFrequencyButton.pack(padx=5, in_=btn_Frame, side=tk.LEFT)

        # Get the RT60 difference redcued by .5 seconds and provide that back to the user
        RTdiff = tk.Label(self.root, text="RT60 Difference: " + str(round(self.controller.model.rtDifference, 3)) + " seconds")
        RTdiff.pack(side=tk.BOTTOM)

        # Obtain the highest resonsance frequency
        lowestLength = min(len(self.controller.model.freqs), len(self.controller.model.data))
        highestAmp = np.argmax(self.controller.model.data[:lowestLength])

        # Provide said frequency back the user
        resonancelabel = tk.Label(self.root, text="Frequency of greatest amplitude: " + str(
            round(self.controller.model.freqs[highestAmp], 1)) + " hz")
        resonancelabel.pack(side=tk.BOTTOM)

        # Provide the length of the selected audio file back the user
        lengthLabel = tk.Label(self.root, text="Time of audio file: " + str(round(self.controller.model.audiotime[-1], 2)) + " seconds")
        lengthLabel.pack(side=tk.BOTTOM)

    def displayWaveform(self, model):
        # Get rid of the load button
        self.LoadButton.destroy()
        # Call the new buttons in if there's a single channel
        if self.controller.model.numChannels == 1:
            self.createButtons()
            # Set a new GUI size
            self.root.geometry("500x520")
        # Otherwise skip the buttons
        else:
            self.root.geometry("500x500")

        # Add the waveform to the list of figures
        self.figures.append(Figure(figsize=(7, 5), dpi=100))
        # Prepare for the plots
        time = np.linspace(0., model.data.shape[0] / model.samplerate, model.data.shape[0])
        figure = self.figures[0].add_subplot(1, 1, 1)

        #TODO -> Account for surround sound
        if model.numChannels == 2:
            figure.plot(time, model.data[:, 0], label="Left")
            figure.plot(time, model.data[:, 1], label="Right")
        else:
            figure.plot(time, model.data, label="Audio")
        figure.legend()
        figure.set_xlabel("Time (in seconds)")
        figure.set_ylabel("Amplitude (in decibals")
        figure.set_title("Waveform of " + model.audiofilename)

        # Make the canvas a TkAgg object, so we can put it in window
        self.canvas = FigureCanvasTkAgg(self.figures[0], master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP)
