from Imports import *

class Audio:
    def __init__(self, filename):
        self.filename = filename
        self.wf = wave.open(self.filename, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True
        )

    def play(self):
        data = self.wf.readframes(1024)
        while data:
            self.stream.write(data)
            data = self.wf.readframes(1024)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

# Пример использования класса
# if __name__ == "__main__":
#     player = AudioPlayer('01.wav')
#     try:
#         player.play()
#     except KeyboardInterrupt:
#         print("Воспроизведение остановлено.")
#     finally:
#         player.stop()