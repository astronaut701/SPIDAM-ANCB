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

    def readWav(self):
        self.samplerate, self.data = wavfile.read("tempconvert.wav")
        if self.numChannels == 1:
            self.spectrum, self.freqs, self.audiotime, self.im = plt.specgram(self.data, Fs=self.samplerate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
            self.frequency_target(300)
            self.rt60compute(0)
            self.frequency_target(1000)
            self.rt60compute(1)
            self.frequency_target(3000)
            self.rt60compute(2)
            self.calcDiff()

    def placeConvert(self, path):
        sound = AudioSegment.from_file(path)
        sound.export("tempconvert.wav", format="wav", tags={})
        self.num_channels()

    def num_channels(self):
        sound = AudioSegment.from_file("tempconvert.wav")
        self.numChannels = sound.channels

    def findAFrequency(self, target):
        for frequency in self.freqs:
            if frequency > target:
                return frequency
        return None

    def frequency_target(self, target):
        # Use the findAFrequency function to obtain the function to obtain the dB data for the RT60 computation
        targetFreq = self.findAFrequency(target)
        # Find where the targetFreq first occurs
        targetFreqIndex = np.where(self.freqs == targetFreq)[0][0]
        # Grab the raw data of the frequency
        dataOfFreq = self.spectrum[targetFreqIndex]
        # Convert to dB
        freqData_dB = 10 * np.log10(dataOfFreq)
        # Add it to a list for later use in RT60 computation
        self.dBdata.append(freqData_dB)

    def grabNearestFreq(self, target, nearest):
        target = np.asarray(target)
        index = (np.abs(target-nearest)).argmin()
        return target[index]
