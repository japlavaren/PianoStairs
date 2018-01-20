import os
import glob
import subprocess
import collections


DEVNULL = open(os.devnull, 'wb')


class Piano(object):
    MAX_PARALLEL_PLAY = 4

    def __init__(self, tones_dir=None, player='aplay'):
        if tones_dir is None:
            tones_dir = os.path.dirname(__file__) + '/tones'

        self._tones_dir = tones_dir
        self._player = player
        self._tones = {os.path.basename(name).replace('.wav', '') for name in glob.glob('%s/*.wav' % tones_dir)}
        self._processes = collections.deque()

    def play(self, tone):
        if tone not in self._tones:
            raise ValueError('Unknown tone %s' % tone)

        self._kill_previous()

        cmd = '%s %s/%s.wav' % (self._player, self._tones_dir, tone)
        process = subprocess.Popen(cmd.split(), stdout=DEVNULL, stderr=subprocess.STDOUT)
        self._processes.appendleft(process)

    def _kill_previous(self):
        while len(self._processes) >= self.MAX_PARALLEL_PLAY:
            process = self._processes.pop()
            process.kill()
