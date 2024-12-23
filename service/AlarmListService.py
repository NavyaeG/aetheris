from model.AlarmList import alarmList
from model.Alarm import Alarm

class AlarmListService():

    def __init__(self):
        self.alarmList = alarmList.alarmList

    def addAlarm(self, alarm: Alarm):
        self.alarmList[alarm.alarmId] = alarm

    def removeAlarm(self, alarmId: str):
        if alarmId in self.alarmList:
            del self.alarmList[alarmId]

    def getAlarm(self, alarmId: str):
        return self.alarmList.get(alarmId)
    
    def getAlarmList(self):
        return self.alarmList