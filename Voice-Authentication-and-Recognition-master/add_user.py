import pyaudio
import wave
import cv2
import os
import audioop
import time
import numpy as np
import random
import pickle
import requests
import re
import select
import sys
import threading
import speech_recognition
from scipy.io.wavfile import read
from IPython.display import Audio, display, clear_output
from main_functions import *
from threading import *
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO



r = speech_recognition.Recognizer()


def add_user():


    name = input("Enter Name:")
    dir = "./voice_database/" + name
    choice = input ("Enter number 0-10:")



    #Voice authentication
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 4


    os.mkdir(dir)

    for i in range(3):
        audio = pyaudio.PyAudio()

        if i == 0:
            time.sleep(1.0)
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Speak your number in {} seconds".format(2))
            time.sleep(2.0)

        elif i ==1:
            time.sleep(2.0)
            print("Speak your number one more time")
            time.sleep(0.8)

        else:
            time.sleep(2.0)
            print("Speak your number one last time")
            time.sleep(0.8)

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

        print("recording...")
        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        audio.terminate()
        waveFile = wave.open("temp" + '.wav', 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        harvard = speech_recognition.AudioFile('temp.wav')
        with harvard as source:
            print("Start reading file")
            audio2 = r.record(source,duration=4)
            print("File read")
            text = r.recognize_google(audio2, language='en-IN')
            print("Recognized number: ")
            print (text)
        os.remove('temp.wav')








        # saving wav file of speaker
        waveFile = wave.open(dir + '/' + str((i+1)) + '.wav', 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        print("Done")
    dest =  "./gmm_models/"
    count = 1

    for path in os.listdir(dir):
        path = os.path.join(dir, path)

        features = np.array([])

        # reading audio files of speaker
        (sr, audio) = read(path)

        # extract 40 dimensional MFCC & delta MFCC features
        vector   = extract_features(audio,sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))

        # when features of 3 files of speaker are concatenated, then do model training
        if count == 3:
            gmm = GMM(n_components = 16, n_iter = 200, covariance_type='diag',n_init = 3)
            gmm.fit(features)

            # saving the trained gaussian model
            pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
            print(name + ' added successfully')

            features = np.asarray(())
            count = 0
        count = count + 1

if __name__ == '__main__':
    add_user()
