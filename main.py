import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import serial.tools.list_ports
from tabs.tab_activity import TabActivity
from tabs.tab_midi_message import TabMidiMessage
from midi.midi_uart_comm import MidiUartComm


class MidiTapProApp(tk.Tk):

    def __init__(self):
        super().__init__()

        row = 0

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.comm_manager = MidiUartComm()
        self.uart_port_name = StringVar()

        self.title("CSS Designs - MIDI Tap Pro Utility - V1.0")
        self.geometry("1100x500")

        self.grid_columnconfigure(4, weight=1)

        # uart access
        self.tk_open_close_uart_button = ttk.Button(self, text="Open UART", command=self.open_close_uart_port)
        self.tk_open_close_uart_button.grid(column=0, row=row, padx=5, pady=5)

        Label(self, text="Serial Port").grid(row=row, column=1, padx=5, pady=5)

        self.tk_uart_ports_combo = ttk.Combobox(self, values=self.serial_ports(), state="readonly", textvariable=self.uart_port_name, width=40)
        self.tk_uart_ports_combo.grid(column=2, row=row, padx=5, pady=5)

        self.tk_refresh_uart_ports_button = ttk.Button(self, text="Refresh", command=self.refresh_uart_ports)
        self.tk_refresh_uart_ports_button.grid(column=3, row=row, padx=5, pady=5)

        row = row + 1

        ttk.Separator(self, orient='horizontal').grid(
            row=row, columnspan=5, sticky="we"
        )

        row = row + 1

        self.frame_tabs = tk.Frame(self)
        self.frame_tabs.grid(
            column=0, row=row, columnspan=10, padx=5, pady=5, sticky="ew"
        )

        self.tab_control = ttk.Notebook(self.frame_tabs)
        self.tab_control.enable_traversal()

        self.tab_activity = TabActivity(self.tab_control, self.comm_manager)
        self.tab_midi_message = TabMidiMessage(self.tab_control, self.comm_manager)

        self.tab_control.grid(column=0, row=0, columnspan=10, padx=5, pady=5, sticky="ew")

    def open_close_uart_port(self):
        if self.comm_manager.is_running:
            self.tk_open_close_uart_button.config(text="Open")
            self.tk_refresh_uart_ports_button.config(state="enabled")
            self.tk_uart_ports_combo.config(state="enabled")
            self.comm_manager.stop()
        else:
            if self.uart_port_name.get() == "":
                messagebox.showerror("error", "no port selected!")
                return
            if self.comm_manager.start(self.uart_port_name.get(),
                                       self.comm_manager_rx_callback):
                self.tk_open_close_uart_button.config(text="Close")
                self.tk_refresh_uart_ports_button.config(state="disabled")
                self.tk_uart_ports_combo.config(state="disabled")
            else:
                messagebox.showerror("error", "failed to open port!")

    def serial_ports(self):
        return [p.device for p in serial.tools.list_ports.comports()]

    def refresh_uart_ports(self):
        self.tk_uart_ports_combo.set('')
        self.tk_uart_ports_combo.config(values=self.serial_ports())
        if len(self.tk_uart_ports_combo["values"]) > 0:
            self.tk_uart_ports_combo.current(0)

    def comm_manager_rx_callback(self, midi_message):
        self.tab_activity.rx_handler(midi_message)
        self.tab_midi_message.rx_handler(midi_message)

    def on_closing(self):
        self.comm_manager.stop()
        self.destroy()


if __name__ == "__main__":
    Application = MidiTapProApp()
    Application.mainloop()
