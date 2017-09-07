import visa
import struct
import numpy

class hp8673b:
    chanlist = {34 : 5170,
                35 : 5175,
                36 : 5180,
                37 : 5185,
                38 : 5190,
                39 : 5195,
                40 : 5200,
                41 : 5205,
                42 : 5210,
                43 : 5215,
                44 : 5220,
                45 : 5225,
                46 : 5230,
                47 : 5235,
                48 : 5240,
                50 : 5250,
                52 : 5260,
                54 : 5270,
                56 : 5280,
                58 : 5290,
                60 : 5300,
                62 : 5310,
                64 : 5320,
                100 : 5500,
                102 : 5510,
                104 : 5520,
                106 : 5530,
                108 : 5540,
                110 : 5550,
                112 : 5560,
                114 : 5570,
                116 : 5580,
                118 : 5590,
                120 : 5600,
                122 : 5610,
                124 : 5620,
                126 : 5630,
                128 : 5640,
                130 : 5650,
                132 : 5660,
                134 : 5670,
                136 : 5680,
                138 : 5690,
                140 : 5700,
                147 : 5735,
                149 : 5745,
                151 : 5755,
                153 : 5765,
                155 : 5575,
                157 : 5785,
                159 : 5795,
                161 : 5805,
                163 : 5815,
                165 : 5825,
                }

    def __init__(self, addr=19):
        self.ag = visa.instrument('GPIB1::%i' %addr)
        #print self.ag.ask('IDN?')


    def setfreq(self, chan=159, offset=0):
        self.ag.write('FR%.3fMZ' %(self.chanlist[chan] + offset * 1000))


    def setlevel(self, level=-60):
        self.ag.write('LE%+.1fDM' %level)


    def setoutput(self, output=1):
        if output:
            self.ag.write('RF1')        
        else:
            self.ag.write('RF0')


class hp438a:

    def __init__(self, addr=13, gpib=0):
        self.ag = visa.instrument('GPIB%i::%i' %(gpib, addr))
        print self.ag.ask('?ID')
        self.ag.write('LG')


    def read(self):
        val = self.ag.ask('TR1')
        return float(val)


    def setref(self, refon=True):
        if refon:
            self.ag.write('OC1')
        else:
            self.ag.write('OC0')


    def zero(self):
        self.ag.write('ZE')


    def setcalfactor(self, calfactor=1.):
        self.ag.write('KB %.1f EN' %(calfactor*100))


    def setoffset(self, offset=0):
        self.ag.write('OS %f EN' %offset)



class ag34401a:
    def __init__(self, addr=10):
        try:
            self.ag = visa.instrument('GPIB1::%i' %addr)
        except visa.VisaIOError:
            print 'Instrument not found'
            raise ValueError


    def readvoltage(self):
        reading = self.ag.ask('MEAS:VOLT:DC?')
        return float(reading)


class ag8753e:
    chanlabels = ['S11', 'S21', 'S12', 'S22']
    channels = [1, 2, 3, 4]

    def __init__(self, addr=16):
        self.ag = visa.instrument('GPIB0::%i::INSTR' %addr)
        print self.ag.ask('*IDN?')
        self.ag.write('FORM5')


    def recall_state(self, stateval=29):
        self.ag.write('RECAREG%02i' %stateval)


    def get_sweep_params(self):
        fstart = float(self.ag.ask('STAR?'))
        fstop = float(self.ag.ask('STOP?'))
        points = float(self.ag.ask('POIN?'))
        fstep = (fstop - fstart) / (points - 1)
        
        return fstart, fstop, fstep, points


    def set_chan(self, chan = 0):
        self.ag.write('CHAN%i' %self.channels[chan])


    def get_data(self):
        dat = self.ag.ask('OUTPFORM')

        datverify = struct.unpack('2cH', dat[:4])
        #print datverify
        assert datverify[0] == '#'
        assert datverify[1] == 'A'
        datlen = datverify[2]

        data = struct.unpack('%if' %(len(dat[4:])/4), dat[4:])
        return data[::2]


    def get_freq_list(self):
        fstart, fstop, fstep, points = self.get_sweep_params()

        return numpy.arange(fstart, fstop + fstep, fstep)
