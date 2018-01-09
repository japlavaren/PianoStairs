import importlib.util
import RPi.GPIO as GPIO
from piano import Piano


class ButtonPiano(Piano):
    def __init__(self, buttons, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._buttons = buttons

        GPIO.setmode(GPIO.BOARD)
        for pin in buttons.keys():
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        try:
            while True:
                for tone, pin in self._buttons.items():
                    GPIO.add_event_detect(pin, GPIO.RISING, lambda _: self.play(tone))
        except KeyboardInterrupt:
            GPIO.cleanup()


if __name__ == '__main__':
    buttons = {
        'c1': 10,
        'd': 11,
        'e': 12,
        'f': 13,
        'g': 21,
        'a': 22,
        'b': 23,
        'c': 24,
    }
    piano = ButtonPiano(buttons)
    piano.run()
