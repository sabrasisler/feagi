#!/usr/bin/env python3

import sys
import time
from datetime import datetime

import RPi.GPIO as GPIO

from configuration import *
from Led import *
from PCA9685 import PCA9685
from router import *
# from src.inf import runtime_data
# from src.ipu.processor.proximity import map_value

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


address = 'tcp://' + router_settings['feagi_ip'] + ':' + router_settings['feagi_port']
feagi_state = find_feagi(address=address)

print("** **", feagi_state)
sockets = feagi_state['sockets']
router_settings['feagi_burst_speed'] = float(feagi_state['burst_frequency'])

print("--->> >> >> ", sockets)

# todo: to obtain this info directly from FEAGI as part of registration
ipu_channel_address = 'tcp://0.0.0.0:' + router_settings['ipu_port']
print("IPU_channel_address=", ipu_channel_address)
opu_channel_address = 'tcp://' + router_settings['feagi_ip'] + ':' + sockets['opu_port']

feagi_ipu_channel = Pub(address=ipu_channel_address)
feagi_opu_channel = Sub(address=opu_channel_address, flags=zmq.NOBLOCK)


def send_to_feagi(message):
    print("Sending message to FEAGI...")
    print("Original message:", message)

    # pause before sending to FEAGI IPU SUB (avoid losing connection)
    time.sleep(router_settings['feagi_burst_speed'])
    message['timestamp'] = datetime.now()
    feagi_ipu_channel.send(message)


def map_value(val, min1, max1, min2, max2):
    if val < min1:
        return min2
    if val > max1:
        return max2

    mapped_value = (val - min1) * ((max2 - min2) / (max1 - min1)) + min2

    if max2 >= mapped_value >= min2:
        return mapped_value


class LED:
    def __init__(self):
        self.led = Led()

    def LED_on(self, led_ID, Red_Intensity, Blue_Intensity, Green_intensity):
        """
        Parameters
        ----------
        led_ID: This is the ID of leds. It can be from 1 to 8
        Red_Intensity: 1 to 255, from dimmest to brightest
        Blue_Intensity: 1 to 255, from dimmest to brightest
        Green_intensity: 1 to 255, from dimmest to brightest
        -------
        """
        try:
            self.led.ledIndex(led_ID, Red_Intensity, Blue_Intensity, Green_intensity)
        except KeyboardInterrupt:
            self.led.colorWipe(led.strip, Color(0, 0, 0))  ##This is to turn all leds off/

    def test_Led(self):
        """
        This is to test all leds and do several different leds.
        """
        try:
            self.led.ledIndex(0x01, 255, 0, 0)  # Red
            self.led.ledIndex(0x02, 255, 125, 0)  # orange
            self.led.ledIndex(0x04, 255, 255, 0)  # yellow
            self.led.ledIndex(0x08, 0, 255, 0)  # green
            self.led.ledIndex(0x10, 0, 255, 255)  # cyan-blue
            self.led.ledIndex(0x20, 0, 0, 255)  # blue
            self.led.ledIndex(0x40, 128, 0, 128)  # purple
            self.led.ledIndex(0x80, 255, 255, 255)  # white'''
            print("The LED has been lit, the color is red orange yellow green cyan-blue blue white")
            time.sleep(3)  # wait 3s
            self.led.colorWipe("", Color(0, 0, 0))  # turn off the light
            print("\nEnd of program")
        except KeyboardInterrupt:
            self.led.colorWipe("", Color(0, 0, 0))  # turn off the light
            print("\nEnd of program")

    def leds_off(self):
        self.led.colorWipe("", Color(0, 0, 0))  ##This is to turn all leds off/


class Motor:
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=True)
        self.pwm.setPWMFreq(50)
        self.motor_channels = [[0, 1], [3, 2], [4, 5], [6, 7]]

    @staticmethod
    def duty_range(duty1, duty2, duty3, duty4):
        if duty1 > 4095:
            duty1 = 4095
        elif duty1 < -4095:
            duty1 = -4095

        if duty2 > 4095:
            duty2 = 4095
        elif duty2 < -4095:
            duty2 = -4095

        if duty3 > 4095:
            duty3 = 4095
        elif duty3 < -4095:
            duty3 = -4095

        if duty4 > 4095:
            duty4 = 4095
        elif duty4 < -4095:
            duty4 = -4095
        return duty1, duty2, duty3, duty4

    def left_Upper_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(0, 0)
            self.pwm.setMotorPwm(1, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(1, 0)
            self.pwm.setMotorPwm(0, abs(duty))
        else:
            self.pwm.setMotorPwm(0, 4095)
            self.pwm.setMotorPwm(1, 4095)

    def left_Lower_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(3, 0)
            self.pwm.setMotorPwm(2, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(2, 0)
            self.pwm.setMotorPwm(3, abs(duty))
        else:
            self.pwm.setMotorPwm(2, 4095)
            self.pwm.setMotorPwm(3, 4095)

    def right_Upper_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(6, 0)
            self.pwm.setMotorPwm(7, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(7, 0)
            self.pwm.setMotorPwm(6, abs(duty))
        else:
            self.pwm.setMotorPwm(6, 4095)
            self.pwm.setMotorPwm(7, 4095)

    def right_Lower_Wheel(self, duty):
        if duty > 0:
            self.pwm.setMotorPwm(4, 0)
            self.pwm.setMotorPwm(5, duty)
        elif duty < 0:
            self.pwm.setMotorPwm(5, 0)
            self.pwm.setMotorPwm(4, abs(duty))
        else:
            self.pwm.setMotorPwm(4, 4095)
            self.pwm.setMotorPwm(5, 4095)

    def move(self, motor_index, speed):
        if speed > 0:
            self.pwm.setMotorPwm(self.motor_channels[motor_index][0], 0)
            self.pwm.setMotorPwm(self.motor_channels[motor_index][1], speed)
        elif speed < 0:
            self.pwm.setMotorPwm(self.motor_channels[motor_index][1], 0)
            self.pwm.setMotorPwm(self.motor_channels[motor_index][0], abs(speed))
        else:
            self.pwm.setMotorPwm(self.motor_channels[motor_index][0], 4095)
            self.pwm.setMotorPwm(self.motor_channels[motor_index][1], 4095)

    def setMotorModel(self, duty1, duty2, duty3, duty4):
        duty1, duty2, duty3, duty4 = self.duty_range(duty1, duty2, duty3, duty4)
        self.left_Upper_Wheel(duty1)
        self.left_Lower_Wheel(duty2)
        self.right_Upper_Wheel(duty3)
        self.right_Lower_Wheel(duty4)

    def stop(self):
        self.setMotorModel(0, 0, 0, 0)


class IR:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IR01, GPIO.IN)
        GPIO.setup(self.IR02, GPIO.IN)
        GPIO.setup(self.IR03, GPIO.IN)

    def read(self):
        gpio_state = []
        ir_sensors = [self.IR01, self.IR02, self.IR03]
        for idx, sensor in enumerate(ir_sensors):
            if GPIO.input(sensor):
                gpio_state.append(idx)
        return gpio_state


class Ultrasonic:
    def __init__(self):
        GPIO.setwarnings(False)
        self.trigger_pin = 27
        self.echo_pin = 22
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin,GPIO.OUT)
        GPIO.setup(self.echo_pin,GPIO.IN)

    def send_trigger_pulse(self):
        GPIO.output(self.trigger_pin,True)
        time.sleep(0.00015)
        GPIO.output(self.trigger_pin,False)

    def wait_for_echo(self,value,timeout):
        count = timeout
        while GPIO.input(self.echo_pin) != value and count>0:
            count = count-1

    def get_distance(self):
        distance_cm=[0,0,0]
        for i in range(3):
            self.send_trigger_pulse()
            self.wait_for_echo(True,10000)
            start = time.time()
            self.wait_for_echo(False,10000)
            finish = time.time()
            pulse_len = finish-start
            distance_cm[i] = pulse_len/0.000058
        distance_cm=sorted(distance_cm)
        return int(distance_cm[1])


def main(args=None):
    print("Connecting to FEAGI resources...")

    motor = Motor()
    ir = IR()
    ultrasonic = Ultrasonic()

    try:
        while True:
            # transmit data to FEAGI IPU
            ir_data = ir.read()
            if ir_data:
                formatted_ir_data = {'ir': {sensor: True for sensor in ir_data}}
            else:
                formatted_ir_data = {}

            ultrasonic_data = ultrasonic.get_distance()
            if ultrasonic_data:
                formatted_ultrasonic_data = {
                    'ultrasonic': {
                        sensor: data for sensor, data in enumerate([ultrasonic_data])
                    }
                }
            else:
                formatted_ultrasonic_data = {}

            send_to_feagi({**formatted_ir_data, **formatted_ultrasonic_data})

            # Process OPU data received from FEAGI and pass it along
            opu_data = feagi_opu_channel.receive()
            print("Received:", opu_data)
            if opu_data is not None:
                if 'motor' in opu_data:
                    for motor_id in opu_data['motor']:
                        motor_speed = opu_data['motor'][motor_id]
                        mapped_speed = round(map_value(motor_speed, 0, 20, 0, 4095))
                        print(">>>>>>>>> >>>>>>>>>>>> MAPPED SPEED: ", mapped_speed)
                        motor.move(motor_id, -mapped_speed)
            else:
                motor.stop()
            time.sleep(router_settings['feagi_burst_speed'])
    except KeyboardInterrupt:
        motor.stop()
        pass


if __name__ == '__main__':
    main()
