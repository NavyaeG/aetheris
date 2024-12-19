from config.BulbConfig import BulbConfig
import tinytuya
import asyncio
from config.LoggerConfig import logger
from service.AlarmListService import AlarmListService
from model.Alarm import Alarm
from model.BulbState import BulbState

VERSION = 3.5

class BulbService:

    def __init__(self):
        self.bulbConfig = BulbConfig()
        self.alarmListService = AlarmListService()

    def createDevice(self):
        configuration = self.bulbConfig
        device = tinytuya.BulbDevice(configuration.getDeviceId(), configuration.getDeviceIp(), configuration.getLocalKey())
        device.set_version(VERSION)
        return device
    
    def turnOn(self):
        device = self.createDevice()
        device.turn_on()
        logger.info("Light turned on")

    def turnOff(self):
        device = self.createDevice()
        device.turn_off()
        logger.info("Light turned off")

    async def alarm(self, alarm: Alarm):
        logger.info("Starting alarm")
        if not alarm.repeat :
            self.alarmListService.removeAlarm(alarm.alarmId)
        device = self.createDevice()
        current_brightness = 0
        device.set_brightness(current_brightness) 
        device.turn_on()
        device.set_colourtemp_percentage(0)
        while current_brightness <= 100:
            current_brightness += 1
            device.set_brightness_percentage(current_brightness)
            await asyncio.sleep(0.5)
        logger.info("Completed alarm")

    async def flashLight(self, duration):
        device = self.createDevice()
        device.set_brightness(100)
        device.turn_on()
        await asyncio.sleep(duration)

        device.turn_off()
        await asyncio.sleep(0.2)
    
    def getBulbState(self):
        device = self.createDevice()
        try:
            brightness = device.brightness()
            temperature = device.colourtemp()
            state = device.state()
            hsv = device.colour_hsv()
            isOn = state["is_on"]
            mode = state["mode"]
            return BulbState(brightness, temperature, isOn, mode, hsv)
        except Exception as e:
            logger.error(f"Error retrieving bulb values: {e}")
            return None
        
    def setBulbState(self, bulbState: BulbState):
        device = self.createDevice()
        try:
            if(bulbState.mode == "colour"):
                device.set_hsv(bulbState.hsv[0], bulbState.hsv[1], bulbState.hsv[2])
            else:
                device.set_mode(bulbState.mode)
                device.set_brightness(bulbState.brightness)
                device.set_colourtemp(bulbState.temperature)
            if(bulbState.isOn):
                device.turn_on()
            logger.info("Set bulb state to previous state")
        except Exception as e:
            logger.error(f"Error setting bulb state to previous state: {e}")
            return None