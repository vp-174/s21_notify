from Imports import *

class PlayWaveThread(QThread):
    finished = Signal()

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self):
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
        self.finished.emit()

class PlayWaveGnuThread(QThread):
    finished = Signal()

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def run(self):
        try:
            subprocess.run(['aplay', self.filename], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при воспроизведении аудио: {e}")
        self.finished.emit()

class Audio:
    '''Класс звука. Мультиплатформа'''

    def __init__(self):
        self.wave_thread = None
        self.wave_gnu_thread = None

    def play_wave(self, filename):
        '''Воспроизведение звука в Windows (в отдельном потоке)'''
        if self.wave_thread and self.wave_thread.isRunning():
            self.wave_thread.terminate()

        self.wave_thread = PlayWaveThread(filename)
        self.wave_thread.start()

    def play_wave_gnu(self, filename):
        '''Воспроизведение звука в Linux (в отдельном потоке)'''
        if self.wave_gnu_thread and self.wave_gnu_thread.isRunning():
            self.wave_gnu_thread.terminate()

        self.wave_gnu_thread = PlayWaveGnuThread(filename)
        self.wave_gnu_thread.start()