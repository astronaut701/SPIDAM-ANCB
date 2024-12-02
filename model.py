import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
import matplotlib.pyplot as plt

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
        
    def rt60compute(self, type):
        # Get the index of max dB value
        self.maxvaluepos.append(np.argmax(self.dBdata[type]))
        # Go from the max down to each frequency
        stepped_array = self.dBdata[type][self.maxvaluepos[-1]:]
        # Compute the -5 dB drop
        drop5 = self.dBdata[type][self.maxvaluepos[type]] - 5
        # Find nearest match for -5dB within the stepped data
        drop5 = self.grabNearestFreq(stepped_array, drop5)
        # Find where that lines up in the original data
        match5 = np.where(self.dBdata[type] == drop5)
        # Do the same for the -25 dB drop
        drop25 = self.dBdata[type][self.maxvaluepos[type]] - 25
        drop25 = self.grabNearestFreq(stepped_array, drop25)
        match25 = np.where(self.dBdata[type] == drop25)
        # Compute RT20 from the -5 and -25 dB drops, multiply that by three to get RT60.
        rt20 = (self.audiotime[match5] - self.audiotime[match25])[0]
        # place indexes and RT60 in list
        self.rt60_computed.append([match5, match25, abs(rt20*3)])

    # RT60 difference to .5 seconds
    def calcDiff(self):
        self.rtDifference = ((self.rt60_computed[0][2] + self.rt60_computed[1][2]+ self.rt60_computed[2][2]) / 3) - 0.5
