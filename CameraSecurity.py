import asyncio
import picamera
import RPi.GPIO as GPIO

from datetime import datetime, timedelta


class CameraSecurity:
    """Security system built with a DORHEA Camera Module w/ night-vision compatibility, and an HC-SR501 PIR Sensor module
    for motion detection.

    Notes: Project meant for development with async behavior in Python, and to see if I can get Google API access.
    """

    def __init__(self, motion_sensor_pin_number):
        """Construct object

        Args:
            motion_sensor_pin_number (int): Meant to be the RPi.GPIO.BCM pin number.

        TODO:
        - Set up camera
        - Set up motion sensor to start up and continuously set whether motion has happened
        - Set up camera to record when motion detected and continue recording for 15 seconds
            after the motion has stopped. Read up on what `wait_recording()` can actually do
        - Get shell script to instantiate this object and start up motion sensor to record when
            motion is active
        """
        # Set the mode for GPIO pins
        GPIO.setmode(GPIO.BCM)

        # Camera set-up
        self.camera = picamera.PiCamera()
        self.camera.resolution = "HD"

        self.MOTION = DotDict(
            {
                "COUNT": 0,
                "CURRENT": None,
                "DETECTED": False,
                "SENSOR": motion_sensor_pin_number,
                # datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                "START": None,
            }
        )
        self.MOTION_END_TIME_LAPSE = timedelta(seconds=15)

        # Set up the input connector to check for when the motion sensor is tipped off
        GPIO.setup(self.MOTION.SENSOR, GPIO.IN)

    def _append_motion(self):
        #  Set detected to true
        self.MOTION.DETECTED = True
        # Set the start date of the trip
        self.MOTION.START = datetime.now()
        # Append one to the motion count
        self.MOTION.COUNT += 1

    async def _detect_motion(self):
        # Give the sensor an extra second for start up
        await asyncio.sleep(1)

        try:
            while True:
                # If sensor is tripped
                if GPIO.input(self.MOTION.SENSOR):
                    # If we haven't been tripped and this is a new motion
                    if self.MOTION.DETECTED == False:
                        # Append new motion
                        self._append_motion()
                    else:
                        # Keep our motion current
                        self.MOTION.CURRENT = datetime.now()

                else:
                    # Now always check if we can end a motion when we are not triggering
                    self._end_motion()

                await asyncio.sleep(0)
        except KeyboardInterrupt:
            print(f"Manual exit.")
        finally:
            # this ensures a clean exit
            GPIO.cleanup()

    async def _start_camera(self):
        pass

    def _end_motion(self):
        # Check if we are 15 seconds ahead of our motion's current
        delta = datetime.now() - self.MOTION.CURRENT
        self.MOTION.DETECTED = (
            False
            if self.MOTION.DETECTED == True and delta > self.MOTION_END_TIME_LAPSE
            else None
        )

        # Add an async function that kicks off a function that creates a directory, based on the current data
        # and moves all the video footage into it
        # NOTE: https://stackoverflow.com/questions/8858008/how-to-move-a-file-in-python
        # shutil.move() will copy and remove the original if you move the files to a different drive,
        # and I bet a USB would fall under this category


class DotDict(dict):
    """Utility code for added functionality for `dict` to access values easier/cleaner"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
