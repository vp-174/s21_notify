from Imports import *

class Audio:
    def __init__(self, filename):
        self.filename = filename
        try:
            self.wf = wave.open(self.filename, 'rb')
        except FileNotFoundError:
            print(f"Файл не найден: {self.filename}")
            self.wf = None
            return
        except wave.Error as e:
            print(f"Ошибка при открытии файла WAV: {e}")
            self.wf = None
            return

        self.p = pyaudio.PyAudio()
        try:
            self.stream = self.p.open(
                format=self.p.get_format_from_width(self.wf.getsampwidth()),
                channels=self.wf.getnchannels(),
                rate=self.wf.getframerate(),
                output=True
            )
        except Exception as e:
            print(f"Ошибка при открытии потока: {e}")
            self.stream = None
            self.p.terminate()

    def play(self):
        if self.wf is None or self.stream is None:
            print("Не удалось воспроизвести звук, так как аудиофайл не был загружен корректно.")
            return

        try:
            data = self.wf.readframes(1024)
            while data:
                self.stream.write(data)
                data = self.wf.readframes(1024)
        except Exception as e:
            self.stream.close()

    def stop(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        if self.p is not None:
            self.p.terminate()

def play_wave(filename):
    chunk = 1024

    with wave.open(filename, 'rb') as wf:
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