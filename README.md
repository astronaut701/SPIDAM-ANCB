# SPIDAM (Scientific Python Interactive Data Acoustic Modeling) COP2080 Final Project

By Christopher Broche, Austin Norman

## description

Ensure you run pip install -r requirements.txt after cloning/unzipping the directory.

Run the program by executing main.py

Takes an audio file and converts it to wav, can compute wav and mp3 files, shows a plot of whatever audio as RT60 value of low, mid, and high frequencies.

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

## undocumented behavior
any audio file with more than two channels will not work

## errors
won't take any file other than mp3 and wav files

## known issues
the converted WAV file created from loading an MP3 is left behind and never cleaned up
