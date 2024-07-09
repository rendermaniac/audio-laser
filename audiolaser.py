#!/usr/bin/env python

import time
import math
import pigpio

import numpy as np
import soundfile as sf

PWM0 = 12
IN1 = 20
IN2 = 21

pi = pigpio.pi()
if not pi.connected:
   exit(0)

pi.set_mode(IN1, pigpio.OUTPUT)
pi.set_mode(IN2, pigpio.OUTPUT)
pi.set_mode(PWM0, pigpio.OUTPUT)

# set H bridge to "forwards"
pi.write(IN1, 0)
pi.write(IN2, 1)

pi.set_PWM_frequency(PWM0, 40000)
pi.set_PWM_range(PWM0, 1000)
print(f"Frequency set to {pi.get_PWM_frequency(PWM0)}")

#data, samplerate = sf.read('/home/sibun/never_gonna_give_you_up.ogg')
#print("finsihed reading file")

# print(data.size)
# print(data.shape)
# print(data.max())
# print(samplerate)

volume = 0.5  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
duration = 5.0  # in seconds, may be float
f = 440.0  # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)


for sample in samples:
    amp = abs(sample * 1000) # int(sample[0] * 1000)
    pi.set_PWM_dutycycle(PWM0, amp)
    print(f"playing sample amp {amp}")
    time.sleep(1.0/float(fs))

pi.stop()
