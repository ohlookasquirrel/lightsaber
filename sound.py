import random


def play_wav(file_name, speaker, override_current_sound=True):
    print("playing", file_name)
    try:
        wave_file = open('sounds/' + file_name + '.wav', 'rb')
        wave = speaker.audioio.WaveFile(wave_file)
        if override_current_sound:
            speaker.audio.play(wave, loop=False)
        else:
            while speaker.audio.playing:
                pass
            speaker.audio.play(wave, loop=False)
    except Exception as e:
        print("Encountered exception: " + str(e))
        return


class Lightsaber:

    @staticmethod
    def idle():
        return 'idle'

    @staticmethod
    def clash():
        return "clash%s" % random.randint(1, 6)

    @staticmethod
    def swing():
        return "swing%s" % random.randint(1, 9)

    @staticmethod
    def on():
        return 'on'

    @staticmethod
    def off():
        return 'off'


class Wowsaber:
    @staticmethod
    def idle():
        return 'idle'

    @staticmethod
    def clash():
        return "wow%s" % random.randint(1, 6)

    @staticmethod
    def swing():
        return 'wow-swing'

    @staticmethod
    def on():
        return 'on'

    @staticmethod
    def off():
        return 'off'
