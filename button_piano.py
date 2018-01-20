import time
import RPi.GPIO as GPIO
from piano import Piano


class ButtonPiano(Piano):
    def __init__(self, pin_tones, *args, **kwargs):
        super(ButtonPiano, self).__init__(*args, **kwargs)
        self._pin_tones = pin_tones

        GPIO.setmode(GPIO.BOARD)
        for pin in pin_tones.keys():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        for pin in self._pin_tones.keys():
            GPIO.add_event_detect(pin, GPIO.FALLING, self._play_pin, bouncetime=200)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()

    def _play_pin(self, pin):
        tone = self._pin_tones[pin]
        self.play(tone)


if __name__ == '__main__':
    piano = ButtonPiano(pin_tones={
        7: 'c1',
        11: 'd',
        13: 'e',
        15: 'f',
        12: 'g',
        16: 'a',
        18: 'b',
        22: 'c',
    })
    piano.run()
