#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Glfsr Msk Block2
# Generated: Fri Jun 16 13:16:19 2017
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
from grc_gnuradio import blks2 as grc_blks2
import argparse
import math
import numpy
import sys
import threading
import time
from gnuradio import qtgui

def argument_parser():
    parser = argparse.ArgumentParser(description='Process some BAN constrains.')
    parser.add_argument('--GLFSR_degree',type=int,
                    help='degrees of the pseudo random data',default=6)
    parser.add_argument('--noise_amp',type=float,
                    help='amplitude of the simulated gaussian noise',default=0.0)
    parser.add_argument('--rand_seed',type=int,
                    help='seed to generate the pseudo random GLFSR and noise',default=1)

    return parser     


class GLFSR_MSK_Block2(gr.top_block, Qt.QWidget):

    def __init__(self, hdr_format=digital.header_format_default(digital.packet_utils.default_access_code, 0),options = argument_parser().parse_args()):
        gr.top_block.__init__(self, "Glfsr Msk Block2")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Glfsr Msk Block2")
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

        self.settings = Qt.QSettings("GNU Radio", "GLFSR_MSK_Block2")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.hdr_format = hdr_format

        ##################################################
        # Variables
        ##################################################
        self.dummy = dummy = 10
        self.samp_rate = samp_rate = 45.6e6/2
        self.fsk_deviation_hz = fsk_deviation_hz = 1e5/dummy
        self.nfilts = nfilts = 64
        self.SPS = SPS = int(samp_rate/fsk_deviation_hz/4)
        self.RX_decimation = RX_decimation = 19*3
        self.EBW = EBW = .05
        self.rand_seed = rand_seed = options.rand_seed
        self.noise_amp = noise_amp = options.noise_amp
        self.delay = delay = 0
        self.carrier_freq = carrier_freq = 1.75e6

        self.RRC_filter_taps = RRC_filter_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0, EBW, 5*SPS*nfilts/RX_decimation)

        self.GLFSR_degree = GLFSR_degree = options.GLFSR_degree
        self.FindDelay = FindDelay = 0


        ##################################################
        # Blocks
        ##################################################
        self.probe_BER = blocks.probe_signal_f()
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=RX_decimation,
                taps=None,
                fractional_bw=None,
        )
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_fff(SPS/RX_decimation, 6.28/400.0*2/70, (RRC_filter_taps), nfilts, nfilts/2, 2, 1)
        self.digital_glfsr_source_x_0 = digital.glfsr_source_b(GLFSR_degree, True, 0, rand_seed)
        self.digital_chunks_to_symbols_xx_0_0_0_0_0 = digital.chunks_to_symbols_bf(((2*3.14*carrier_freq-2*3.14*fsk_deviation_hz,2*3.14*carrier_freq+2*3.14*fsk_deviation_hz)), 1)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vco_f_0_0_0_0 = blocks.vco_f(samp_rate, 1, 1)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_repeat_0_0_0_0 = blocks.repeat(gr.sizeof_float*1, SPS-1)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, SPS-1)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, delay)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blks2_error_rate_0 = grc_blks2.error_rate(
            type='BER',
            win_size=1000,
            bits_per_symbol=1,
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -carrier_freq, 1, 0)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(samp_rate/(2*math.pi*fsk_deviation_hz/8.0)/(RX_decimation))
        self.analog_pwr_squelch_xx_0_0 = analog.pwr_squelch_cc(-60, .01, 0, True)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, 0, rand_seed)
        self.analog_feedforward_agc_cc_0 = analog.feedforward_agc_cc(1024, 1.0)

        def _FindDelay_probe():
            print "test GLFSR_degree = " + str(self.GLFSR_degree)
            while True:
                val = self.probe_BER.level()
                the_delay=self.get_delay()
                if val > 0.2:
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
        self.connect((self.analog_feedforward_agc_cc_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_pwr_squelch_xx_0_0, 0), (self.analog_feedforward_agc_cc_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.blks2_error_rate_0, 0), (self.probe_BER, 0))
        self.connect((self.blocks_delay_0, 0), (self.blks2_error_rate_0, 1))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_repeat_0_0_0_0, 0), (self.blocks_vco_f_0_0_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blks2_error_rate_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0_0_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_vco_f_0_0_0_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0_0_0, 0), (self.blocks_repeat_0_0_0_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_pwr_squelch_xx_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "GLFSR_MSK_Block2")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_dummy(self):
        return self.dummy

    def set_dummy(self, dummy):
        self.dummy = dummy
        self.set_fsk_deviation_hz(1e5/self.dummy)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_SPS(int(self.samp_rate/self.fsk_deviation_hz/4))
        self.qtgui_time_sink_x_0_0_0_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*self.fsk_deviation_hz/8.0)/(self.RX_decimation))

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.set_SPS(int(self.samp_rate/self.fsk_deviation_hz/4))
        self.digital_chunks_to_symbols_xx_0_0_0_0_0.set_symbol_table(((2*3.14*self.carrier_freq-2*3.14*self.fsk_deviation_hz,2*3.14*self.carrier_freq+2*3.14*self.fsk_deviation_hz)))
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*self.fsk_deviation_hz/8.0)/(self.RX_decimation))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts

    def get_SPS(self):
        return self.SPS

    def set_SPS(self, SPS):
        self.SPS = SPS
        self.blocks_repeat_0_0_0_0.set_interpolation(self.SPS-1)
        self.blocks_repeat_0.set_interpolation(self.SPS-1)

    def get_RX_decimation(self):
        return self.RX_decimation

    def set_RX_decimation(self, RX_decimation):
        self.RX_decimation = RX_decimation
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*self.fsk_deviation_hz/8.0)/(self.RX_decimation))

    def get_EBW(self):
        return self.EBW

    def set_EBW(self, EBW):
        self.EBW = EBW

    def get_rand_seed(self):
        return self.rand_seed

    def set_rand_seed(self, rand_seed):
        self.rand_seed = rand_seed

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        if delay > 200:
            print "FAIL TO SYSCHRONIZE!"
            exit()
        self.delay = delay
        self.blocks_delay_0.set_dly(self.delay)

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.digital_chunks_to_symbols_xx_0_0_0_0_0.set_symbol_table(((2*3.14*self.carrier_freq-2*3.14*self.fsk_deviation_hz,2*3.14*self.carrier_freq+2*3.14*self.fsk_deviation_hz)))
        self.analog_sig_source_x_0.set_frequency(-self.carrier_freq)

    def get_RRC_filter_taps(self):
        return self.RRC_filter_taps

    def set_RRC_filter_taps(self, RRC_filter_taps):
        self.RRC_filter_taps = RRC_filter_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.RRC_filter_taps))

    def get_GLFSR_degree(self):
        return self.GLFSR_degree

    def set_GLFSR_degree(self, GLFSR_degree):
        self.GLFSR_degree = GLFSR_degree

    def get_FindDelay(self):
        return self.FindDelay

    def set_FindDelay(self, FindDelay):
        self.FindDelay = FindDelay


def main(top_block_cls=GLFSR_MSK_Block2):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    ##################################################
    #print out the variable information
    ##################################################
    print "GLFSR_degree = " + str(tb.GLFSR_degree)
    print "Gaussian Noise Amplitute = " + str(tb.noise_amp)
    print "rand_seed = " + str(tb.rand_seed)

    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
