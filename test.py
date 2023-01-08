import random
import picamera


def motion_detected():
    # Randomly return True (like a fake motion detection routine)
    return True


def record_when_motion_detected():
    camera = picamera.PiCamera()
    stream = picamera.PiCameraCircularIO(camera, seconds=20)
    camera.start_recording(stream, format="h264")
    try:
        while True:
            camera.wait_recording(1)
            if motion_detected():
                # Keep recording for 10 seconds and only then write the
                # stream to disk
                camera.wait_recording(10)
                stream.copy_to("motion.h264")
                break
    finally:
        camera.stop_recording()


if __name__ == "__main__":
    record_when_motion_detected()
