import pyaudio
import wave
import numpy as np
import serial
from lifxlan import Light
# import matplotlib.pyplot as plt

bulb = Light("d0:73:d5:28:0b:4a", "10.0.0.16")
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"

# s = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600)

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
print "recording..."
frames = []
amplitudes = []
max = 10000

# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
count = 0
while(True):
    count = count + 1
    data = stream.read(CHUNK, exception_on_overflow=False)
    x = np.fromstring(data, dtype=np.int16)
    freq = np.fft.rfft(x)
    val = np.abs(freq[0]) + np.abs(freq[1]) + np.abs(freq[2])
    if len(amplitudes) >= 20:
      amplitudes.pop()
    amplitudes.insert(0, val)
    avg = sum(amplitudes)/len(amplitudes)
    avg = avg*avg*avg
    if max < avg:
      max = avg
    else:
      max = 0.99*max
    serout = int(avg/max*69390)
    if serout > 65535:
      serout = 65535
    elif serout < 20000:
      serout = 20000
    # s.write(chr(serout))
    if count % 1 == 0:
      print(serout)
      try:
        bulb.set_brightness(serout, rapid=True)
      except:
        pass
    # frames.append(data)
print "finished recording"


# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

# plt.plot(amplitudes)
# plt.show()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

