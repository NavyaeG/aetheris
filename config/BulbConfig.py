import os

class BulbConfig:
    
    def __init__(self):
        self.DEVICE_IP = os.getenv("DEVICE_IP")
        self.DEVICE_ID = os.getenv("DEVICE_ID")
        self.LOCAL_KEY = os.getenv("LOCAL_KEY")

    def setDeviceIp(self, device_ip: str):
        self.DEVICE_IP=device_ip

    def getDeviceIp(self):
        return self.DEVICE_IP
    
    def getDeviceId(self):
        return self.DEVICE_ID
    
    def getLocalKey(self):
        return self.LOCAL_KEY