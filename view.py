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
