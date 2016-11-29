#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 10:41:30 2016

@author: iiivanitskiy
"""

import time

def check_time(update):
    unix_now_time = int(time.time())
    unix_message_time = update.message['date']
    return (unix_now_time <= unix_message_time + 120)