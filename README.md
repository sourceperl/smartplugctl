# smartplugctl

Little utility for control Awox BLE smartPlug (test with Bluez 5 and Raspberry
Pi)

![](img/rpi_smartplug.jpg)

## Usage example

On Raspbian the script don't require sudo right for pi user but it's necessary
on some host.

### Setup

    sudo python setup.py install

### Turn plug on

    smartplugctl 98:7B:F3:34:78:52 on

### Turn plug off

    smartplugctl 98:7B:F3:34:78:52 off

### Help

    smartplugctl -h
