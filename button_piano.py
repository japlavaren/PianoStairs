import time
import RPi.GPIO as GPIO
from piano import Piano


class ButtonPiano(Piano):
    def __init__(self, buttons, *args, **kwargs):
        super(ButtonPiano, self).__init__(*args, **kwargs)
        self._buttons = buttons

        GPIO.setmode(GPIO.BOARD)
        for pin in buttons.values():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        for tone, pin in self._buttons.items():
            GPIO.add_event_detect(pin, GPIO.FALLING, lambda _: self.play(tone))

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            GPIO.cleanup()


if __name__ == '__main__':
    buttons = {
        'c1': 7,
        'd': 11,
        'e': 13,
        'f': 15,
        'g': 12,
        'a': 16,
        'b': 18,
        'c': 22,
    }
    piano = ButtonPiano(buttons)
    piano.run()
