from Imports import *

class Audio:
    def __init__(self, filename):
        self.filename = filename
    def play_wave(self):
        chunk = 1024

        with wave.open(self.filename, 'rb') as wf:
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)

            data = wf.readframes(chunk)
            while data:
                stream.write(data)
                data = wf.readframes(chunk)

            stream.close()
            p.terminate()