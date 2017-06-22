#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Msk Fsk Mod
# Generated: Wed Jun 21 15:21:15 2017
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
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
import argparse
import numpy
import sys
from gnuradio import qtgui

def argument_parser():
    parser = argparse.ArgumentParser(description='Process some BAN constrains.')
    parser.add_argument('--GLFSR_degree',type=int,
                    help='degrees of the pseudo random data',default=3)
    parser.add_argument('--rand_seed',type=int,
                    help='seed to generate the pseudo random GLFSR and noise',default=1)
    parser.add_argument('--samp_rate',type=float,
                    help='sample rate',default=20e6)
    parser.add_argument('--dummy',type=int,
                    help='a factor to control the frequncy deviation, 1e5/dummy',default=10)
    parser.add_argument('--carrier_freq',type=int,
                    help='carrier frequncy',default=1.75e6)
    parser.add_argument('--dst',type=str,
                    help='destination of folder the source signal located',default='C:\\Users\\cheny\\Documents\\Body-Area-Communication\\General Lib\\Files\\')
    parser.add_argument('--length',type=int,
                    help='length of signal, better to be 2**x',default=2**14)
    parser.add_argument('--noise_amp',type=float,
                    help='amplitute for gaussian noise (refer to signal amp =1)',default=0.0)

    return parser 



class MSK_FSK_mod(gr.top_block, Qt.QWidget):

    def __init__(self,options = argument_parser().parse_args()):
        gr.top_block.__init__(self, "Msk Fsk Mod")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Msk Fsk Mod")
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

        self.settings = Qt.QSettings("GNU Radio", "MSK_FSK_mod")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.dummy = dummy = options.dummy
        self.samp_rate = samp_rate = options.samp_rate
        self.rand_seed = rand_seed = options.rand_seed
        self.length = length = options.length
        self.fsk_deviation_hz = fsk_deviation_hz = 1e5/dummy
        self.dst = dst = options.dst
        self.carrier_freq = carrier_freq = options.carrier_freq
        self.GLFSR_degree = GLFSR_degree = options.GLFSR_degree
        self.noise_amp = noise_amp = options.noise_amp
        self.in_file_name = in_file_name = dst+"GLFSR_"+str(GLFSR_degree)+"_"+str(rand_seed)+"_"+str(length)+"_"+str(int(samp_rate/1e3))+'K'
        self.SPS = SPS = int(samp_rate/fsk_deviation_hz/4)
        self.RX_file_name = RX_file_name = dst+"GLFSR_"+str(GLFSR_degree)+"_"+str(rand_seed)+"_"+str(length)+"_"+str(int(samp_rate/1e3))+'K_'+str(int(carrier_freq/1000))+"K_"+str(int(fsk_deviation_hz/1000))+"K_"+str(int(noise_amp*100))+"_RX"

        ##################################################
        # Blocks
        ##################################################
        self.digital_chunks_to_symbols_xx_0_0_0_0_0 = digital.chunks_to_symbols_bf(((2*3.14*carrier_freq-2*3.14*fsk_deviation_hz,2*3.14*carrier_freq+2*3.14*fsk_deviation_hz)), 1)
        self.blocks_vco_f_0_0_0_0 = blocks.vco_f(samp_rate, 1, 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_repeat_0_0_0_0 = blocks.repeat(gr.sizeof_float*1, SPS-1)
        self.blocks_head_0 = blocks.head(gr.sizeof_float*1, SPS*length*16)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, in_file_name, True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, RX_file_name, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, noise_amp, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_repeat_0_0_0_0, 0), (self.blocks_vco_f_0_0_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0_0_0, 0))
        self.connect((self.blocks_vco_f_0_0_0_0, 0), (self.blocks_head_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0_0_0, 0), (self.blocks_repeat_0_0_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "MSK_FSK_mod")
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
        self.set_SPS(int(self.samp_rate/self.fsk_deviation_hz/4))
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K")
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_rand_seed(self):
        return self.rand_seed

    def set_rand_seed(self, rand_seed):
        self.rand_seed = rand_seed
        self.set_in_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K')
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K")

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length
        self.set_in_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K')
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K")
        self.blocks_head_0.set_length(self.SPS*self.length*16)

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.set_SPS(int(self.samp_rate/self.fsk_deviation_hz/4))
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K")
        self.digital_chunks_to_symbols_xx_0_0_0_0_0.set_symbol_table(((2*3.14*self.carrier_freq-2*3.14*self.fsk_deviation_hz,2*3.14*self.carrier_freq+2*3.14*self.fsk_deviation_hz)))

    def get_dst(self):
        return self.dst

    def set_dst(self, dst):
        self.dst = dst
        self.set_in_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K')
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K")

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K")
        self.digital_chunks_to_symbols_xx_0_0_0_0_0.set_symbol_table(((2*3.14*self.carrier_freq-2*3.14*self.fsk_deviation_hz,2*3.14*self.carrier_freq+2*3.14*self.fsk_deviation_hz)))

    def get_GLFSR_degree(self):
        return self.GLFSR_degree

    def set_GLFSR_degree(self, GLFSR_degree):
        self.GLFSR_degree = GLFSR_degree
        self.set_in_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K')
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K")

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp
        self.analog_noise_source_x_0.set_amplitude(self.noise_amp)

    def get_in_file_name(self):
        return self.in_file_name

    def set_in_file_name(self, in_file_name):
        self.in_file_name = in_file_name
        self.blocks_file_source_0.open(self.in_file_name, True)

    def get_SPS(self):
        return self.SPS

    def set_SPS(self, SPS):
        self.SPS = SPS
        self.blocks_repeat_0_0_0_0.set_interpolation(self.SPS-1)
        self.blocks_head_0.set_length(self.SPS*self.length*16)

    def get_RX_file_name(self):
        return self.RX_file_name

    def set_RX_file_name(self, RX_file_name):
        self.RX_file_name = RX_file_name
        self.blocks_file_sink_0.open(self.RX_file_name)

    def get_RX_decimation(self):
        return self.RX_decimation

    def set_RX_decimation(self, RX_decimation):
        self.RX_decimation = RX_decimation


def main(top_block_cls=MSK_FSK_mod, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    ##################################################
    #print out the variable information
    ##################################################
    print "length = " + str(tb.length)
    print "in file location: " + tb.in_file_name
    print "GLFSR_degree = " + str(tb.GLFSR_degree)
    print "rand_seed = " + str(tb.rand_seed)
    print "samp_rate = " + str(tb.samp_rate)
    print "fsk_deviation_hz = " + str(tb.fsk_deviation_hz)
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
