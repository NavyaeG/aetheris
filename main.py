from fastapi import FastAPI, HTTPException
from service.BulbService import BulbService
from service.AlarmService import AlarmService
from model.Alarm import Alarm
from model.Morse import Morse
from model.ColorGradientAnimation import ColorGradientAnimation
from config.LoggerConfig import LoggerConfig
from service.MorseService import MorseService
from service.TaskManagerService import taskManagerService
from service.ColorService import ColorService

logger = LoggerConfig.configure_logger()

app = FastAPI()

colorService = ColorService()
bulbService = BulbService()
alarmService = AlarmService()
morseService = MorseService()

@app.post("/turn-off")
async def turnOffLight():
    try:
        await taskManagerService.addTask("bulbOff", bulbService.turnOff)
        return {"status": "success", "message": "Light turned off successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error turning off light: {str(e)}")

@app.post("/turn-on")
def turnOffLight():
    try:
        bulbService.turnOn()
        return {"status": "success", "message": "Light turned off successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error turning off light: {str(e)}")
    
@app.post("/alarm/create")
def createAlarm(alarm : Alarm):
    result = alarmService.scheduleAlarm(alarm) 
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

@app.delete("/alarm/cancel/{alarmId}")
def cancelAlarm(alarmId: str):
    result = alarmService.cancelAlarm(alarmId)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    elif result["status"] == "not found":
        raise HTTPException(status_code=404, detail=result["message"])
    return result

@app.get("/alarm/list")
def getAlarms():
    return alarmService.getAllAlarms()

@app.post("/morse-code")
async def morseCode(morse: Morse):
    try:
        await taskManagerService.addTask("morse", morseService.morseCode, morse.text)
        return {"status": "success", "message": f"Flashing morse code for string: {morse.text}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing morse code: {str(e)}")

@app.get("/status")
def getBulbStatus():
    try:
        bulbState = bulbService.getBulbState()
        return {"status": "success", "bulb": bulbState}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status of bulb: {str(e)}")
    
@app.post("/cga")
async def startFlowyColor(cga: ColorGradientAnimation):
    try:
        if(cga.state):
            await taskManagerService.addTask("colorGradientAnimationOn", colorService.colorGradientAnimationOn)
            return {"status": "success", "message": f"Color gradient animation on"}
        elif(not cga.state):
            await taskManagerService.addTask("colorGradientAnimationOff", colorService.colorGradientAnimationOff)
            return {"status": "success", "message": f"Color gradient animation turned off"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing color gradient request: {str(e)}")