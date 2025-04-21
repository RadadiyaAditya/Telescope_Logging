import serial
import json
import os
from dotenv import load_dotenv

load_dotenv()

def listen_to_serial(port=os.getenv('SERIAL_PORT'), baudrate=os.getenv('SERIAL_BAUDRATE')):
    ser = serial.Serial(port, baudrate, timeout=1)

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print("Received:", line)
                data = json.loads(line)
                with open("latest_serial_data.json", "w") as f:
                    json.dump(data, f)
        except Exception as e:
            print("Error:", e)