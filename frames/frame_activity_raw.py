from tkinter import Listbox, Button, Label, Checkbutton, IntVar
from frames.frame_base import FrameBase
from midi.midi_uart_comm import MidiUartComm
from midi.midi_spec import *
import tkinter as tk
import datetime


class FrameActivityRaw(FrameBase):
    def __init__(self, parent, comm_manager: MidiUartComm):
        super().__init__(parent, comm_manager)

        self.parent = parent
        self.is_paused = False
        self.message_count = IntVar(value=0)
        self.raw_data = []

        self.grid_columnconfigure(2, weight=1)

        Label(self, text="MIDI Raw Activity").grid(column=0, row=0, sticky='w', padx=5, pady=5)

        Button(self, text="clear", width=10, command=self.clear_data).grid(column=1, row=0, sticky='w', padx=5, pady=5)

        Checkbutton(self, text="pause", width=10, command=self.pause_data).grid(column=2, row=0, sticky='w', padx=5, pady=5)

        self.label_message_count = Label(self, textvariable=self.message_count)
        self.label_message_count.grid(column=3, row=0, sticky='e', padx=5, pady=5)

        self.list_raw = Listbox(self, width=80, height=22)
        self.list_raw.grid(column=0, row=1, columnspan=4, padx=5, pady=5)

        parent.after(100, self.refresh)

    def refresh(self):
        for i in range(len(self.raw_data)):
            self.list_raw.insert(0, self.raw_data[i])
        self.list_raw.delete(100, tk.END)
        self.raw_data = []
        self.parent.after(100, self.refresh)

    def clear_data(self):
        self.list_raw.delete(0, tk.END)

    def pause_data(self):
        self.is_paused = not self.is_paused

    def rx_handler(self, message: MidiMessage):
        if not self.is_paused:
            self.message_count.set(self.message_count.get() + 1)
            now = datetime.datetime.now()
            self.raw_data.append(now.strftime('%H:%M:%S.%f: ') + message.to_string())


