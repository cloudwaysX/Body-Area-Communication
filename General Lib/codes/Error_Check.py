#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Error Check
# Author: Yifang Chen
# Generated: Wed Jun 21 16:46:56 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
import argparse
import sys
import threading
import time
from gnuradio import qtgui


def argument_parser():
    parser = argparse.ArgumentParser(description='Process some BAN constrains.')
    parser.add_argument('--GLFSR_degree',type=int,
                    help='degrees of the pseudo random data',default=3)
    parser.add_argument('--rand_seed',type=int,
                    help='seed to generate the pseudo random GLFSR and noise',default=1)
    parser.add_argument('--RX_decimation',type=int,
                    help='Decimation number at RX to downsample and LPF',default=50)
    parser.add_argument('--samp_rate',type=float,
                    help='sample rate',default=4e6)
    parser.add_argument('--dummy',type=int,
                    help='a factor to control the frequncy deviation, 1e5/dummy',default=5)
    parser.add_argument('--carrier_freq',type=int,
                    help='carrier frequncy',default=270e3)
    parser.add_argument('--BER_windowSize',type=int,
                    help='number of the points you want to calcualte the bit error rate',default=100)
    parser.add_argument('--dst',type=str,
                    help='destination of folder the source signal located',default='C:\\Users\\cheny\\Documents\\Body-Area-Communication\\General Lib\\Files\\')
    parser.add_argument('--length',type=int,
                    help='length of signal, better to be 2**x',default=2**14)
    parser.add_argument('--noise_amp',type=float,
                    help='amplitute for gaussian noise (refer to signal amp =1)',default=0.0)
    return parser 



class Error_Check(gr.top_block, Qt.QWidget):

    def __init__(self, options = argument_parser().parse_args()):
        gr.top_block.__init__(self, "Error Check")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Error Check")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Error_Check")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.dummy = dummy = options.dummy
        self.samp_rate = samp_rate = options.samp_rate
        self.rand_seed = rand_seed = options.rand_seed
        self.noise_amp = noise_amp = options.noise_amp
        self.length = length = options.length
        self.fsk_deviation_hz = fsk_deviation_hz = 2e4/dummy
        self.dst = dst = options.dst
        self.carrier_freq = carrier_freq = options.carrier_freq
        self.RX_decimation = RX_decimation = options.RX_decimation
        self.GLFSR_degree = GLFSR_degree = options.GLFSR_degree
        self.in_file_name = in_file_name = dst+"GLFSR_"+str(GLFSR_degree)+"_"+str(rand_seed)+"_"+str(length)+"_"+str(int(samp_rate/1e3))+'K'
        self.demod_file_name = demod_file_name = dst+"GLFSR_"+str(GLFSR_degree)+"_"+str(rand_seed)+"_"+str(length)+"_"+str(int(samp_rate/1e3))+'K_'+str(int(carrier_freq/1000))+"K_"+str(int(fsk_deviation_hz/1000))+"K_"+str(int(noise_amp*100))+"_"+str(RX_decimation)+"_demod"
        self.delay = delay = 0
        self.FindDelay = FindDelay = 0
        self.BER_windowSize = BER_windowSize = options.BER_windowSize
        self.SPS = SPS = int(samp_rate/fsk_deviation_hz/4)


        ##################################################
        # Blocks
        ##################################################
        self.probe_BER = blocks.probe_signal_f()
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, in_file_name, True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, demod_file_name, True)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, delay)
        self.blks2_error_rate_0 = grc_blks2.error_rate(
        	type='BER',
        	win_size=BER_windowSize,
        	bits_per_symbol=1,
        )

        def _FindDelay_probe():
            while True:
                val = self.probe_BER.level()
                the_delay=self.get_delay()
                if (val > 0.3) and (val < 0.7):
                    self.set_delay(the_delay+1)
                else:
                    print "At delay = " + str(the_delay) + ", BER = "+str(val)
                try:
                    self.set_FindDelay(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _FindDelay_thread = threading.Thread(target=_FindDelay_probe)
        _FindDelay_thread.daemon = True
        _FindDelay_thread.start()



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_error_rate_0, 0), (self.probe_BER, 0))
        self.connect((self.blocks_delay_0, 0), (self.blks2_error_rate_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.blks2_error_rate_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Error_Check")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_dummy(self):
        return self.dummy

    def set_dummy(self, dummy):
        self.dummy = dummy
        self.set_fsk_deviation_hz(1e5/self.dummy)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_in_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K')
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_rand_seed(self):
        return self.rand_seed

    def set_rand_seed(self, rand_seed):
        self.rand_seed = rand_seed
        self.set_in_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K')
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length
        self.set_in_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K')
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")

    def get_dst(self):
        return self.dst

    def set_dst(self, dst):
        self.dst = dst
        self.set_in_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K')
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")

    def get_RX_decimation(self):
        return self.RX_decimation

    def set_RX_decimation(self, RX_decimation):
        self.RX_decimation = RX_decimation
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")

    def get_GLFSR_degree(self):
        return self.GLFSR_degree

    def set_GLFSR_degree(self, GLFSR_degree):
        self.GLFSR_degree = GLFSR_degree
        self.set_in_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K')
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")

    def get_in_file_name(self):
        return self.in_file_name

    def set_in_file_name(self, in_file_name):
        self.in_file_name = in_file_name
        self.blocks_file_source_0_0.open(self.in_file_name, True)

    def get_demod_file_name(self):
        return self.demod_file_name

    def set_demod_file_name(self, demod_file_name):
        self.demod_file_name = demod_file_name
        self.blocks_file_source_0.open(self.demod_file_name, True)

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(self.delay)

    def get_FindDelay(self):
        return self.FindDelay

    def set_FindDelay(self, FindDelay):
        self.FindDelay = FindDelay

    def get_BER_windowSize(self):
        return self.BER_windowSize

    def set_BER_windowSize(self, BER_windowSize):
        self.BER_windowSize = BER_windowSize


def main(top_block_cls=Error_Check, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    ##################################################
    #print out the variable information
    ##################################################
    print "ref file name: "+tb.in_file_name
    print "demoded file name: "+tb.demod_file_name
    print "GLFSR_degree = " + str(tb.GLFSR_degree)
    print "rand_seed = " + str(tb.rand_seed)
    print "BER_windowSize = " + str(tb.BER_windowSize)
    print "samp_rate = " + str(tb.samp_rate)
    print "fsk_deviation_hz = " + str(tb.fsk_deviation_hz)
    print "RX_decimation = " + str(tb.RX_decimation)
    print "carrier_frequncy = " + str(tb.carrier_freq)
    print "SPS = " + str(tb.SPS)
    print "baud_rate = " + str(tb.samp_rate/tb.SPS)
    print "================================================="

    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
