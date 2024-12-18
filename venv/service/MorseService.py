import asyncio
import logging
from config.LoggerConfig import logger

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 
    'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
    '9': '----.', '0': '-----', ' ': '/'
}

class MorseService:

    def __init__(self):
        from service.BulbService import BulbService
        self.bulbService = BulbService()

    async def morseCode(self, message: str):
        try:
            logger.info(f"Flashing morse code for string: {message}.")
            message = message.upper()
            bulbState = self.bulbService.getBulbState()
            for char in message:
                if char in MORSE_CODE_DICT:
                    code = MORSE_CODE_DICT[char]
                    for symbol in code:
                        if symbol == '.':
                            await self.bulbService.flashLight(0.5) 
                        elif symbol == '-':
                            await self.bulbService.flashLight(1.5)
                        await asyncio.sleep(0.5)
                    await asyncio.sleep(1.5)
                elif char == '/':
                    await asyncio.sleep(3.5)
            logger.info(f"Done flashing morse code for string: {message}.")
            self.bulbService.setBulbState(bulbState)
        except Exception as e:
            logger.info(f"Error flash morse code for string: {message}: {str(e)}")