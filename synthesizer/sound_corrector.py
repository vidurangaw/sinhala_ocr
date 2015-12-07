__author__ = 'Chin'

import wave
import os

package_directory = os.path.dirname(os.path.abspath(__file__))

def correct_audio():
    CHANNELS = 1
    swidth = 2
    Change_RATE = 2.25

    spf = wave.open(package_directory + "/output/output_audio.wav", 'rb')
    RATE=spf.getframerate()
    signal = spf.readframes(-1)

    wf = wave.open(package_directory + "/output/output3.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE*Change_RATE)
    wf.writeframes(signal)
    wf.close()