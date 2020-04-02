#!/usr/bin/python3
"""
Module Name: time.py
Purpose: Time module

Description:
    This module is used to process all time data such as time zone setting or get current time.
History:
    Anber Huang 06/30/2019,created.

Copyright(c) Accton Technology Corporation, 2019.
"""
from datetime import datetime,timezone,timedelta

class Time():
    def __init__(self):
        pass
    
    def get_time_now(self):
        dt = datetime.utcnow()
        dt = dt.replace(tzinfo=timezone.utc)
        tzutc_8 = timezone(timedelta(hours=8))
        local_dt = dt.astimezone(tzutc_8)
        return str(local_dt).split('.')[0]

    def get_time_for_calculate(self):
        return datetime.now()

    def cal_target_time_from_now(self, hours):
        now_time = self.get_time_for_calculate()
        target = now_time + timedelta(hours=float(hours))
        return target