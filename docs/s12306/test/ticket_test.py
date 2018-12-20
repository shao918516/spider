#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Terry'

#  '10'   or   '0, 10'  or  '119, 0'  or  '1, 125'
ticket = '10'

def validate_ticket(ticket):
    if int(ticket.split(',')[0]) > 0:
        return True


print(validate_ticket())


