#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Msk Fsk Demod
# Generated: Wed Jun 21 16:14:31 2017
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
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
import argparse
import math
import numpy
import sys
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
    parser.add_argument('--dst',type=str,
                    help='destination of folder the source signal located',default='C:\\Users\\cheny\\Documents\\Body-Area-Communication\\General Lib\\Files\\')
    parser.add_argument('--length',type=int,
                    help='length of signal, better to be 2**x',default=2**14)
    parser.add_argument('--noise_amp',type=float,
                    help='amplitute for gaussian noise (refer to signal amp =1)',default=0.0)
    parser.add_argument('--offset_freq',type=float,
                    help='adjust the frequncy offset between the channel',default=0.0)
    return parser 


class MSK_FSK_demod(gr.top_block, Qt.QWidget):

    def __init__(self,options = argument_parser().parse_args()):
        gr.top_block.__init__(self, "Msk Fsk Demod")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Msk Fsk Demod")
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

        self.settings = Qt.QSettings("GNU Radio", "MSK_FSK_demod")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.dummy = dummy = options.dummy
        self.samp_rate = samp_rate = options.samp_rate
        self.fsk_deviation_hz = fsk_deviation_hz = 2e4/dummy
        self.rand_seed = rand_seed = options.rand_seed
        self.noise_amp = noise_amp = options.noise_amp
        self.nfilts = nfilts = 64
        self.length = length = options.length
        self.dst = dst = options.dst
        self.carrier_freq = carrier_freq = options.carrier_freq
        self.SPS = SPS = int(samp_rate/fsk_deviation_hz/4)
        self.RX_decimation = RX_decimation = options.RX_decimation
        self.GLFSR_degree = GLFSR_degree = options.GLFSR_degree
        self.EBW = EBW = .05
        self.offset_freq = offset_freq = options.offset_freq
        self.demod_file_name = demod_file_name = dst+"GLFSR_"+str(GLFSR_degree)+"_"+str(rand_seed)+"_"+str(length)+"_"+str(int(samp_rate/1e3))+'K_'+str(int(carrier_freq/1000))+"K_"+str(int(fsk_deviation_hz/1000))+"K_"+str(int(noise_amp*100))+"_"+str(RX_decimation)+"_demod"
        self.TX_file_name = TX_file_name = dst+"GLFSR_"+str(GLFSR_degree)+"_"+str(rand_seed)+"_"+str(length)+"_"+str(int(samp_rate/1e3))+'K_'+str(int(carrier_freq/1000))+"K_"+str(int(fsk_deviation_hz/1000))+"K_"+str(int(noise_amp*100))+"_TX"

        self.RRC_filter_taps = RRC_filter_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0, EBW, 5*SPS*nfilts/RX_decimation)


        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=RX_decimation,
                taps=None,
                fractional_bw=None,
        )
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_fff(SPS/RX_decimation, 6.28/400.0*2/70, (RRC_filter_taps), nfilts, nfilts/2, 2, 1)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_threshold_ff_1 = blocks.threshold_ff(0.5, 0.5, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0, 0, 0)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_head_0 = blocks.head(gr.sizeof_char*1, length*8)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, TX_file_name, True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, demod_file_name, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -carrier_freq, 1, 0)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(samp_rate/(2*math.pi*fsk_deviation_hz/8.0)/(RX_decimation))
        self.analog_pwr_squelch_xx_0_0 = analog.pwr_squelch_cc(-60, .01, 0, True)
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(1024, 1.0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.analog_pwr_squelch_xx_0_0, 0), (self.analog_feedforward_agc_cc_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.blocks_threshold_ff_1, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.blocks_threshold_ff_1, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_pwr_squelch_xx_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "MSK_FSK_demod")
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
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")
        self.set_SPS(int(self.samp_rate/self.fsk_deviation_hz/4))
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*self.fsk_deviation_hz/8.0)/(self.RX_decimation))

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")
        self.set_SPS(int(self.samp_rate/self.fsk_deviation_hz/4))
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*self.fsk_deviation_hz/8.0)/(self.RX_decimation))

    def get_rand_seed(self):
        return self.rand_seed

    def set_rand_seed(self, rand_seed):
        self.rand_seed = rand_seed
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")
        self.blocks_head_0.set_length(self.length*8)

    def get_dst(self):
        return self.dst

    def set_dst(self, dst):
        self.dst = dst
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")
        self.analog_sig_source_x_0.set_frequency(-self.carrier_freq)

    def get_SPS(self):
        return self.SPS

    def set_SPS(self, SPS):
        self.SPS = SPS

    def get_RX_decimation(self):
        return self.RX_decimation

    def set_RX_decimation(self, RX_decimation):
        self.RX_decimation = RX_decimation
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*self.fsk_deviation_hz/8.0)/(self.RX_decimation))

    def get_GLFSR_degree(self):
        return self.GLFSR_degree

    def set_GLFSR_degree(self, GLFSR_degree):
        self.GLFSR_degree = GLFSR_degree
        self.set_demod_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_"+str(self.RX_decimation)+"_demod")
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")

    def get_EBW(self):
        return self.EBW

    def set_EBW(self, EBW):
        self.EBW = EBW

    def get_offset_freq(self):
        return self.offset_freq

    def set_offset_freq(self, offset_freq):
        self.offset_freq = offset_freq
        self.analog_sig_source_x_0.set_frequency(-self.carrier_freq+self.offset_freq)

    def get_demod_file_name(self):
        return self.demod_file_name

    def set_demod_file_name(self, demod_file_name):
        self.demod_file_name = demod_file_name
        self.blocks_file_sink_0.open(self.demod_file_name)

    def get_TX_file_name(self):
        return self.TX_file_name

    def set_TX_file_name(self, TX_file_name):
        self.TX_file_name = TX_file_name
        self.blocks_file_source_0.open(self.TX_file_name, True)

    def get_RRC_filter_taps(self):
        return self.RRC_filter_taps

    def set_RRC_filter_taps(self, RRC_filter_taps):
        self.RRC_filter_taps = RRC_filter_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.RRC_filter_taps))


def main(top_block_cls=MSK_FSK_demod, options=None):

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
    print "in file location: " + tb.TX_file_name
    print "GLFSR_degree = " + str(tb.GLFSR_degree)
    print "rand_seed = " + str(tb.rand_seed)
    print "samp_rate = " + str(tb.samp_rate)
    print "fsk_deviation_hz = " + str(tb.fsk_deviation_hz)
    print "RX_decimation = " + str(tb.RX_decimation)
    print "carrier_frequncy = " + str(tb.carrier_freq)
    print "SPS = " + str(tb.SPS)
    print "baud_rate = " + str(tb.samp_rate/tb.SPS)
    print "offset_freq = " + str(tb.offset_freq)
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
