import RPi.GPIO as GPIO
import time

COUNT = 0


def main():
    GPIO.setmode(GPIO.BCM)

    MOTION_SENSOR = 16
    # Set up the input connector to check for when the motion sensor is tipped off
    GPIO.setup(MOTION_SENSOR, GPIO.IN)

    print("Starting up the PIR Module (type CTRL-C to exit)")
    time.sleep(1)
    print("Ready")
    try:
        while True:
            if GPIO.input(MOTION_SENSOR):
                COUNT += 1
                print(f"Motion Detected: {COUNT}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print(f"Manual exit.")
    finally:
        # this ensures a clean exit
        GPIO.cleanup()


if __name__ == "__main__":
    main()
