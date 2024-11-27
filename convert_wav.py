from pydub import AudioSegment

if format=="mp3":
    # convert mp3 to wav
    audio = AudioSegment.from_mp3("input.mp3")
    audio.export("output.wav", format="wav")
    print('Audio converted to wav.')
