import serial, time
arduino = serial.Serial('COM3', 9600)

try:
    while True:
        # Envía el carácter '1' a Arduino para encender el LED
        arduino.write(b'1')
        print('LED encendido')
        time.sleep(1)

except KeyboardInterrupt:
    arduino.close()
    