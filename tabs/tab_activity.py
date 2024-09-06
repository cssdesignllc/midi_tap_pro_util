from tabs.tab_base import TabBase
from tkinter import ttk
from midi.midi_uart_comm import MidiUartComm
from midi.midi_spec import *
from frames.frame_activity_bars import FrameActivityBars
from frames.frame_activity_indicators import FrameActivityIndicators
from frames.frame_activity_raw import FrameActivityRaw


class TabActivity(TabBase):
    def __init__(self, master: ttk.Notebook, comm_manager: MidiUartComm):
        super().__init__(master, "Activity", comm_manager)

        self.frame_activity_bars = FrameActivityBars(self, self.comm_manager)
        self.frame_activity_bars.grid(column=0, row=0, padx=5, pady=5, sticky='n')

        self.frame_activity_indicators = FrameActivityIndicators(self, self.comm_manager)
        self.frame_activity_indicators.grid(column=1, row=0, padx=5, pady=5, sticky='n')

        self.frame_activity_raw = FrameActivityRaw(self, self.comm_manager)
        self.frame_activity_raw.grid(column=2, row=0, padx=5, pady=5, sticky='n')

    def rx_handler(self, message: MidiMessage):
        self.frame_activity_bars.rx_handler(message)
        self.frame_activity_indicators.rx_handler(message)
        self.frame_activity_raw.rx_handler(message)
        pass
