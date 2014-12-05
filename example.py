#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mikrotik.mikrotikapi import MikrotikApi

mtk = MikrotikApi('10.30.0.25', 'admin', '')
print mtk.exec_command('/interface/wireless/registration-table/print')
