import serial

class Adapter:
    def __init__(self, port: str, baud: int, end_flag='$') -> None:
        self.port = port
        self.baud = baud
        self.end_flag = end_flag
        self.com = None
    
    def open(self):
        try:
            self.com = serial.Serial(port=self.port, baudrate=self.baud, timeout=10)
        except Exception as e:
            print(e)
    
    def close(self):
        if self.com is not None and self.com.is_open:
            self.com.close()
            
    def transmit(self, data: str) -> int:
        if self.com is None:
            self.open()
        success_bytes = self.com.write(data.encode('ascii'))
        return success_bytes
    
    def read(self) -> bytes:
        if self.com is None:
            self.open()
        data = self.com.readline()
        return data
