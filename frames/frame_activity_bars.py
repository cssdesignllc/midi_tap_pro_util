from frames.frame_base import FrameBase
from midi.midi_uart_comm import MidiUartComm
from midi.midi_spec import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np


class FrameActivityBars(FrameBase):
    def __init__(self, parent, comm_manager: MidiUartComm):
        super().__init__(parent, comm_manager)

        self.parent = parent

        self.fig = Figure(figsize=(4, 4), dpi=100)
        self.plot1 = self.fig.add_subplot()
        columns = 17
        self.data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.bar = self.plot1.bar(range(columns), self.data, width=1, linewidth=0.7, edgecolor="white")
        self.plot1.set(xlim=(0, 17), xticks=np.arange(1, 17), ylim=(0, 128), yticks=[1, 32, 64, 96, 128])
        self.plot1.set_xlabel("Channels")
        self.plot1.set_title("MIDI Activity")

        canvas = FigureCanvasTkAgg(self.fig, master=parent)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, parent, pack_toolbar=False)
        toolbar.update()
        canvas.get_tk_widget().grid()

        parent.after(100, self.refresh)

    def refresh(self):
        for i in range(17):
            if self.data[i] > 0:
                self.data[i] = self.data[i] - 5
                if self.data[i] < 0:
                    self.data[i] = 0
            self.bar[i].set_height(self.data[i])
        self.fig.canvas.draw()
        self.parent.after(100, self.refresh)

    def rx_handler(self, message: MidiMessage):
        if type(message) == MidiNoteOn:
            if self.data[message.channel + 1] < message.velocity:
                self.data[message.channel + 1] = message.velocity
        if type(message) == MidiAftertouch:
            if self.data[message.channel + 1] < message.pressure:
                self.data[message.channel + 1] = message.pressure

