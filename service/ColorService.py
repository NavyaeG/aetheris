from service.BulbService import BulbService
import asyncio
from PIL import ImageGrab
import colorsys
from colorthief import ColorThief
import io

class ColorService:

    def __init__(self):
        self.bulbService = BulbService()

    def getDominantColor(self):
        img = ImageGrab.grab()

        with io.BytesIO() as byte_io:
            img.save(byte_io, format='PNG')
            byte_io.seek(0)
            color_thief = ColorThief(byte_io)
            dominant_color = color_thief.get_color(quality=10)  

        r, g, b = dominant_color
        r /= 255.0
        g /= 255.0
        b /= 255.0

        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (h, s, 0.8)

    def setBulbColor(self, hsvColor, device):
        device.set_hsv(hsvColor[0], hsvColor[1], hsvColor[2])

    async def smoothTransition(self, device, startHsv, endHsv, steps=3, delay=0.2):
        for step in range(steps):
            intermediate_hsv = tuple(startHsv[i] + (endHsv[i] - startHsv[i]) * step / steps for i in range(3))
            self.setBulbColor(intermediate_hsv, device)
            await asyncio.sleep(delay)

    async def colorGradientAnimationOn(self):
        device = self.bulbService.createDevice()
        device.turn_on()
        while True:
            dominantColorHsv = self.getDominantColor()
            self.setBulbColor(dominantColorHsv, device)
            await asyncio.sleep(0.2)
        
    async def colorGradientAnimationOff(self):
        bulbState = self.bulbService.getBulbState()
        self.bulbService.setBulbState(bulbState)