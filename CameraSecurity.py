import asyncio
import picamera
import RPi.GPIO as GPIO

from datetime import datetime, timedelta

from subprocess import Popen


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
        self.camera = None
        self.CAMERA = DotDict(
            {
                "STOPPED": True,
            }
        )
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

        # Run the camera and motion detection
        self._main()

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
                    print("motion detected")
                    # If we haven't been tripped and this is a new motion
                    if self.MOTION.DETECTED == False:
                        # Append new motion
                        self._append_motion()
                    else:
                        # Keep our motion current
                        self.MOTION.CURRENT = datetime.now()

                else:
                    print("no motion detected")
                    if self.MOTION.DETECTED:
                        # Now always check if we can end a motion when we are not triggering
                        self._kill_motion()

                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print(f"Manual exit.")
        except BaseException as e:
            print(e)
            raise e
        finally:
            print("GPIO cleanup")
            # this ensures a clean exit
            GPIO.cleanup()

    def _kill_camera(self):
        if self.camera:
            self.camera.close()
            self.camera = None

    def _kill_motion(self):
        # Check if we are 15 seconds ahead of our motion's current
        delta = datetime.now() - self.MOTION.CURRENT
        if self.MOTION.DETECTED == True and delta > self.MOTION_END_TIME_LAPSE:
            print("kill motion")
            # Set motion detected to false
            self.MOTION.DETECTED = False

    def _main(self):
        asyncio.run(self._run())

    async def _record_motion(self):
        try:
            while True:
                # If sensor is tripped
                # Even if killing the camera takes a second or two to wrap up, we will still have recursed and ended up
                # with motion and another video being created
                if self.MOTION.DETECTED:
                    if not self.camera:
                        print("create camera")
                        await self._start_camera()
                    print("camera active - motion")
                    self.camera.wait_recording(1)
                else:
                    if self.camera:
                        print("no motion - yes camera")
                        self.camera.stop_recording()
                        self.CAMERA.STOPPED = True
                        # Add the task of writing video file to an `.mp4` file
                        asyncio.create_task(self._write_motion_to_file())
                        break
                    print("no motion - no camera")

                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print(f"Manual exit.")
        finally:
            print("Camera killed")
            self._kill_camera()
            # Recursively call it again
            await self._record_motion()

    async def _run(self):
        motion_task = asyncio.create_task(self._detect_motion())
        recording_task = asyncio.create_task(self._record_motion())

        await asyncio.wait([motion_task, recording_task])

    async def _start_camera(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = "HD"
        # Warm up camera
        await asyncio.sleep(1)

        self.camera.start_recording(f"motion_{self.MOTION.COUNT}.h264")

    async def _write_motion_to_file(self):
        print("starting to write h264 file to mp4")
        Popen(["./scripts/parse.sh"])


class DotDict(dict):
    """Utility code for added functionality for `dict` to access values easier/cleaner"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
