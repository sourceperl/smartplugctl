# smartplugctl

Little utility for control Awox BLE smartPlug (test with Bluez 5 and Raspberry
Pi)

![](img/rpi_smartplug.jpg)

## Usage example

On Raspbian the script don't require sudo right for pi user but it's necessary
on some host.

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
