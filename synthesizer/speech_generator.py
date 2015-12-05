__author__ = 'Chin'

import dictionary
import wave
import scikits.audiolab
import scipy
from pydub import AudioSegment
import os

package_directory = os.path.dirname(os.path.abspath(__file__))

def generate_audio(phoneme_list):
    outfile = package_directory + "/output/output_audio.wav"
    data=[]

    for i in phoneme_list:
        w = wave.open(package_directory + "/" + dictionary.sounds[i], 'rb')
        data.append([w.getparams(), w.readframes(w.getnframes())])
        w.close()

    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])

    for i in range(0, len(phoneme_list), 1):
        output.writeframes(data[i][1])

    output.close()

    # audio = wave.open(outfile, 'rb')
    # rate = audio.getframerate()
    # rate2 = audio.getparams()
    # audio.close()
    # audio2 = wave.open(outfile, 'wb')
    # audio2.setframerate(2*rate)
    # audio2.setparams(rate2)
    # audio2.close()

    return data

def generate_audio2():

    a, fs, enc = scikits.audiolab.wavread(package_directory+'/input/1.wav')
    b, fs, enc = scikits.audiolab.wavread(package_directory+'/input/2.wav')
    c, fs, enc = scikits.audiolab.wavread(package_directory+'/input/3.wav')
    d = scipy.vstack((a,b,c))
    scikits.audiolab.wavwrite(d, package_directory+'/output/q.wav', fs, enc)

def generate_audio3(phoneme_list):

    combined_sounds = AudioSegment.from_wav(dictionary.sounds[phoneme_list[0]])
    for i in range(1, len(phoneme_list), 1):
        combined_sounds = combined_sounds + AudioSegment.from_wav(package_directory+"/"+dictionary.sounds[phoneme_list[i]])

    combined_sounds.export(package_directory+"/output/output3.wav", format="wav")