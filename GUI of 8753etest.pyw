import numpy
import struct
import pylab
import csv
import time
import datetime
import agilent
import visa
from Tkinter import *

def test(event):
    text.delete(0.0,END)
    text.insert(INSERT,"Test start\r\n")
    chandata = [] 
    label['text'] = "Testing"
    label['background'] = 'yellow'
    flist = ag.get_freq_list()
    top.update()
    for chan in chans:
        ag.set_chan(chan)

        dat = ag.get_data()
        chandata.append(dat)

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

    print datetime.datetime.now()
    '''
    if (max(chandata[0]) > return_loss_limit) or (max(chandata[3]) > return_loss_limit):
        print 'FAIL! FAIL! FAIL! FAIL! FAIL! FAIL!'
        label['text'] = "FAIL"
        label['background'] = 'red'
    else:
        print 'PASS!'
        label['text'] = "PASS"
        label['background'] = 'green'
    '''
    dt = {}
    dts = {}
    result = True
    for i in open('testspec.txt').readlines():
        dt.setdefault(i.strip().split()[0],i.strip().split()[1])
        dts = sorted(dt.iteritems(),key=lambda d:d[0])    
    for d,x in dts:
        minfreq = 6000000000
        flistmin = []
        targetfreq = float(d) * 1000000000
        print "targetfreq:", targetfreq
        for freq in flist:
            flistmin.append(abs(freq - targetfreq))
        #print flistmin
        #     
        print float(chandata[0][flistmin.index(min(flistmin))]), \
              float(chandata[0][flistmin.index(min(flistmin))])<float(x),\
              float(x),\
              flistmin.index(min(flistmin))
        print float(chandata[3][flistmin.index(min(flistmin))]),\
              float(chandata[3][flistmin.index(min(flistmin))])<float(x),\
              float(x),\
              flistmin.index(min(flistmin))
        if(float(chandata[0][flistmin.index(min(flistmin))])<float(x)) is False:
            text.insert(INSERT,"LHCP:\r\n")
            text.insert(INSERT,"[" + d + "GHz]: " + str(x) + "dB < ")
            text.insert(INSERT,str(chandata[0][flistmin.index(min(flistmin))])[0:6])
            text.insert(INSERT,"dB -> ")
            text.insert(INSERT,str(float(chandata[0][flistmin.index(min(flistmin))])<float(x)) + "\r\n")
            #show test result
            result = False
        if(float(chandata[3][flistmin.index(min(flistmin))])<float(x)) is False:
            text.insert(INSERT,"RHCP:\r\n")
            text.insert(INSERT,"[" + d + "GHz]: " + str(x) + "dB < ")
            text.insert(INSERT,str(chandata[3][flistmin.index(min(flistmin))])[0:6])
            text.insert(INSERT,"dB -> ")
            text.insert(INSERT,str(float(chandata[3][flistmin.index(min(flistmin))])<float(x)) + "\r\n")
            #show test result
            result = False
    if result is False:
        print 'FAIL! FAIL! FAIL! FAIL! FAIL! FAIL!'
        label['text'] = "FAIL"
        label['background'] = 'red'
    else:
        print 'PASS!'
        label['text'] = "PASS"
        label['background'] = 'green'
    if(e.get()!= ""):        
        fname = e.get() + "-" + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    else:
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
    e.delete(0,END)
    e.focus_set()
    text.insert(INSERT,"Test finished\r\n")
root = Tk()
root.geometry('560x650+150+10')
root.resizable(False,False)
top = Frame(root,height=600,width=600)
top.grid()

root.title("A5-18, A5-14 Antenna Tester(V1.1 2016-08-20)  Mimosa Networks")
top.columnconfigure(0,minsize=1)
top.columnconfigure(1,minsize=100)

label = Label(top, text='Ready',font=("Ariel",64,"normal"),bg='yellow')
label.grid(row=0,column=0,padx=2,pady=2,sticky=W+E,columnspan=2)

label2 = Label(top, text='SN',font=("Ariel",24,"normal"))
label2.grid(row=1,column=0,padx=2,pady=2,sticky=W)
e = Entry(top, text='input sn',font=("Ariel",24,"bold"))
e.grid(row=2,column=0,padx=2,pady=2,columnspan=2,sticky=W+E)
e.focus_set()
e.bind("<Return>",test)

b = Button(top,text='Test',font=('aril',64,"normal"))
b.grid(row=3,column=0,padx=2,pady=2,sticky=W+E,columnspan=2)
#b.focus_set()
b.bind("<Button-1>",test)

label3 = Label(top, text='Message')
label3.grid(row=4,column=0,padx=2,pady=2,columnspan=2,sticky=W)
text = Text(top)
text.grid(row=5,column=0,padx=2,pady=2,columnspan=2,sticky=W+E)

ag = agilent.ag8753e()
#ag.recall_state(1)
time.sleep(1)

return_loss_limit = -15

colors = ['y', 'c', 'm', 'g']
chans = [0, 1, 2, 3]



top.mainloop()    
