#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 19:23:57 2020

@author: taylor
"""
from logging import getLogger
from diph.config import DiPHConfig


class Wizard(DiPHConfig):
    def __init__(self):
        self.log_name = 'DiPHConfig.Wizard'
        super().__init__()
        print(dir(self))
        print(self.conf_parser)
        print(self.args)
        w_log = getLogger(self.log_name)

        if not self.args.log_level == 'info':
            self.log_device.adjust_level(self.args.log_level)
            w_log.debug('Logger level adjusted to user parameters.')

        print(self.runtime)


run = Wizard()
