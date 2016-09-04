# smartplugctl

Little utility for control Awox BLE smartPlug. Test with Bluez 5 and Raspberry
Pi. Also test on amd64 debian jessie.

![](img/rpi_smartplug.jpg)

## Read first

Two scripts is provide here to deal with the plug(s): smartplugscan for find 
the plug address and smartplugctl to send command to it (on/off/read status). 
This 2 scripts use SmartPlugSmpB16 python module for manage Bluetooth Low 
Energy exchanges.

An older release of smartplugctl use bluez gatttool commmand line utility to do 
the stuff. In this script bluepy module is not require, it is available under 
old_scripts/.

### Require

Python module bluepy (https://github.com/IanHarvey/bluepy) is require. You can 
install it with :

    sudo apt-get install -y python-pip libglib2.0-dev
    sudo pip install bluepy

### Setup

    sudo apt-get install -y python-setuptools
    sudo python setup.py install

### Find a plug

    sudo smartplugscan

### Turn plug on

    smartplugctl 98:7B:F3:34:78:52 on

### Turn plug off

    smartplugctl 98:7B:F3:34:78:52 off

### Read plug status (on/off and power level)

    smartplugctl 98:7B:F3:34:78:52 status

### Help

    smartplugctl -h

## Python module

Alternatively to smartplug scripts you can directly use module from python code.

### Usage example

    # cycle power then log plug state and power level to terminal
    import pySmartPlugSmpB16
    import time

    # connect to the plug with bluetooth address
    plug = pySmartPlugSmpB16.SmartPlug('98:7B:F3:34:78:52')

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
