import random
IDLE = 'idle'
ON = 'on'


def play_wav(file_name, speaker, loop=False, override_current_sound=True):
    print("playing", file_name)
    try:
        wave_file = open('sounds/' + file_name + '.wav', 'rb')
        wave = speaker.audioio.WaveFile(wave_file)
        if override_current_sound:
            speaker.audio.play(wave, loop=loop)
        else:
            while speaker.audio.playing:
                pass
            speaker.audio.play(wave, loop=loop)
    except Exception as e:
        print("Encountered exception: " + str(e))
        return


def wow(speaker):
    play_wav("wow" + str(random.randint(1, 6)), speaker)
