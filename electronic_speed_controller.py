import os
import time
import pigpio
os.system("sudo pigpiod")
time.sleep(1)

#Connect the ESC in this GPIO pin
ESCOne = 4
ESCTwo = 17
ESCThree = 27
ESCFour = 22

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESCOne, 0)
pi.set_servo_pulsewidth(ESCTwo, 0)
pi.set_servo_pulsewidth(ESCThree, 0)
pi.set_servo_pulsewidth(ESCFour, 0)

max_value = 2000 #ESC's max value
min_value = 700  #ESC's min value

print("Choose one of the options: calibrate - manual - control - arm - stop")


def manual_drive():
    print("You have selected manual option so give a value between 0 and you max value")
    while True:
        inp = input()
        if inp == "stop":
            stop()
            break
        elif inp == "control":
            control()
            break
        elif inp == "arm":
            arm()
            break
        else:
            pi.set_servo_pulsewidth(ESCOne, inp)
            pi.set_servo_pulsewidth(ESCTwo, inp)
            pi.set_servo_pulsewidth(ESCThree, inp)
            pi.set_servo_pulsewidth(ESCFour, inp)


def calibrate():
    pi.set_servo_pulsewidth(ESCOne, 0)
    pi.set_servo_pulsewidth(ESCTwo, 0)
    pi.set_servo_pulsewidth(ESCThree, 0)
    pi.set_servo_pulsewidth(ESCFour, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == '':
        pi.set_servo_pulsewidth(ESCOne, max_value)
        pi.set_servo_pulsewidth(ESCTwo, max_value)
        pi.set_servo_pulsewidth(ESCThree, max_value)
        pi.set_servo_pulsewidth(ESCFour, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == '':
            pi.set_servo_pulsewidth(ESCOne, min_value)
            pi.set_servo_pulsewidth(ESCTwo, min_value)
            pi.set_servo_pulsewidth(ESCThree, min_value)
            pi.set_servo_pulsewidth(ESCFour, min_value)
            print("Special tone")
            time.sleep(7)
            print("Wait...")
            time.sleep (5)
            print("Wait...")
            pi.set_servo_pulsewidth(ESCOne, 0)
            pi.set_servo_pulsewidth(ESCTwo, 0)
            pi.set_servo_pulsewidth(ESCThree, 0)
            pi.set_servo_pulsewidth(ESCFour, 0)
            time.sleep(2)
            print("Arming ESC")
            pi.set_servo_pulsewidth(ESCOne, min_value)
            pi.set_servo_pulsewidth(ESCTwo, min_value)
            pi.set_servo_pulsewidth(ESCThree, min_value)
            pi.set_servo_pulsewidth(ESCFour, min_value)
            time.sleep(1)
            control()


def control(): 
    print("Motors starting")
    time.sleep(1)
    speed = 1000
    print("Controls - a,q to decrease speed & d,e to increase speed")
    while True:
        pi.set_servo_pulsewidth(ESCOne, speed)
        pi.set_servo_pulsewidth(ESCTwo, speed)
        pi.set_servo_pulsewidth(ESCThree, speed)
        pi.set_servo_pulsewidth(ESCFour, speed)
        inp = input()

        if inp == "q":
            speed -= 100
            print("speed = %d" % speed)
        elif inp == "e":    
            speed += 100
            print("speed = %d" % speed)
        elif inp == "d":
            speed += 10
            print("speed = %d" % speed)
        elif inp == "a":
            speed -= 10
            print("speed = %d" % speed)
        elif inp == "stop":
            stop()
            break
        elif inp == "manual":
            manual_drive()
            break
        elif inp == "arm":
            arm()
            break
        else:
            print("Press a,q,d or e to increase or decrease the speed")


def arm():
    print("Connect the battery and press Enter")
    inp = input()    
    if inp == '':
        pi.set_servo_pulsewidth(ESCOne, 0)
        pi.set_servo_pulsewidth(ESCTwo, 0)
        pi.set_servo_pulsewidth(ESCThree, 0)
        pi.set_servo_pulsewidth(ESCFour, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESCOne, max_value)
        pi.set_servo_pulsewidth(ESCTwo, max_value)
        pi.set_servo_pulsewidth(ESCThree, max_value)
        pi.set_servo_pulsewidth(ESCFour, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESCOne, min_value)
        pi.set_servo_pulsewidth(ESCTwo, min_value)
        pi.set_servo_pulsewidth(ESCThree, min_value)
        pi.set_servo_pulsewidth(ESCFour, min_value)
        time.sleep(1)
        control() 


def stop():
    pi.set_servo_pulsewidth(ESCOne, 0)
    pi.set_servo_pulsewidth(ESCTwo, 0)
    pi.set_servo_pulsewidth(ESCThree, 0)
    pi.set_servo_pulsewidth(ESCFour, 0)
    pi.stop()


inp = input()
if inp == "manual":
    manual_drive()
elif inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else:
    print("Restart the program")
