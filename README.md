# SPIDAM (Scientific Python Interactive Data Acoustic Modeling) COP2080 Final Project

By Christopher Broche, Austin Norman

## Description

Ensure you install ffmpeg as per your system, and run pip install -r requirements.txt after cloning/unzipping the directory.

Run the program by executing main.py

The program takes an audio file (MP3/WAV/M4A) and converts it to wav, can compute wav and mp3 files, shows a plot of whatever audio as RT60 value of low, mid, and high frequencies.

Below are the options in the program

### load audio file
loads whatever audio file
### waveform
shows the plot for waveform
### low
shows the plot for low frequency
### mid
shows the plot for mid frequency
### high
shows the plot for high frequency
### combine plots
shows the combined plots for low, mid, and high frequencies
### amplitude vs frequency
compares the amplitude versus the frequency


## known issues
The converted WAV file created from loading an audio file is left behind and never cleaned up
