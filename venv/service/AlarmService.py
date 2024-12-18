import asyncio
from datetime import datetime, timedelta
from typing import Optional
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from service.BulbService import BulbService
from model.Alarm import Alarm
from config.LoggerConfig import logger
from service.AlarmListService import AlarmListService
from apscheduler.triggers.cron import CronTrigger

class AlarmService:

    def __init__(self):
        self.backgroundScheduler = AsyncIOScheduler()
        self.bulbService = BulbService()
        self.alarmListService = AlarmListService()
        self.backgroundScheduler.start()

    def getNextTriggerDate(self, triggerDate: datetime, day: str):
        daysUntilRepeat = (self.getDayOfWeek(day) - triggerDate.weekday())%7
        nextTriggerDate = triggerDate + timedelta(days=daysUntilRepeat)
        if(datetime.now() > nextTriggerDate):
            nextTriggerDate = nextTriggerDate + timedelta(days=7)
        return nextTriggerDate

    def getDayOfWeek(self, dayName: str):
        daysOfWeek = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6
        }
    
        return daysOfWeek[dayName.lower()]

    def getTriggerDate(self, alarmTime: str, day: str):
        try:
            timeObj = datetime.strptime(alarmTime, "%H:%M").time()
            today = datetime.now().date() 
            triggerDate = datetime.combine(today, timeObj) 
            if day!=None:
                triggerDate = self.getNextTriggerDate(triggerDate, day)
            elif(triggerDate < datetime.now()):
                triggerDate = triggerDate + timedelta(days=1)

            return triggerDate
        except ValueError as e:
            logger.error(f"Invalid time format. Please provide time in 'HH:MM' format. Error: {e}.")

    def scheduleAlarm(self, alarm: Alarm):
        try:
            triggerDate = self.getTriggerDate(alarm.alarmTime, alarm.day)
            
            if alarm.repeat:
                trigger = CronTrigger(day_of_week=triggerDate.weekday(), hour=triggerDate.hour, minute=triggerDate.minute)
            else:
                trigger = DateTrigger(run_date=triggerDate)

            job = self.backgroundScheduler.add_job(self.bulbService.alarm, trigger, args=[alarm], id=alarm.alarmId)
            self.alarmListService.addAlarm(alarm)
            logger.info(f"Alarm {alarm.alarmId} scheduled at {alarm.alarmTime}.")
            return {"status": "success", "message": f"Alarm scheduled for {triggerDate} with repeat: {alarm.repeat}."}
        except Exception as e:
            logger.error(f"Error scheduling alarm: {str(e)}.")
            return {"status": "error", "message": f"Error scheduling alarm."}

    def cancelAlarm(self, alarmId: str):
        try:
            if alarmId in self.alarmListService.getAlarmList():
                job = self.backgroundScheduler.get_job(alarmId)
                if job:
                    job.remove()
                self.alarmListService.removeAlarm(alarmId)
                logger.info(f"Alarm {alarmId} canceled.")
                return {"status": "success", "message": f"Alarm {alarmId} canceled."}
            else:
                logger.warning(f"Alarm {alarmId} not found.")
                return {"status": "not found", "message": f"Alarm {alarmId} not found."}
        except Exception as e:
            logger.error(f"Error canceling alarm {alarmId}: {str(e)}")
            return {"status": "error", "message": f"Error canceling alarm."}
        
    def getAllAlarms(self):
        return {"alarms": [alarm.__dict__ for alarm in self.alarmListService.getAlarmList().values()]}