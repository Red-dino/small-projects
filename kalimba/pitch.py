import pyaudio
import sys
import numpy as np
import aubio
import random
import time

# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
buffer_size = 1024
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)

# setup pitch
tolerance = 0.8
win_s = 4096 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

active = False
consec = 0
running_total = 0
running_weight = 0

notes = [
    (60.0, "C, 1"), # 0
    (62.0, "D, 2"), # 1
    (64.0, "E, 3"), # 2
    (65.0, "F, 4"), # 3
    (67.0, "G, 5"), # 4
    (69.0, "A, 6"), # 5
    (71.0, "B, 7"), # 6
    (72.0, "C, 1*"), # 7
    (74.0, "D, 2*"), # 8
    (76.0, "E, 3*"), # 9
    (77.0, "F, 4*"), # 10
    (79.0, "G, 5*"), # 11
    (81.0, "A, 6*"), # 12
    (83.0, "B, 7*"), # 13
    (84.0, "C, 1**"), # 14
    (86.0, "D, 2**"), # 15
    (88.0, "E, 3**"), # 16
]

note_mapper = {
    "1" : 0,
    "2" : 1,
    "3" : 2,
    "4" : 3,
    "5" : 4,
    "6" : 5,
    "7" : 6,
    "1*" : 7,
    "2*" : 8,
    "3*" : 9,
    "4*" : 10,
    "5*" : 11,
    "6*" : 12,
    "7*" : 13,
    "1**" : 14,
    "2**" : 15,
    "3**" : 16,
}

print("Let's begin.")

use_random = False

song = [
    "1*", "2", "1",
    "1*", "2", "1", "6",
    "1*", "2", "1",
    "1*", "2", "1",
    "1*", "2", "1",
    "1*", "2", "1", "6",
    "1*", "2", "1",
    "1*", "2", "1",

    "1*", "7", "5",
    "1*", "7", "3",
    "1*", "7", "5",
    "1*", "7", "1",
    
    "1*", "7", "5",
    "1*", "7", "3",
    "2*", "3*", "5*",
    "1*", "3*", "5*", "1*",
    
    "7", "6", "3",
    "7", "6", "3",
    "7", "1*", "5",
    "4", "3", "1",
    
    "2*", "3*", "1*",
    "2*", "3*", "5*",
    "7*", "1**", "5*",
    "7*", "1**", "1",

    "1*", "7", "5",
    "1*", "7", "3",
    "1*", "7", "5",
    "1*", "7", "1",

    "1*", "2*", "5",
    "1*", "2*", "3",
    "7*", "1**", "5*",
    "1**", "7*", "1",

    "1*", "7", "5",
    "1*", "7", "5", "2",
    "1*", "7", "5", "4", "3",

    "1*", "7", "5",
    "1*", "7", "3",
    "2*", "6*", "5*",
    "3*", "5*", "2*", "1*"

    "1**", "6*", "5*",
    "3*", "5*", "6*",
    "5*", "6*", "5*",
    "3*", "5*", "2*", "1*",
]

if use_random:
    current_note = random.randint(0, 16)
else:
    current_note = note_mapper[song[0]]

start = time.time()
average = 0
instances = 0

ignore_window = 0

print("I want %s." % notes[current_note][1])

while True:
    try:
        audiobuffer = stream.read(buffer_size)
        signal = np.frombuffer(audiobuffer, dtype=np.float32)

        pitch = pitch_o(signal)[0]
        confidence = pitch_o.get_confidence()
        
        if ignore_window > 0:
            ignore_window -= 1
            continue

        if pitch > 10 and confidence > 0.90:
            active = True
            consec += 1
            running_total += pitch * confidence
            running_weight += confidence
#             print("{} / {}".format(pitch,confidence))
        elif active:
            active = False
            consec = 0
            
            final = running_total / running_weight
            goal = notes[current_note][0]
            if final > goal - 0.1 and final < goal + 0.1:
                elapsed = time.time() - start
                print("Good! It took you %.1f seconds." % elapsed)
                instances += 1
                average += elapsed
                start = time.time()
                
                if use_random:
                    current_note = random.randint(0, 16)
                else:
                    if instances == len(song):
                        break
                    current_note = note_mapper[song[instances]]

                print("I want %s." % notes[current_note][1])
                ignore_window = 50

            running_total = 0
            running_weight = 0
            
        if consec == 10:
            active = False
            consec = 0
            
            final = running_total / running_weight
            goal = notes[current_note][0]
            if final > goal - 0.1 and final < goal + 0.1:
                elapsed = time.time() - start
                print("Good! It took you %.1f seconds." % elapsed)
                instances += 1
                average += elapsed
                start = time.time()
                
                if use_random:
                    current_note = random.randint(0, 16)
                else:
                    if instances == len(song):
                        break
                    current_note = note_mapper[song[instances]]

                print("I want %s." % notes[current_note][1])
                ignore_window = 50

            running_total = 0
            running_weight = 0
            
    except KeyboardInterrupt:
        print("All done?")
        break

print("Thanks for playing!")
print("You played %d notes, averaging %.1f seconds." % (instances, average / instances))
stream.stop_stream()
stream.close()
p.terminate()