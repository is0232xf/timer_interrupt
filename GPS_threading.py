import serial
from micropyGPS import MicropyGPS

gps = MicropyGPS(9, 'dd') # MicroGPSオブジェクトを生成する。

def rungps(): # GPSモジュールを読み、GPSオブジェクトを更新する
    s = serial.Serial('/dev/serial0', 9600, timeout=10)
    s.readline() # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    while True:
        sentence = s.readline().decode('utf-8') # GPSデーターを読み、文字列に変換する
        if sentence[0] != '$': # 先頭が'$'でなければ捨てる
            continue
        for x in sentence: # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
            gps.update(x)

def get_GPS_data():
	latitude = gps.latitude[0]
	longitude = gps.longitude[0]
	return latitude, longitude
 
def get_speed():
    speed = gps.speed
    return speed
