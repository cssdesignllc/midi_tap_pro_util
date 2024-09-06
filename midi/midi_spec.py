from enum import Enum


class MidiMessageType(Enum):
    NOTE_OFF = 0x80
    NOTE_ON = 0x90
    AFTERTOUCH = 0xA0
    CONTROLLER = 0xB0
    PROGRAM_CHANGE = 0xC0
    CHANNEL_PRESSURE = 0xD0
    PITCH_WHEEL = 0xE0
    SYSEX_START = 0xF0
    QUARTER_FRAME = 0xF1
    SONG_POSITION = 0xF2
    SONG_SELECT = 0xF3
    TUNE_REQUEST = 0xF6
    SYSEX_END = 0xF7
    CLOCK = 0xF8
    START = 0xFA
    CONTINUE = 0xFB
    STOP = 0xFC
    SENSE = 0xFE
    RESET = 0xFF


class MidiMessage:

    def __init__(self):
        self.channel = 1
        self.rx_packet = bytearray()
        self.message_length = 0

    def serialize(self):
        return bytearray()

    def deserialize(self):
        return True

    def to_string(self):
        return ""

    def append(self, rx_byte):
        self.rx_packet.append(rx_byte)
        if len(self.rx_packet) == self.message_length:
            return True
        return False


class MidiNoteOff(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.NOTE_OFF
        self.note = 64
        self.velocity = 0
        self.message_length = 3

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.NOTE_OFF.value | (self.channel & 0x0F))
        packet.append(self.note & 0x7F)
        packet.append(self.velocity & 0x7F)
        return packet

    def deserialize(self):
        if len(self.rx_packet) == self.message_length:
            self.channel = self.rx_packet[0] & 0x0F
            self.note = self.rx_packet[1] & 0x7F
            self.velocity = self.rx_packet[2] & 0x7F
            return True
        return False

    def to_string(self):
        return "Note Off: channel " + str(self.channel) + ", note " + str(self.note) + ", velocity " + str(self.velocity)


class MidiNoteOn(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.NOTE_ON
        self.note = 64
        self.velocity = 64
        self.message_length = 3

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.NOTE_ON.value | (self.channel & 0x0F))
        packet.append(self.note & 0x7F)
        packet.append(self.velocity & 0x7F)
        return packet

    def deserialize(self):
        if len(self.rx_packet) == self.message_length:
            self.channel = self.rx_packet[0] & 0x0F
            self.note = self.rx_packet[1] & 0x7F
            self.velocity = self.rx_packet[2] & 0x7F
            return True
        return False

    def to_string(self):
        return "Note On: channel " + str(self.channel) + ", note " + str(self.note) + ", velocity " + str(self.velocity)


class MidiAftertouch(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.AFTERTOUCH
        self.note = 64
        self.pressure = 64
        self.message_length = 3

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.AFTERTOUCH.value & (self.channel & 0x0F))
        packet.append(self.note & 0x7F)
        packet.append(self.pressure & 0x7F)
        return packet

    def deserialize(self):
        if len(self.rx_packet) == self.message_length:
            self.channel = self.rx_packet[0] & 0x0F
            self.note = self.rx_packet[1] & 0x7F
            self.pressure = self.rx_packet[2] & 0x7F
            return True
        return False

    def to_string(self):
        return "Aftertouch: channel " + str(self.channel) + ", note " + str(self.note) + ", pressure " + str(self.pressure)


class MidiController(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.CONTROLLER
        self.controller = 0
        self.value = 0
        self.message_length = 3

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.CONTROLLER.value | (self.channel & 0x0F))
        packet.append(self.controller & 0x7F)
        packet.append(self.value & 0x7F)
        return packet

    def deserialize(self):
        if len(self.rx_packet) == self.message_length:
            self.channel = self.rx_packet[0] & 0x0F
            self.controller = self.rx_packet[1] & 0x7F
            self.value = self.rx_packet[2] & 0x7F
            return True
        return False

    def to_string(self):
        return "Controller: channel " + str(self.channel) + ", controller " + str(self.controller) + ", value " + str(self.value)


class MidiProgramChange(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.PROGRAM_CHANGE
        self.program = 0
        self.message_length = 2

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.PROGRAM_CHANGE.value | (self.channel & 0x0F))
        packet.append(self.program & 0x7F)
        return packet

    def deserialize(self):
        if len(self.rx_packet) == self.message_length:
            self.channel = self.rx_packet[0] & 0x0F
            self.program = self.rx_packet[1] & 0x7F
            return True
        return False

    def to_string(self):
        return "Program change: channel " + str(self.channel) + ", program " + str(self.program)


class MidiChannelPressure(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.CHANNEL_PRESSURE
        self.pressure = 0
        self.message_length = 2

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.CHANNEL_PRESSURE.value | (self.channel & 0x0F))
        packet.append(self.pressure & 0x7F)
        return packet

    def deserialize(self):
        if len(self.rx_packet) == self.message_length:
            self.channel = self.rx_packet[0] & 0x0F
            self.pressure = self.rx_packet[1] & 0x7F
            return True
        return False

    def to_string(self):
        return "Channel Pressure: channel " + str(self.channel) + ", pressure " + str(self.pressure)


class MidiPitchWheel(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.PITCH_WHEEL
        self.value = 0
        self.message_length = 3

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.PITCH_WHEEL.value | (self.channel & 0x0F))
        packet.append(self.value & 0x7F)
        packet.append((self.value >> 7) & 0x7F)
        return packet

    def deserialize(self):
        if len(self.rx_packet) == self.message_length:
            self.channel = self.rx_packet[0] & 0x0F
            self.value = (self.rx_packet[1] & 0x7F) + ((self.rx_packet[2] & 0x7F) << 7)
            return True
        return False

    def to_string(self):
        return "Pitch Wheel: channel " + str(self.channel) + ", value " + str(self.value)


class MidiSysEx(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.SYSEX_START
        self.payload = bytearray()

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.SYSEX_START.value)
        for i in range(len(self.payload)):
            packet.append(self.payload[i] & 0x7F)
        packet.append(MidiMessageType.SYSEX_END.value)
        return packet

    def deserialize(self):
        self.payload.clear()
        for i in range(len(self.rx_packet)):
            if self.rx_packet[i] != MidiMessageType.SYSEX_START.value and self.rx_packet[i] != MidiMessageType.SYSEX_END.value:
                self.payload.append(self.rx_packet[i])
        return True

    def append(self, rx_byte):
        self.rx_packet.append(rx_byte)
        if rx_byte == MidiMessageType.SYSEX_END.value:
            return True
        return False

    def to_string(self):
        result = "SysEx: "
        for i in range(len(self.payload)):
            result += " " + f'{self.payload[i]:x}'
        return result


class MidiQuarterFrame(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.QUARTER_FRAME
        self.type = 0
        self.values = 0
        self.message_length = 2

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.QUARTER_FRAME.value)
        packet.append((self.values & 0x0F) & ((self.type << 4) & 0x70))
        return packet

    def deserialize(self):
        if len(self.rx_packet) == self.message_length:
            self.type = (self.rx_packet[1] >> 4) & 0x07
            self.values = self.rx_packet[1] & 0x0F
            return True
        return False

    def to_string(self):
        return "Quarter Frame: type " + str(self.type) + ", values " + str(self.values)


class MidiSongPosition(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.SONG_POSITION
        self.position = 0
        self.message_length = 3

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.SONG_POSITION.value)
        packet.append(self.position & 0x7F)
        packet.append((self.position >> 7) & 0x7F)
        return packet

    def deserialize(self):
        if len(self.rx_packet) == self.message_length:
            self.position = (self.rx_packet[1] & 0x7F) + ((self.rx_packet[2] & 0x7F) << 7)
            return True
        return False

    def to_string(self):
        return "Song Position: position " + str(self.position)


class MidiSongSelect(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.SONG_SELECT
        self.song = 0
        self.message_length = 2

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.SONG_SELECT.value)
        packet.append(self.song & 0x7F)
        return packet

    def deserialize(self):
        if len(self.rx_packet) == self.message_length:
            self.song = self.rx_packet[1] & 0x7F
            return True
        return False

    def to_string(self):
        return "Song Select: song " + str(self.song)


class MidiTuneRequest(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.TUNE_REQUEST
        self.message_length = 1

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.TUNE_REQUEST.value)
        return packet

    def to_string(self):
        return "Tune Request"


class MidiClock(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.CLOCK
        self.message_length = 1

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.CLOCK.value)
        return packet

    def to_string(self):
        return "Clock"


class MidiStart(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.START
        self.message_length = 1

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.START.value)
        return packet

    def to_string(self):
        return "Start"


class MidiContinue(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.CONTINUE
        self.message_length = 1

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.CONTINUE.value)
        return packet

    def to_string(self):
        return "Continue"


class MidiStop(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.STOP
        self.message_length = 1

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.STOP.value)
        return packet

    def to_string(self):
        return "Stop"


class MidiSense(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.SENSE
        self.message_length = 1

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.SENSE.value)
        return packet

    def to_string(self):
        return "Sense"


class MidiReset(MidiMessage):

    def __init__(self):
        MidiMessage.__init__(self)
        self.midi_message_type = MidiMessageType.RESET
        self.message_length = 1

    def serialize(self):
        packet = bytearray()
        packet.append(MidiMessageType.RESET.value)
        return packet

    def to_string(self):
        return "Reset"


