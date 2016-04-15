#!/usr/bin/env python

# smartPlug AWOX control with Bluez
#
# Control an AWOX smartPlug (BLE electrical plug with relay) from command line
# sample: './smart_plug_ctl.py 98:7B:F3:34:78:52 on' to turn on the plug
#
# needs: bluez installed with gatttool utility
#
# license: MIT

import sys
import subprocess
import argparse

# parse args
parser = argparse.ArgumentParser()
parser.add_argument('ble_addr', type=str, 
                    help='plug bluetooth LE address (like 98:7b:f3:34:78:52)')
parser.add_argument('state', type=str, choices=['on', 'off'],
                    help='plug state to set')
args = parser.parse_args()

# format gatttool command
cmd = 'gatttool -b {0}'.format(args.ble_addr)
plug_on_opt = ' --char-write -a 0x2b -n 0f06030001000005ffff'
plug_off_opt = ' --char-write -a 0x2b -n 0f06030000000004ffff'
cmd += plug_on_opt if args.state == 'on' else plug_off_opt
cmd += ' 2>/dev/null'

# do it
return_code = subprocess.call(cmd, shell=True)

# return gatttool error code
sys.exit(return_code)
