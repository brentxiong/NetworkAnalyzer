import numpy
import struct
import pylab
import csv
import time
import datetime
import agilent
import visa

ag = agilent.ag8753e()
#ag.recall_state(1)
time.sleep(1)

return_loss_limit = -15

colors = ['y', 'c', 'm', 'g']
chans = [0, 1, 2, 3]
dt = {}
dts = {}
for i in open('testspec.txt').readlines():
    dt.setdefault(i.strip().split()[0],i.strip().split()[1])
dts = sorted(dt.iteritems(),key=lambda d:d[0])
print dts
for d,x in dts:
    print "key:" + d + ",value:" + str(x)
while True:
    raw_input('Enter to record data:')

    chandata = []

    flist = ag.get_freq_list()
    #print flist
    for chan in chans:
        ag.set_chan(chan)

        dat = ag.get_data()
        chandata.append(dat)
    #print chandata[0]
    for d,x in dts:
        minfreq = 6000000000
        flistmin = []
        targetfreq = float(d) * 1000000000
        print "targetfreq:", targetfreq
        for freq in flist:
            flistmin.append(abs(freq - targetfreq))
        #print flistmin
        #     
        print float(chandata[0][flistmin.index(min(flistmin))]),float(chandata[0][flistmin.index(min(flistmin))])<float(x),float(x),flistmin.index(min(flistmin))
        print float(chandata[3][flistmin.index(min(flistmin))]),float(chandata[3][flistmin.index(min(flistmin))])<float(x),float(x),flistmin.index(min(flistmin))
    '''
    pylab.figure(figsize=[16,16])
   
    for n, chan in enumerate(chans):
        pylab.subplot(2, 2, chan+1, title=ag.chanlabels[chan])
        
        pylab.plot(flist / 1E6, chandata[n], color=colors[chan])
        pylab.xlabel('Freq (MHz)')
        pylab.ylabel('Level (dB)')
        pylab.grid()
        axes = pylab.gca()
        if chan == 0 or chan == 3:
            axes.set_ylim([-40,-10]) # S11, S22
        else:
            axes.set_ylim([-70,-30]) # S21, S12
    #pylab.show()
    print datetime.datetime.now()
    if (max(chandata[0]) > return_loss_limit) or (max(chandata[3]) > return_loss_limit):
        print 'FAIL! FAIL! FAIL! FAIL! FAIL! FAIL!'
    else:
        print 'PASS!'

    fname = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    pylab.savefig('data/' + fname + '.png')
    f = open('data/' + fname + '.csv', 'wb')
    fcsv = csv.writer(f, dialect='excel')
    fcsv.writerow(['Freq'] + list(numpy.array(ag.chanlabels)[chans]))

    chandata = numpy.array(chandata)

    for fi, dat in zip(flist, chandata.T):
        fcsv.writerow([fi] + list(dat))

    f.close()

    pylab.close('all')
    '''
