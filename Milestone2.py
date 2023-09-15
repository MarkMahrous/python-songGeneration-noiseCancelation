''' The libraries that we used are numpy , matplotlib.pyplot and sounddevice'''
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy.fftpack import fft
import math


''' The total time of the song is 6 seconds starting from zero for 2*12*1024 samples'''
𝑡 = np.linspace(0,6,2*12*1024)


''' F_array representing the frequences chosen from the thrid octave with the left hand
    f_array representing the frequences chosen from the fourth octave with the right hand'''
F_array = np.array([174.61, 146.83, 130.81, 246.93/2, 164.81, 130.81, 246.93/2, 220/2])
f_array = np.array([174.61*2, 146.83*2, 130.81*2, 246.93, 164.81*2, 130.81*2, 246.93, 220])


''' t_array representing the starting time values of each tone
    T_array representing the period time values of each tone'''
t_array = np.array([0, 1.2, 1.4, 1.6, 2.5, 3.7, 3.9, 4.1])
T_array = np.array([0.3, 0.1, 0.1, 0.1, 0.3, 0.1, 0.1, 0.1])

 
''' "N" representing number of pairs of notes so it equals 8 as we have 8 frequencies in each hand
    "c" representing a counter to go from the first element in the whole arrays (index 0) till the last
    element (index N-1=7)
    "x" representing the accumulator to sum all the tones
    while loop to loop over the 4 arrays and get frequencies and corresponding starting and periodic
    time one by one to create the tones which we store in the accumulator "x"'''
N=8
c=0
x=0
while (c<N):
    Fi = F_array[c]
    fi = f_array[c]
    ti = t_array[c]
    Ti = T_array[c]
    Notei = np.sin(2*np.pi*Fi*t)
    notei = np.sin(2*np.pi*fi*t)
    x = x + (Notei+notei)*((t>=ti)&(t<=(ti+Ti)))
    c = c+1

''' We have now the generated song in variable "x" so we can finally plot it in the time domain
    using plt.plot(t,x) and play the song to hear it usnig sd.play(x,3*1024)'''
#plt.plot(t,x)
#sd.play(x,3*1024)

'''We set the number of samples 𝑁 to 6*1024 and the frequency axis range'''    
N = 6*1024
f = np. linspace(0 , 512 , int(N/2))

'''We converted the song without noise from the time domain to the frequency domain'''
x_f = fft(x)
x_f = 2/N * np.abs(x_f [0:np.int(N/2)])

'''We generated two random integer frequencies to represent the noise added to the song'''
fn1 , fn2 = np. random. randint(0, 512, 2)
n = np.sin(2*np.pi*fn1*t)+np.sin(2*np.pi*fn2*t)

'''We added the noise to the song then converted it to the frequency domain'''
xn = x+n
xn_f = fft(xn)
xn_f = 2/N * np.abs(xn_f [0:np.int(N/2)])

'''We created z which contains array of indecies of the two random frequencies
   and their types then we get the indecies of the two frequencies'''
z = np.where(xn_f>math.ceil(np.max(x)))
index1 = z[0][0]
index2 = z[0][1]

''' we got the frequencies by getting the value at the indices on the frequency axis'''
found1 = int(f[index1])
found2 = int(f[index2])

'''We filtered the song from noise'''
xFiltered = xn - (np.sin(2*np.pi*found1*t)+np.sin(2*np.pi*found2*t))

'''We played the filtered song to get the same sound as the original one'''
sd.play(xFiltered, 3*1024)

'''We converted the filtered song to frequency domain to plot it in both time & frequency domain'''
xFiltered_f = fft(xFiltered)
xFiltered_f = 2/N * np.abs(xFiltered_f [0:np.int(N/2)])

'''We figured the the graphs in the time domain alone'''
plt.figure()
plt.subplot(3,1,1)
plt.plot(t,x)
plt.subplot(3,1,2)
plt.plot(t,xn)
plt.subplot(3,1,3)
plt.plot(t,xFiltered)

'''We figured the graphs in the frequency domain alone'''
plt.figure()
plt.subplot(3,1,1)
plt.plot(f,x_f)
plt.subplot(3,1,2)
plt.plot(f,xn_f)
plt.subplot(3,1,3)
plt.plot(f,xFiltered_f)

