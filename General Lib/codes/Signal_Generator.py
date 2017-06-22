#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Signal Generator
# Author: Yifang Chen
# Description: Generate 2 bits infomation as digital signal
# Generated: Wed Jun 21 14:33:31 2017
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
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
import argparse
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
    parser.add_argument('--dst',type=str,
                    help='destination of folder the source signal located',default='C:\\Users\\cheny\\Documents\\Body-Area-Communication\\General Lib\\Files\\')
    parser.add_argument('--length',type=int,
                    help='length of signal, better to be 2**x',default=2**14)
    return parser 



class Signal_Generator(gr.top_block, Qt.QWidget):

    def __init__(self,options = argument_parser().parse_args()):
        gr.top_block.__init__(self, "Signal Generator")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Signal Generator")
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

        self.settings = Qt.QSettings("GNU Radio", "Signal_Generator")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.rand_seed = rand_seed = options.rand_seed
        self.length = length = options.length
        self.dst = dst = options.dst
        self.GLFSR_degree = GLFSR_degree = options.GLFSR_degree
        self.samp_rate = samp_rate = options.samp_rate
        self.file_name = file_name = dst+"GLFSR_"+str(GLFSR_degree)+"_"+str(rand_seed)+"_"+str(length)+"_"+str(int(samp_rate/1e3))+'K'

        ##################################################
        # Blocks
        ##################################################
        self.digital_glfsr_source_x_0 = digital.glfsr_source_b(GLFSR_degree, True, 0, rand_seed)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_head_0 = blocks.head(gr.sizeof_char*1, length)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, file_name, False)
        self.blocks_file_sink_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_head_0, 0))
        self.connect((self.digital_glfsr_source_x_0, 0), (self.blocks_throttle_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Signal_Generator")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_rand_seed(self):
        return self.rand_seed

    def set_rand_seed(self, rand_seed):
        self.rand_seed = rand_seed
        self.set_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length))

    def get_length(self):
        return self.length

    def set_length(self, length):
        self.length = length
        self.set_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length))
        self.blocks_head_0.set_length(self.length)

    def get_dst(self):
        return self.dst

    def set_dst(self, dst):
        self.dst = dst
        self.set_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length))

    def get_GLFSR_degree(self):
        return self.GLFSR_degree

    def set_GLFSR_degree(self, GLFSR_degree):
        self.GLFSR_degree = GLFSR_degree
        self.set_file_name(self.dst+"GLFSR_"+str(self.GLFSR_degree)+"_"+str(self.rand_seed)+"_"+str(self.length))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_file_name(self):
        return self.file_name

    def set_file_name(self, file_name):
        self.file_name = file_name
        self.blocks_file_sink_0.open(self.file_name)


def main(top_block_cls=Signal_Generator, options=None):

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
    print "rand_seed = " + str(tb.rand_seed)
    print "samp_rate = " + str(tb.samp_rate)
    print "length = " + str(tb.length)
    print "file location: " + tb.file_name
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
