import abc
from tkinter import Frame
from midi.midi_uart_comm import MidiUartComm
from midi.midi_spec import *


class FrameBase(Frame):
    def __init__(self, parent, comm_manager: MidiUartComm):
        super().__init__(parent)

        self.comm_manager = comm_manager
        self.parent = parent

    def send_message(self, message: MidiMessage):
        self.comm_manager.write(message)

    @abc.abstractmethod
    def rx_handler(self, message: MidiMessage):
        pass

