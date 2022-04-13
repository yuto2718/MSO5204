import sys
try:
    import pyvisa
except:
    print("pyvisa is not available")
    sys.exit()

from PIL import Image
import io
import re

class MSO5204:
    def __init__(self, visaResourceManager:pyvisa.ResourceManager):
        self.__devname  = ""
        self.rm = visaResourceManager
        self.serchDevice()
        self.inst = self.rm.open_resource(self.__devname )
        print(self.__devname+"connected.")
        
    def __del__(self):
        self.inst.close()
        del self.inst
        
    def serchDevice(self):
        for name in self.rm.list_resources():
            inst = self.rm.open_resource(name)
            inst.write('*IDN?')
            ID = inst.read()
            
            if re.search("RIGOL", ID):
                inst.close()
                self.__devname = name
                return name
            else:
                inst.close()
            
        return "NO DEVICE"
    
    def captureDisplay(self, savename):
        bmp_bin = self.inst.query_binary_values(':DISP:DATA?', datatype='B', container=bytes)
        img = Image.open(io.BytesIO(bmp_bin))
        img.save(savename)
    
    def getWave(self):
        pass
    
    def saveWave(self):
        pass
    
    def getConfiguration(self):
        pass
    
    def saveConguration(self):
        pass
    
    def autoScale(self):
        self.inst.write(':AUToscale')
        
    def run(self):
        self.inst.write(':RUN')
        
    def stop(self):
        self.inst.write(':STOP')
    
    def single(self):
        self.inst.write(':SINGle')
        
rm = pyvisa.ResourceManager()
osi = MSO5204(rm)