import binascii
from bluepy import btle


class SmartPlug(btle.Peripheral):
    def __init__(self, addr):
        btle.Peripheral.__init__(self, addr)
        self.delegate = NotificationDelegate()
        self.setDelegate(self.delegate)
        self.plug_svc = self.getServiceByUUID('0000fff0-0000-1000-8000-00805f9b34fb')
        self.plug_cmd_ch = self.plug_svc.getCharacteristics('0000fff3-0000-1000-8000-00805f9b34fb')[0]

    def on(self):
        self.delegate.chg_is_ok = False
        self.plug_cmd_ch.write(binascii.unhexlify('0f06030001000005ffff'))
        self.waitForNotifications(0.5)
        return self.delegate.chg_is_ok

    def off(self):
        self.delegate.chg_is_ok = False
        self.plug_cmd_ch.write(binascii.unhexlify('0f06030000000004ffff'))
        self.waitForNotifications(0.5)
        return self.delegate.chg_is_ok

    def status_request(self):
        self.plug_cmd_ch.write(binascii.unhexlify('0f050400000005ffff'))
        self.waitForNotifications(2.0)
        return self.delegate.state, self.delegate.power


class NotificationDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        self.state = False
        self.power = 0
        self.chg_is_ok = False

    def handleNotification(self, cHandle, data):
        bytes_data = bytearray(data)
        # it's a state change confirm notification ?
        if bytes_data[0:3] == bytearray([0x0f, 0x04, 0x03]):
            self.chg_is_ok = True
        # it's a state/power notification ?
        if bytes_data[0:3] == bytearray([0x0f, 0x0f, 0x04]):
            self.state = bytes_data[4] == 1
            self.power = int(binascii.hexlify(bytes_data[6:10]), 16) / 1000


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
        (state, power) = plug.status_request()
        print('plug state = %s' % ('on' if state else 'off'))
        print('plug power = %d W' % power)
        time.sleep(2.0)
