#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pykrotik import MikrotikApi

# Make sure to enable API at the device:
# /ip service enable api 

mtk = MikrotikApi('192.168.88.1', 'admin', '')
print mtk.exec_command('/ip/address/print')
