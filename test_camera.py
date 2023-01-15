import io
import random
import picamera


def motion_detected():
    # Randomly return True (like a fake motion detection routine)
    return True


def record_when_motion_detected():
    camera = picamera.PiCamera()
    # Set Camera resolution accordingly
    camera.resolution = "HD"

    stream = picamera.PiCameraCircularIO(camera, seconds=20)
    camera.start_recording(stream, format="h264")
    try:
        while True:
            camera.wait_recording(1)
            if motion_detected():
                # Keep recording for 10 seconds and only then write the
                # stream to disk
                camera.wait_recording(10000000000000)
                # camera.resolution = (800, 600)
                # camera.start_preview()
                # camera.start_recording('foo.h264')
                # camera.wait_recording(10)
                # camera.capture('foo.jpg', use_video_port=True)
                # camera.wait_recording(10)
                # camera.stop_recording()

                break
    except KeyboardInterrupt:
        print(f"Manual exit.")
    finally:
        stream.copy_to("motion.h264")
        camera.stop_recording()


if __name__ == "__main__":
    record_when_motion_detected()
