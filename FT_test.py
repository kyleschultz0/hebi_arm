from time import time, sleep
import NetFT

if __name__ == "__main__":

    sensor = NetFT.Sensor("192.168.0.11")

    while True:
       sleep(0.1)
       print(sensor.getForce())
       # print("Force:", f)