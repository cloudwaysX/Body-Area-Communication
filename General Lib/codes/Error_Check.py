#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Error Check
# Author: Yifang Chen
# Generated: Wed Jul  5 16:28:11 2017
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
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import sip
import sys
from gnuradio import qtgui


class Error_Check(gr.top_block, Qt.QWidget):

    def __init__(self, demoded_file_name='test_out', dst='C:\\Users\\cheny\\Desktop\\', in_file_name='test_in', message="Here's an example of how GRC can be used to create a simulation environment. The following flow graph is available as part of the Channel Coding toolbox and was used to demonstrate the capabilities of the included Reed-Muller-Golay code. The original CGRAN server is offline, the code from the channel coding toolbox has been uploaded to github.com/ckuethe/gr-chancoding and is unlikely to work without some work to use newer GNU Radio APIs.A very important thing to observe is the use of the throttle block (the first block after the random source). This block only allows a certain amount of bits to pass the block (this is not an exact rate, but the average rate of bits leaving this block will be the given sampling rate). If you omit the throttle block, you risk your CPU running the flow graph at full speed .", message_repeatNum=3):
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
        # Parameters
        ##################################################
        self.demoded_file_name = demoded_file_name
        self.dst = dst
        self.in_file_name = in_file_name
        self.message = message
        self.message_repeatNum = message_repeatNum

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	len(message)*message_repeatNum*8, #size
        	samp_rate, #samp_rate
        	"", #name
        	3 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['Bit Error Rate', 'Reference Signal', 'Demoded Signal', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.blocks_throttle_1 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, len(message)*8, "packet_len")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, len(message)*8, "packet_len")
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_char*1, dst+in_file_name, False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, dst+demoded_file_name, False)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blks2_error_rate_0 = grc_blks2.error_rate(
        	type='BER',
        	win_size=len(message)*8,
        	bits_per_symbol=1,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_error_rate_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_1, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blks2_error_rate_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.blks2_error_rate_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_throttle_1, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Error_Check")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_demoded_file_name(self):
        return self.demoded_file_name

    def set_demoded_file_name(self, demoded_file_name):
        self.demoded_file_name = demoded_file_name
        self.blocks_file_source_0.open(self.dst+self.demoded_file_name, False)

    def get_dst(self):
        return self.dst

    def set_dst(self, dst):
        self.dst = dst
        self.blocks_file_source_0_0.open(self.dst+self.in_file_name, False)
        self.blocks_file_source_0.open(self.dst+self.demoded_file_name, False)

    def get_in_file_name(self):
        return self.in_file_name

    def set_in_file_name(self, in_file_name):
        self.in_file_name = in_file_name
        self.blocks_file_source_0_0.open(self.dst+self.in_file_name, False)

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len(len(self.message)*8)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len_pmt(len(self.message)*8)
        self.blocks_stream_to_tagged_stream_0.set_packet_len(len(self.message)*8)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(len(self.message)*8)

    def get_message_repeatNum(self):
        return self.message_repeatNum

    def set_message_repeatNum(self, message_repeatNum):
        self.message_repeatNum = message_repeatNum

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--demoded-file-name", dest="demoded_file_name", type="string", default='test_out',
        help="Set demoded_file_name [default=%default]")
    parser.add_option(
        "", "--dst", dest="dst", type="string", default='C:\\Users\\cheny\\Desktop\\',
        help="Set dst [default=%default]")
    parser.add_option(
        "", "--in-file-name", dest="in_file_name", type="string", default='test_in',
        help="Set in_file_name [default=%default]")
    parser.add_option(
        "", "--message-repeatNum", dest="message_repeatNum", type="intx", default=3,
        help="Set message_repeatNum [default=%default]")
    return parser


def main(top_block_cls=Error_Check, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(demoded_file_name=options.demoded_file_name, dst=options.dst, in_file_name=options.in_file_name, message_repeatNum=options.message_repeatNum)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
