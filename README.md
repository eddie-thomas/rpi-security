# RPi-Security

Security systems are one of the most useful and interesting IoT projects. A simple camera can cost a fortune, and why pay for some subscription/equipment when you can do it yourself! I developed an extremely simple, yet effective, surveillance system that will use a basic motion sensor to start a recording, and when the motion has stopped for a set amount of time, the video will be ended and saved off. To save on energy, the camera is only active when motion is detected, and when the motion is considered "dead", the camera is turned off as well.

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Prerequisites

Requirements for the software and other tools to build, test and push

- [Python +3.7](https://www.python.org/)
- [Raspbian OS](https://www.raspberrypi.com/software/)

### Installing

Once on your Raspberry Pi, navigate to the appropriate directory and preform the following commands.

Clone the repo:

```sh
git clone git@github.com:eddie-thomas/rpi-security.git
```

Initialize your Python virtual environment:

- This installs all the required dependencies

```sh
$root/scripts/python3/initialize.sh
```

Make sure your hardware is set up, see [this article](https://www.freva.com/hc-sr501-pir-motion-sensor-on-raspberry-pi/) for setting up the motion sensor. The code as is, expects the motion sensors pin to be on pin 23 when `GPIO.BCM`.

With a camera and the motion sensor connected, and the appropriate settings on the Raspberry Pi have been set, you can start the system:

```sh
$root/scripts/run.sh
```

## Running the tests

Currently there are no automated tests

## Deployment

To deploy this for your home or garage, in a "live-production", you must first outfit your Raspberry Pi with the appropriate settings. This is removing as much access as possible to the Pi, remotely speaking. However secure you need the Pi to be, you can add any addition measures and you see fit. For reference to a few choices that can increase security for the Pi:

- Firewall, lock down all ports and add limits to the open ones
- Backing up the recorded images, either to a physical back-up or to the cloud (this would make a very cool Google Drive API project)
- If remote access is allowed, make sure it's on a user that has the bare minimum of privileges

The video footage is great to have and reassuring if you knew it was backed up, but an added bonus to deploying could be making an API route for getting access to the footage, so either show visually via a front-end service.

## Built With

- [LEGO](https://www.lego.com/)
- [Raspberry Pi](https://www.raspberrypi.com/)
- HC-SR501 motion sensor
- Raspberry Pi Camera
- Homemade jumper wires

## Contributing (Coming soon)

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code
of conduct, and the process for submitting pull requests to us.

## Versioning

v.1.0.1

## Authors

- **Edward Thomas** - Check out my [portfolio](https://eddie-thomas.github.io/portfolio/)!

## License

- Copyright © 2018 - 2023 by Edward K Thomas Jr
- GNU GENERAL PUBLIC LICENSE https://www.gnu.org/licenses/gpl-3.0.en.html
