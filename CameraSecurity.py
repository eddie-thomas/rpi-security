class CameraSecurity:
    """Security system built with a DORHEA Camera Module w/ night-vision compatibility, and an HC-SR501 PIR Sensor module
    for motion detection.

    Notes: Project meant for development with async behavior in Python, and to see if I can get Google API access.
    """

    def __init__(self, motion_sensor_pin_number):
        """Construct object

        Args:
            motion_sensor_pin_number (int): Meant to be the RPi.GPIO.BCM pin number.
        """
        self.motion_pin_number = motion_sensor_pin_number
        # Set up camera
        # Set up motion sensor to start up and continuously set whether motion has happened
        # Set up camera to record when motion detected and continue recording for 15 seconds
        #   after the motion has stopped. Read up on what `wait_recording()` can actually do
        # Get shell script to instantiate this object and start up motion sensor to record when motionis active
