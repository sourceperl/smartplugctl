# pySmartPlugSmpB16

Python module for control Awox BLE smartPlug.

## Usage example

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

### Require

Python module bluepy (https://github.com/IanHarvey/bluepy) is require. You can install it with :

    sudo apt-get install python-pip libglib2.0-dev
    sudo pip install bluepy

### Setup

    sudo python setup.py install


