# smartplugctl

Little utility for control Awox BLE smartPlug (test with Bluez 5 and Raspberry
Pi)

![](img/rpi_smartplug.jpg)

## Read first

On Raspbian the script don't require sudo right for pi user but it's necessary
on some host. It use bluez gatttool commmand line utility to do the stuff. A
full python module is also available with no gatttool dependency see below.

### Require

Python module pexpect is require. You can install it with :

    sudo pip install pexpect

or on debian based system :

    sudo apt-get install python-pexpect

### Setup

    sudo python setup.py install

### Turn plug on

    smartplugctl 98:7B:F3:34:78:52 on

### Turn plug off

    smartplugctl 98:7B:F3:34:78:52 off

### Read plug status (on/off and power level)

    smartplugctl 98:7B:F3:34:78:52 status

### Help

    smartplugctl -h

### Python module

Advanced users can look at python_module/ for pySmartPlugSmpB16 module.
The bluepy package is needed for use this, see https://github.com/IanHarvey/bluepy
for installation purpose.


