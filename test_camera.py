import io
import random
import picamera


def motion_detected(length):
    # Randomly return True (like a fake motion detection routine)
    return True if length < 30 else False


def record_when_motion_detected():
    camera = picamera.PiCamera()
    # Set Camera resolution accordingly
    camera.resolution = "HD"

    stream = picamera.PiCameraCircularIO(camera, seconds=3)
    camera.start_recording(stream, format="h264")
    try:
        length = 0
        while True:
            camera.wait_recording(1)
            if motion_detected(length):
                camera.wait_recording(1)
                print(f"\nwaited for {length} seconds")
                length += 1

                break
    except KeyboardInterrupt:
        print(f"Manual exit.")
    finally:
        stream.copy_to("motion.h264")
        camera.stop_recording()


if __name__ == "__main__":
    record_when_motion_detected()
