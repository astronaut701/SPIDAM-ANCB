import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
import matplotlib.pyplot as plt
from os import remove

class AudioModel:
    def __init__(self):
        # Setup variables for the audio file's name, audio spectrum, frequency, length, sample rate,
        # and the amount of audio channels
        self.audiofilename = ""
        self.spectrum = None
        self.freqs = None
        self.audiotime = None
        self.samplerate = None
        self.numChannels = 0

        # Setup variables to hold the audio's raw data, the derived dB loudness data. And variables the position of
        # the max value for each frequency, as well as the computed RT60 values along with the RT60 difference.
        self.data = None
        self.dBdata = []
        self.maxvaluepos = []
        self.rt60_computed = []
        self.rtDifference = 0


    # The function imports the audio file and converts it to WAV
    def audioToWav(self, path):
        audio = AudioSegment.from_file(path)
        audio.export("tempconvert.wav", format="wav", tags={})
        self.num_channels()
