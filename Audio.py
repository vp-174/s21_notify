from Imports import *

class Audio:
    '''Класс звука. Мультиплаформа'''
    def play_wave(self, filename):
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

    def play_wave_gnu(self, filename):
        try:
            # Выполняем команду aplay с указанным файлом
            subprocess.run(['aplay', filename], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при воспроизведении аудио: {e}")