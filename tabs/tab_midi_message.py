from tabs.tab_base import TabBase
from tkinter import ttk
from midi.midi_uart_comm import MidiUartComm
from midi.midi_spec import *
from frames.frame_message_send import FrameMessageSend


class TabMidiMessage(TabBase):
    def __init__(self, master: ttk.Notebook, comm_manager: MidiUartComm):
        super().__init__(master, "MIDI Message", comm_manager)

        self.frame_message_send = FrameMessageSend(self, comm_manager)
        self.frame_message_send.grid(column=0, row=0, padx=5, pady=5, sticky='n')

    def rx_handler(self, message: MidiMessage):
        self.frame_message_send.rx_handler(message)
        pass
