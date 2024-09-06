from tkinter import Canvas
from frames.frame_base import FrameBase
from midi.midi_uart_comm import MidiUartComm
from midi.midi_spec import *
import time


class ActivityIndicator:

    def __init__(self, name="", midi_message_type=None):
        self.name = name
        self.set = False
        self.tick = 0
        self.midi_message_type = midi_message_type


class FrameActivityIndicators(FrameBase):
    def __init__(self, parent, comm_manager: MidiUartComm):
        super().__init__(parent, comm_manager)

        self.parent = parent

        self.indicators = []
        self.indicators.append(ActivityIndicator("Note On", MidiNoteOn))
        self.indicators.append(ActivityIndicator("Note Off", MidiNoteOff))
        self.indicators.append(ActivityIndicator("Pitch Wheel", MidiPitchWheel))
        self.indicators.append(ActivityIndicator("Controller", MidiController))
        self.indicators.append(ActivityIndicator("Program Change", MidiProgramChange))
        self.indicators.append(ActivityIndicator("SysEx", MidiSysEx))
        self.indicators.append(ActivityIndicator("Quarter Frame", MidiQuarterFrame))
        self.indicators.append(ActivityIndicator("Clock", MidiClock))
        self.indicators.append(ActivityIndicator("Sense", MidiSense))
        self.indicators.append(ActivityIndicator("Reset", MidiReset))

        self.cv = Canvas(self, width=150, height=400)
        self.cv.grid()

        parent.after(250, self.refresh)

    def get_milliseconds(self):
        return round(time.time() * 1000)

    def refresh(self):
        x = 5
        y = 5
        self.cv.delete("all")
        for i in range(len(self.indicators)):
            if self.indicators[i].set:
                self.cv.create_oval(x, y, x + 20, y + 20, fill="red", width=1)
                if self.indicators[i].tick + 1000 < self.get_milliseconds():
                    self.indicators[i].set = False
            else:
                self.cv.create_oval(x, y, x + 20, y + 20, fill="gray", width=1)
            self.cv.create_text(x + 30, y + 10, text=self.indicators[i].name, width=200, anchor='w')
            y += 35
        self.parent.after(250, self.refresh)

    def rx_handler(self, message: MidiMessage):
        for i in range(len(self.indicators)):
            if type(message) == self.indicators[i].midi_message_type:
                self.indicators[i].set = True
                self.indicators[i].tick = self.get_milliseconds()

