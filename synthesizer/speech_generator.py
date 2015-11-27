__author__ = 'Chin'

import dictionary
import wave
import scikits.audiolab
import scipy
from pydub import AudioSegment

def generate_audio(phoneme_list):
    outfile = "output/output_audio.wav"
    data=[]

    for i in phoneme_list:
        w = wave.open(dictionary.sounds[i], 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])

    for i in range(0, len(phoneme_list), 1):
        output.writeframes(data[i][1])

    output.close()

def generate_audio2():

    a, fs, enc = scikits.audiolab.wavread('input/1.wav')
    b, fs, enc = scikits.audiolab.wavread('input/2.wav')
    c, fs, enc = scikits.audiolab.wavread('input/3.wav')
    d = scipy.vstack((a,b,c))
    scikits.audiolab.wavwrite(d, 'output/q.wav', fs, enc)

def generate_audio3(phoneme_list):

    for i in phoneme_list:
        combined_sounds = combined_sounds + AudioSegment.from_wav(dictionary.sounds[i])

    combined_sounds.export("output/output3.wav", format="wav")