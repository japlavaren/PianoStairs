import os
import glob
import time
import threading
import subprocess


DEVNULL = open(os.devnull, 'wb')


class Piano(object):
    TERMINATE_DELAY = 0.3

    def __init__(self, tones_dir=None, player='aplay'):
        if tones_dir is None:
            tones_dir = os.path.dirname(__file__) + '/tones'

        self._tones_dir = tones_dir
        self._player = player
        self._tones = {os.path.basename(name).replace('.wav', '') for name in glob.glob('%s/*.wav' % tones_dir)}
        self._processes = {}

    def play(self, tone):
        if tone not in self._tones:
            raise ValueError('Unknown tone %s' % tone)

        self._cancel_previous(tone)

        cmd = '%s %s/%s.wav' % (self._player, self._tones_dir, tone)
        p = subprocess.Popen(cmd.split(), stdout=DEVNULL, stderr=subprocess.STDOUT)
        self._processes[tone] = p

    def _cancel_previous(self, tone):
        prev_process = self._processes.get(tone)

        # previous tone is still playing
        if prev_process and prev_process.poll() is None:
            t = threading.Thread(target=self._schedule_terminate, args=(prev_process, ))
            t.start()

    @classmethod
    def _schedule_terminate(cls, process):
        time.sleep(cls.TERMINATE_DELAY)
        process.kill()
