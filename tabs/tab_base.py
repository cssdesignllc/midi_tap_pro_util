import abc
from tkinter import Frame
from tkinter import ttk
from midi.midi_uart_comm import MidiUartComm
from midi.midi_spec import *


class TabBase(Frame):
    def __init__(self, master: ttk.Notebook, tab_name: str, comm_manager: MidiUartComm):
        super().__init__(master)

        self.comm_manager = comm_manager
        master.add(self, text=tab_name)

    def send_command(self, message: MidiMessage):
        self.comm_manager.write(message)

    @abc.abstractmethod
    def rx_handler(self, message: MidiMessage):
        pass
