#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Freq Offset Helper
# Generated: Fri Jun 23 15:48:43 2017
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
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
import argparse
import numpy
import sip
import sys
from gnuradio import qtgui

def argument_parser():
    parser = argparse.ArgumentParser(description='Process some BAN constrains.')
    parser.add_argument('--GLFSR_degree',type=int,
                    help='degrees of the pseudo random data',default=3)
    parser.add_argument('--rand_seed',type=int,
                    help='seed to generate the pseudo random GLFSR and noise',default=1)
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
    return parser 


class Freq_offset_helper(gr.top_block, Qt.QWidget):

    def __init__(self,options = argument_parser().parse_args()):
        gr.top_block.__init__(self, "Freq Offset Helper")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Freq Offset Helper")
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

        self.settings = Qt.QSettings("GNU Radio", "Freq_offset_helper")
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
        self.dst = dst = 'C:\\Users\\cheny\\Documents\\Body-Area-Communication\\General Lib\\Files\\'
        self.carrier_freq = carrier_freq = options.carrier_freq
        self.GLFSR_degree = GLFSR_degree = options.GLFSR_degree
        self.offset_freq = offset_freq = 0.0
        self.TX_file_name = TX_file_name = dst+"GLFSR_"+str(GLFSR_degree)+"_"+str(rand_seed)+"_"+str(length)+"_"+str(int(samp_rate/1e3))+'K_'+str(int(carrier_freq/1000))+"K_"+str(int(fsk_deviation_hz/1000))+"K_"+str(int(noise_amp*100))+"_TX"
        self.SPS = SPS = int(samp_rate/fsk_deviation_hz/4)
        self.RX_file_name = RX_file_name = dst+"GLFSR_"+str(GLFSR_degree)+"_"+str(rand_seed)+"_"+str(length)+"_"+str(int(samp_rate/1e3))+'K_'+str(int(carrier_freq/1000))+"K_"+str(int(fsk_deviation_hz/1000))+"K_"+str(int(noise_amp*100))+"_RX"

        ##################################################
        # Blocks
        ##################################################
        self._offset_freq_range = Range(-50e3, 50e3, 1e3, 5050, 200)
        self._offset_freq_win = RangeWidget(self._offset_freq_range, self.set_offset_freq, "offset_freq", "counter_slider", float)
        self.top_layout.addWidget(self._offset_freq_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['TX', 'RX', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, RX_file_name, True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, TX_file_name, True)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, offset_freq, 1, 0)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.qtgui_freq_sink_x_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Freq_offset_helper")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_dummy(self):
        return self.dummy

    def set_dummy(self, dummy):
        self.dummy = dummy
        self.set_fsk_deviation_hz(2e4/self.dummy)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_TX")
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.set_SPS(int(self.samp_rate/self.fsk_deviation_hz/4))

    def get_rand_seed(self):
        return self.rand_seed

    def set_rand_seed(self, rand_seed):
        self.rand_seed = rand_seed
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_TX")
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_TX")
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_TX")
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_TX")
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")
        self.set_SPS(int(self.samp_rate/self.fsk_deviation_hz/4))

    def get_dst(self):
        return self.dst

    def set_dst(self, dst):
        self.dst = dst
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_TX")
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")

    def get_carrier_freq(self):
        return self.carrier_freq

    def set_carrier_freq(self, carrier_freq):
        self.carrier_freq = carrier_freq
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_TX")
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")

    def get_GLFSR_degree(self):
        return self.GLFSR_degree

    def set_GLFSR_degree(self, GLFSR_degree):
        self.GLFSR_degree = GLFSR_degree
        self.set_TX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_TX")
        self.set_RX_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length)+"_"+str(int(self.samp_rate/1e3))+'K_'+str(int(self.carrier_freq/1000))+"K_"+str(int(self.fsk_deviation_hz/1000))+"K_"+str(int(self.noise_amp*100))+"_RX")

    def get_offset_freq(self):
        return self.offset_freq

    def set_offset_freq(self, offset_freq):
        self.offset_freq = offset_freq
        self.analog_sig_source_x_0.set_frequency(self.offset_freq)

    def get_TX_file_name(self):
        return self.TX_file_name

    def set_TX_file_name(self, TX_file_name):
        self.TX_file_name = TX_file_name
        self.blocks_file_source_0.open(self.TX_file_name, True)

    def get_SPS(self):
        return self.SPS

    def set_SPS(self, SPS):
        self.SPS = SPS

    def get_RX_file_name(self):
        return self.RX_file_name

    def set_RX_file_name(self, RX_file_name):
        self.RX_file_name = RX_file_name
        self.blocks_file_source_0_0.open(self.RX_file_name, True)


def main(top_block_cls=Freq_offset_helper, options=None):

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
    print "TX file location: " + tb.TX_file_name
    print "RX file location: " + tb.RX_file_name
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
