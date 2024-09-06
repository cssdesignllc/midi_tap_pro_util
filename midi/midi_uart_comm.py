import serial
import threading
from midi.midi_spec import *


class MidiUartComm:

    def __init__(self):
        self.serial_port = serial.Serial()
        self.rx_callback = None
        self.is_running = False

    def start(self, port_name, rx_callback):
        if self.is_running:
            print("failed to start! already connected!")
            return True
        self.rx_callback = rx_callback
        self.serial_port.port = port_name
        try:
            self.serial_port.open()
            thread_handle = threading.Thread(target=self.comm_thread)
            thread_handle.start()
        except:
            print("open exception!")
            return False
        return True

    def stop(self):
        try:
            self.is_running = False
            if self.serial_port.is_open:
                self.serial_port.close()
        except:
            print("close exception!")

    def write(self, message: MidiMessage):
        if not self.is_running:
            print("serial port not open!")
            return
        try:
            packet = message.serialize()
            #print(packet)
            self.serial_port.write(packet)
        except:
            print("serial port write exception!")

    def comm_thread(self):
        self.is_running = True
        midi_message = MidiMessage()
        first_byte = True
        print("enter client thread")

        try:
            while self.is_running:
                rx_bytes = self.serial_port.read(1)
                for i in range(len(rx_bytes)):
                    #print(str(counter) + ":" + hex(rx_bytes[i]))
                    if first_byte:
                        if (rx_bytes[i] & 0xF0) == MidiMessageType.NOTE_ON.value:
                            midi_message = MidiNoteOn()
                        elif (rx_bytes[i] & 0xF0) == MidiMessageType.NOTE_OFF.value:
                            midi_message = MidiNoteOff()
                        elif (rx_bytes[i] & 0xF0) == MidiMessageType.AFTERTOUCH.value:
                            midi_message = MidiAftertouch()
                        elif (rx_bytes[i] & 0xF0) == MidiMessageType.CONTROLLER.value:
                            midi_message = MidiController()
                        elif (rx_bytes[i] & 0xF0) == MidiMessageType.PROGRAM_CHANGE.value:
                            midi_message = MidiProgramChange()
                        elif (rx_bytes[i] & 0xF0) == MidiMessageType.CHANNEL_PRESSURE.value:
                            midi_message = MidiChannelPressure()
                        elif (rx_bytes[i] & 0xF0) == MidiMessageType.PITCH_WHEEL.value:
                            midi_message = MidiPitchWheel()
                        elif (rx_bytes[i] & 0xF0) == 0xF0:
                            if rx_bytes[i] == MidiMessageType.SYSEX_START.value:
                                midi_message = MidiSysEx()
                            elif rx_bytes[i] == MidiMessageType.QUARTER_FRAME.value:
                                midi_message = MidiQuarterFrame()
                            elif rx_bytes[i] == MidiMessageType.SONG_POSITION.value:
                                midi_message = MidiSongPosition()
                            elif rx_bytes[i] == MidiMessageType.SONG_SELECT.value:
                                midi_message = MidiSongSelect()
                            elif rx_bytes[i] == MidiMessageType.TUNE_REQUEST.value:
                                midi_message = MidiTuneRequest()
                            elif rx_bytes[i] == MidiMessageType.CLOCK.value:
                                midi_message = MidiClock()
                            elif rx_bytes[i] == MidiMessageType.START.value:
                                midi_message = MidiStart()
                            elif rx_bytes[i] == MidiMessageType.CONTINUE.value:
                                midi_message = MidiContinue()
                            elif rx_bytes[i] == MidiMessageType.STOP.value:
                                midi_message = MidiStop()
                            elif rx_bytes[i] == MidiMessageType.SENSE.value:
                                midi_message = MidiSense()
                            elif rx_bytes[i] == MidiMessageType.RESET.value:
                                midi_message = MidiReset()
                            else:
                                print("unknown midi system message " + str(rx_bytes[i]))
                                midi_message = MidiMessage()
                        else:
                            print("unknown midi voice message " + str(rx_bytes[i]))
                            midi_message = MidiMessage()
                        first_byte = False
                    if type(midi_message) == MidiMessage:
                        first_byte = True
                    elif midi_message.append(rx_bytes[i]):
                        #print("got midi message: " + str(type(midi_message)))
                        midi_message.deserialize()
                        self.rx_callback(midi_message)
                        first_byte = True
        except Exception as ex:
            print("read exception!" + ex)

        self.stop()
        self.is_running = False

        print("leave client thread")
