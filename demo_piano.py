import time
from piano import Piano


class DemoPiano(Piano):
    DELAY = 1

    def run_demo(self):
        tones = ['c1', 'd', 'e', 'f', 'g', 'a', 'b', 'c']
        for tone in tones:
            self.play(tone)
            time.sleep(self.DELAY)

        chords = [('c1', 'e', 'g'), ('d', 'f', 'a'), ('e', 'g', 'b'), ('f', 'a', 'c')]
        for tones in chords:
            for tone in tones:
                self.play(tone)

            time.sleep(self.DELAY)


if __name__ == '__main__':
    piano = DemoPiano()
    piano.run_demo()
