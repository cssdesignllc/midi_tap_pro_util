from tkinter import Button, Entry, IntVar, Label
from frames.frame_base import FrameBase
from midi.midi_uart_comm import MidiUartComm
from midi.midi_spec import *


class FrameMessageSend(FrameBase):
    def __init__(self, parent, comm_manager: MidiUartComm):
        super().__init__(parent, comm_manager)

        self.parent = parent

        self.grid_columnconfigure(2, weight=1)

        # NOTE ON
        row = 0
        self.note_on_channel = IntVar()
        self.note_on_note = IntVar(value=64)
        self.note_on_velocity = IntVar(value=127)
        Button(self, text="Note On", width=15, command=self.note_on).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Channel").grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.note_on_channel).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Note").grid(column=3, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.note_on_note).grid(column=4, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Velocity").grid(column=5, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.note_on_velocity).grid(column=6, row=row, sticky='w', padx=5, pady=5)

        # NOTE OFF
        row += 1
        self.note_off_channel = IntVar()
        self.note_off_note = IntVar(value=64)
        self.note_off_velocity = IntVar(value=0)
        Button(self, text="Note Off", width=15, command=self.note_off).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Channel").grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.note_off_channel).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Note").grid(column=3, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.note_off_note).grid(column=4, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Velocity").grid(column=5, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.note_off_velocity).grid(column=6, row=row, sticky='w', padx=5, pady=5)

        # CONTROLLER
        row += 1
        self.controller_channel = IntVar()
        self.controller_controller = IntVar(value=0)
        self.controller_value = IntVar(value=0)
        Button(self, text="Controller", width=15, command=self.controller).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Channel").grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.controller_channel).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Controller").grid(column=3, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.controller_controller).grid(column=4, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Value").grid(column=5, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.controller_value).grid(column=6, row=row, sticky='w', padx=5, pady=5)

        # PROGRAM CHANGE
        row += 1
        self.program_change_channel = IntVar()
        self.program_change_value = IntVar(value=0)
        Button(self, text="Program Change", width=15, command=self.program_change).grid(column=0, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Channel").grid(column=1, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.program_change_channel).grid(column=2, row=row, sticky='w', padx=5, pady=5)
        Label(self, text="Value").grid(column=3, row=row, sticky='w', padx=5, pady=5)
        Entry(self, width=10, textvariable=self.program_change_value).grid(column=4, row=row, sticky='w', padx=5, pady=5)

        # RESET
        row += 1
        Button(self, text="Reset", width=15, command=self.reset).grid(column=0, row=row, sticky='w', padx=5, pady=5)

    def note_on(self):
        command = MidiNoteOn()
        command.channel = self.note_on_channel.get()
        command.note = self.note_on_note.get()
        command.velocity = self.note_on_velocity.get()
        self.comm_manager.write(command)

    def note_off(self):
        command = MidiNoteOff()
        command.channel = self.note_off_channel.get()
        command.note = self.note_off_note.get()
        command.velocity = self.note_off_velocity.get()
        self.comm_manager.write(command)

    def controller(self):
        command = MidiController()
        command.channel = self.controller_channel.get()
        command.note = self.controller_controller.get()
        command.velocity = self.controller_value.get()
        self.comm_manager.write(command)

    def program_change(self):
        command = MidiProgramChange()
        command.channel = self.program_change_channel.get()
        command.program = self.program_change_value.get()
        self.comm_manager.write(command)

    def reset(self):
        command = MidiReset()
        self.comm_manager.write(command)

    def rx_handler(self, message: MidiMessage):
        None

