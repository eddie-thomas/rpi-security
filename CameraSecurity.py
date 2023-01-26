import asyncio
import picamera
import RPi.GPIO as GPIO

from datetime import datetime, timedelta

from subprocess import Popen


class CameraSecurity:
    """Security system built with a DORHEA Camera Module w/ night-vision compatibility, and an HC-SR501 PIR Sensor module
    for motion detection.

    NOTE:
        - Project meant for development with async behavior in Python, and to see if I can get Google API access.
    """

    def __init__(self, motion_sensor_pin_number):
        """Construct object

        Args:
            motion_sensor_pin_number (int): Meant to be the RPi.GPIO.BCM pin number.

        NOTE:
            - This function invokes the `self._main()` method which calls the two async
            routines together.
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
        self.logger = True
        self.manual_kill = False
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
        """Method to start a new motion. This only happens if there is no currently active motion."""
        #  Set detected to true
        self.MOTION.DETECTED = True
        # Set the start date of the trip
        self.MOTION.START = datetime.now()
        # Append one to the motion count
        self.MOTION.COUNT += 1

    async def _detect_motion(self):
        """Asynchronous method to constantly run every second and check if the motion sensor has been triggered

        NOTE:
            - We expect this method to, independently, check for motion activity and when found, it will create
            append a motion. If a motion has already been created, and the motion sensor triggers, the active motion's
            `CURRENT` property will be reset with the current `datetime`. This way, we keep track of a motion's
            last known time when motion was actively triggering the sensor.
        """
        # Give the sensor an extra second for start up
        await asyncio.sleep(1)

        try:
            while not self.manual_kill:
                # If sensor is tripped
                if GPIO.input(self.MOTION.SENSOR):
                    self.logger and print("motion detected")
                    # If we haven't been tripped and this is a new motion
                    if self.MOTION.DETECTED == False:
                        # Append new motion
                        self._append_motion()
                    else:
                        # Keep our motion current
                        self.MOTION.CURRENT = datetime.now()

                else:
                    self.logger and print("no motion detected")
                    if self.MOTION.DETECTED:
                        # Now always check if we can end a motion when we are not triggering
                        self._kill_motion()

                await asyncio.sleep(1)
        except KeyboardInterrupt:
            self.logger and print(f"Manual exit.")
            self.manual_kill = True
        except BaseException as e:
            self.logger and print(e)
        finally:
            self.logger and print("GPIO cleanup")
            # this ensures a clean exit
            GPIO.cleanup()

    def _kill_camera(self):
        """Method to kill the camera

        NOTE:
            - We can kill the camera for multiple reasons, it will happen in the `finally` clause of the
            `_record_motion` method.
        """
        if self.camera:
            self.camera.stop_recording()
            self.CAMERA.STOPPED = True
            # Add the task of writing video file to an `.mp4` file
            asyncio.create_task(self._write_motion_to_file())

            self.camera.close()
            self.camera = None

    def _kill_motion(self):
        """Method to kill motion.

        NOTE:
            - We kill the active motion after 15 seconds. See the `MOTION_END_TIME_LAPSE` class constant
            to see where this delta is assigned
        """
        # Check if we are 15 seconds ahead of our motion's current
        delta = datetime.now() - self.MOTION.CURRENT
        if self.MOTION.DETECTED == True and delta > self.MOTION_END_TIME_LAPSE:
            self.logger and print("kill motion")
            # Set motion detected to false
            self.MOTION.DETECTED = False

    def _main(self):
        """Main method that kicks off the asynchronous methods that run the loops."""
        asyncio.run(self._run())

    async def _record_motion(self):
        """Record motion. Kind of a bad name, but this method will asynchronously run every second to
        determine if a motion has been created. If a motion is active, and there is not active recording being done
        start the camera and record. If we are recording, it is because motion has been detected and a recording
        was started to capture it. If the motion is no longer detecting (meaning it hasn't been triggered for 15+ seconds)
        then we can kill the camera.

        NOTE:
            - We recursively will call this method. So each time we invoke this method, it's only to capture one motion,
            start recording, and keep recording until the motion has been stagnate for 15+ seconds. Then we recurse.
        """
        try:
            while not self.manual_kill:
                # If sensor is tripped
                # Even if killing the camera takes a second or two to wrap up, we will still have recursed and ended up
                # with motion and another video being created
                if self.MOTION.DETECTED:
                    if not self.camera:
                        self.logger and print("create camera")
                        await self._start_camera()
                    self.logger and print("camera active - motion")
                    self.camera.wait_recording(1)
                else:
                    if self.camera:
                        self.logger and print("no motion - yes camera")

                        break
                    self.logger and print("no motion - no camera")

                await asyncio.sleep(1)

        except KeyboardInterrupt:
            self.logger and print(f"Manual exit.")
            self.manual_kill = True
        finally:
            self.logger and print("Camera killed")
            self._kill_camera()

        # Recursively call it again
        not self.manual_kill and await self._record_motion()

    async def _run(self):
        """Asynchronous method that adds the two co-routines to the main event loop"""
        motion_task = asyncio.create_task(self._detect_motion())
        recording_task = asyncio.create_task(self._record_motion())

        await asyncio.wait([motion_task, recording_task])

    async def _start_camera(self):
        """Method to start a recording

        NOTE:
            - To save energy, I kill the camera so if the motion sensor is inactive for multiple
            hour(s), we do not keep the camera rolling.
        """
        self.camera = picamera.PiCamera()
        self.camera.resolution = "HD"
        # Warm up camera
        await asyncio.sleep(1)

        self.camera.start_recording(f"motion_{self.MOTION.COUNT}.h264")
        self.CAMERA.STOPPED = False

    async def _write_motion_to_file(self):
        """Method that kicks off the writing process

        NOTE:
            - This sub-process is a CPU-heavy process,
            - We expect that many motions within a short time period will, hopefully,
            not bottleneck the CPU's memory, but this will need to be done in a trial
            by error
            - Because of the extra computation needed after a recording has finished,
            post-processing if you will, it would probably be best to kill recordings
            after a specific max length. So our CPU won't be overloaded with a process
            that could take minutes to hours to run.
        """
        self.logger and print("starting to write h264 file to mp4")
        Popen(["./scripts/parse.sh"])


class DotDict(dict):
    """Utility code for added functionality for `dict` to access values easier/cleaner"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
