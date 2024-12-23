from pydantic import BaseModel

class Morse(BaseModel):
    
    text: str