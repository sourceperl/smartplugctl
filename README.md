# smartplugctl

Little utility for control Awox BLE smartPlug (test with Bluez 5 and Raspberry
Pi)

![](img/rpi_smartplug.jpg)

## Usage example

On Raspbian the script don't require sudo right for pi user but it's necessary
on Debian.

### Turn plug on

    sudo ./smart_plug_ctl.py 98:7B:F3:34:78:52 on

### Turn plug off

    sudo ./smart_plug_ctl.py 98:7B:F3:34:78:52 off

### Help

    ./smart_plug_ctl.py -h
