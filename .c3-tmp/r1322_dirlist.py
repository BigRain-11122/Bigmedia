# -*- coding: utf-8 -*-
import os
BASE = r'data\storylines\cards'
for d in ('MC-20261005-DAILY-v66', 'MC-20261005-DAILY-v66-tmp', 'MC-20261005-DAILY-v65'):
    p = os.path.join(BASE, d)
    if os.path.isdir(p):
        print(d, '->', sorted(os.listdir(p)))
