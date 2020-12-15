#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
class timer(object):
    # 计时器，用来延时运行
    def __init__(self, maxtime=1):
        self.maxtime = maxtime
    def time_start(self):
        self.begin_time = time.time()
    def is_ready(self):
        end_time = time.time()
        if end_time - self.begin_time > self.maxtime:
            return True
        else:
            return False