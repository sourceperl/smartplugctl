import binascii
import datetime
import struct
import sys
import array
from bluepy import btle

START_OF_MESSAGE = b'\x0f'
END_OF_MESSAGE = b'\xff\xff'


class SmartPlug(btle.Peripheral):
    def __init__(self, addr):
        btle.Peripheral.__init__(self, addr)
        self.delegate = NotificationDelegate()
        self.setDelegate(self.delegate)
        self.plug_svc = self.getServiceByUUID('0000fff0-0000-1000-8000-00805f9b34fb')
        self.plug_cmd_ch = self.plug_svc.getCharacteristics('0000fff3-0000-1000-8000-00805f9b34fb')[0]
        self.plug_name_ch = self.plug_svc.getCharacteristics('0000fff6-0000-1000-8000-00805f9b34fb')[0]

    def get_name(self):
        name = self.plug_name_ch.read()
        return name.decode('iso-8859-1')

    def set_time(self):
        self.delegate.chg_is_ok = False
        buffer = b'\x01\x00'
        now = datetime.datetime.now()
        buffer += struct.pack(">BBBBBH", now.second, now.minute, now.hour, now.day, now.month, now.year)
        buffer += b'\x00\x00\x00\x00'
        self.write_data(self.get_buffer(buffer))
        self.wait_data(0.5)
        return self.delegate.chg_is_ok

    def set_name(self, name):
        buffer = b'\x02\x00'
        buffer += struct.pack(">20s", name.encode('iso-8859-1'))
        self.write_data(self.get_buffer(buffer))
        self.wait_data(0.5)
        return self.delegate.chg_is_ok

    def on(self):
        self.delegate.chg_is_ok = False
        self.write_data(self.get_buffer(binascii.unhexlify('0300010000')))
        self.wait_data(0.5)
        return self.delegate.chg_is_ok

    def off(self):
        self.delegate.chg_is_ok = False
        self.write_data(self.get_buffer(binascii.unhexlify('0300000000')))
        self.wait_data(0.5)
        return self.delegate.chg_is_ok

    def status_request(self):
        self.write_data(self.get_buffer(binascii.unhexlify('04000000')))
        self.wait_data(2.0)
        return self.delegate.state, self.delegate.power, self.delegate.voltage

    def power_history_hour_request(self):
        self.write_data(self.get_buffer(binascii.unhexlify('0a000000')))
        self.wait_data(2.0)
        return self.delegate.history

    def power_history_day_request(self):
        self.write_data(self.get_buffer(binascii.unhexlify('0b000000')))
        self.wait_data(2.0)
        return self.delegate.history

    def program_write(self, program_list):
        buffer = b'\x06\x00'
        for program in program_list:
            start_hour = -1
            start_minute = -1
            if program["start"]:
                start_hour, start_minute = map(int, program["start"].split(':'))
            end_hour = -1
            end_minute = -1
            if program["end"]:
                end_hour, end_minute = map(int, program["end"].split(':'))

            buffer += struct.pack(">?16sBbbbb", True, program["name"].encode('iso-8859-1'), program["flags"], start_hour, start_minute, end_hour, end_minute)

        buffer = buffer.ljust(2 + 5*22, '\0')
        self.write_data(self.get_buffer(buffer))
        self.wait_data(0.5)
        return self.delegate.history

    def reset(self):
        self.delegate.chg_is_ok = False
        self.write_data(self.get_buffer(binascii.unhexlify('0F00000000')))
        self.wait_data(0.5)
        return self.delegate.chg_is_ok

    def light_enable(self, enable):
        self.delegate.chg_is_ok = False
        buffer = b'\x0F\x00\x01'
        buffer += struct.pack(">?x",enable)
        self.write_data(self.get_buffer(buffer))
        self.wait_data(0.5)
        return self.delegate.chg_is_ok

    def program_request(self):
        self.write_data(self.get_buffer(binascii.unhexlify('07000000')))
        self.wait_data(2.0)
        return self.delegate.programs

    def calculate_checksum(self, message):
        return (sum(bytearray(message)) + 1) & 0xff

    def get_buffer(self, message):
        return START_OF_MESSAGE + struct.pack("B",len(message) + 1) + message + struct.pack("B",self.calculate_checksum(message)) + END_OF_MESSAGE

    def write_data(self, data):
        remaining_data = data
        while len(remaining_data) > 0:
            self.plug_cmd_ch.write(remaining_data[:20])
            remaining_data = remaining_data[20:]

    def wait_data(self, timeout):
        self.delegate.need_data = True
        while self.delegate.need_data and self.waitForNotifications(timeout):
            pass


class NotificationDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        self.state = False
        self.power = 0
        self.voltage = 0
        self.chg_is_ok = False
        self.history = []
        self.programs = []
        self._buffer = b''
        self.need_data = True

    def handleNotification(self, cHandle, data):
        # not sure 0x0f indicate begin of buffer but
        if data[:1] == START_OF_MESSAGE:
            self._buffer = data
        else:
            self._buffer = self._buffer + data
        if self._buffer[-2:] == END_OF_MESSAGE:
            self.handle_data(self._buffer)
            self._buffer = b''
            self.need_data = False 

    def handle_data(self, bytes_data):
        # it's a set time confirm notification ?
        if bytes_data[0:5] == b'\x0f\x04\x01\x00\x00':
            self.chg_is_ok = True
        # it's a set name confirm notification ?
        if bytes_data[0:5] == b'\x0f\x04\x02\x00\x00':
            self.chg_is_ok = True
        # it's a state change confirm notification ?
        if bytes_data[0:3] == b'\x0f\x04\x03':
            self.chg_is_ok = True
        # it's a state/power notification ?
        if bytes_data[0:3] == b'\x0f\x0f\x04':
            (state, dummy, power, voltage) = struct.unpack_from(">?BIB", bytes_data, offset=4)
            self.state = state
            self.power = power / 1000
            self.voltage = voltage
        # it's a power history for last 24h notif ?
        if bytes_data[0:3] == b'\x0f\x33\x0a':
            history_array = array.array('H', bytes_data[4:52])
            # get the right byte order
            if sys.byteorder == 'little':
                history_array.byteswap()
            self.history = reversed(history_array.tolist())
        # it's a power history kWh/day notif ?
        if bytes_data[0:3] == b'\x0f\x7b\x0b':
            history_array = array.array('I', bytes_data[4:124])
            # get the right byte order
            if sys.byteorder == 'little':
                history_array.byteswap()
            self.history = reversed(history_array.tolist())
         # it's a programs notif ?
        if bytes_data[0:3] == b'\x0f\x71\x07':
            program_offset = 4
            self.programs = []
            while program_offset + 21 < len(bytes_data):
                (present, name, flags, start_hour, start_minute, end_hour, end_minute) = struct.unpack_from(">?16sBbbbb", bytes_data, program_offset)
                #TODO interpret flags (day of program ?)
                if present:
                    start_time = None
                    end_time = None
                    if start_hour >= 0 and start_minute >= 0:
                        start_time = "{0:02d}:{1:02d}".format(start_hour, start_minute)
                    if end_hour >= 0 and end_minute >= 0:
                        end_time = "{0:02d}:{1:02d}".format(end_hour, end_minute)
                    self.programs.append({"name" : name.decode('iso-8859-1').strip('\0'), "flags":flags, "start":start_time, "end":end_time})
                program_offset += 22
        if bytes_data[0:4] == b'\x0f\x05\x0f\x00':
            self.chg_is_ok = True
# SmartPlugSmpB16 usage sample: cycle power then log plug state and power level to terminal
if __name__ == '__main__':
    import time

    # connect to the plug with bluetooth address
    plug = SmartPlug('98:7B:F3:34:78:52')

    # cycle power
    plug.off()
    time.sleep(2.0)
    plug.on()

    # display state and power level
    while True:
        (state, power, voltage) = plug.status_request()
        print('plug state = %s' % ('on' if state else 'off'))
        print('plug power = %d W' % power)
        time.sleep(2.0)
