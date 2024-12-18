from model.Alarm import Alarm
from typing import Dict

class AlarmList:
    
    def __init__(self):
        self.alarmList: Dict[str, Alarm] = {}

    def getAlarmList(self):
        return self.alarmList

alarmList = AlarmList()