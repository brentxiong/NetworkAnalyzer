import numpy
import struct
import pylab
import csv
import time
import datetime
import os
import glob

path = "D:\\vna\\data"
file_iter = 0

for filename in glob.glob(os.path.join(path, '*.csv')):
    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        freq_iter = 0
        for row in csvreader:
            freq_iter = freq_iter + 1
    file_iter = file_iter + 1

files = file_iter
freqs = freq_iter-1

print files

freq = [0 for x in range(freqs)]
max_s11 = [0 for x in range(freqs)]
min_s11 = [0 for x in range(freqs)]
max_s22 = [0 for x in range(freqs)]
min_s22 = [0 for x in range(freqs)]
max_s21 = [0 for x in range(freqs)]
min_s21 = [0 for x in range(freqs)]
s11 = [[0 for x in range(freqs)] for y in range(files)] 
s21 = [[0 for x in range(freqs)] for y in range(files)] 
s22 = [[0 for x in range(freqs)] for y in range(files)] 

file_iter = 0

for filename in glob.glob(os.path.join(path, '*.csv')):
    
    print filename

    with open(filename, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        freq_iter = 0
        for row in csvreader:
            if freq_iter != 0:
                freq[freq_iter-1] = row[0].split(",")[0]
                s11[file_iter][freq_iter-1] = row[0].split(",")[1]
                s21[file_iter][freq_iter-1] = row[0].split(",")[2]
                s22[file_iter][freq_iter-1] = row[0].split(",")[4]
            freq_iter = freq_iter + 1

    file_iter = file_iter + 1

for x in range(freqs):
    max_s11[x] = s11[0][x]
    min_s11[x] = s11[0][x]
    max_s22[x] = s22[0][x]
    min_s22[x] = s22[0][x]
    max_s21[x] = s21[0][x]
    min_s21[x] = s21[0][x]
    for y in range(1,files):
        if s11[y][x] < min_s11[x]:
            min_s11[x] = s11[y][x]
        if s11[y][x] > max_s11[x]:
            max_s11[x] = s11[y][x]
        if s22[y][x] < min_s22[x]:
            min_s22[x] = s22[y][x]
        if s22[y][x] > max_s22[x]:
            max_s22[x] = s22[y][x]
        if s21[y][x] < min_s21[x]:
            min_s21[x] = s21[y][x]
        if s21[y][x] > max_s21[x]:
            max_s21[x] = s21[y][x]

pylab.figure(figsize=[16,16])
pylab.plot(numpy.asarray(freq), numpy.asarray(max_s11), linewidth = 10)
pylab.plot(numpy.asarray(freq), numpy.asarray(min_s11), linewidth = 10)
for x in range(files):
    pylab.plot(numpy.asarray(freq), numpy.asarray(s11[x][:]))
pylab.xlabel('Freq (MHz)')
pylab.ylabel('S11 (dB)')
pylab.grid()
pylab.savefig('s11.png')

pylab.figure(figsize=[16,16])
pylab.plot(numpy.asarray(freq), numpy.asarray(max_s22), linewidth = 10)
pylab.plot(numpy.asarray(freq), numpy.asarray(min_s22), linewidth = 10)
for x in range(files):
    pylab.plot(numpy.asarray(freq), numpy.asarray(s22[x][:]))
pylab.xlabel('Freq (MHz)')
pylab.ylabel('S22 (dB)')
pylab.grid()
pylab.savefig('s22.png')

pylab.figure(figsize=[16,16])
pylab.plot(numpy.asarray(freq), numpy.asarray(max_s21), linewidth = 10)
pylab.plot(numpy.asarray(freq), numpy.asarray(min_s21), linewidth = 10)
for x in range(files):
    pylab.plot(numpy.asarray(freq), numpy.asarray(s21[x][:]))
pylab.xlabel('Freq (MHz)')
pylab.ylabel('S21 (dB)')
pylab.grid()
pylab.savefig('s21.png')
