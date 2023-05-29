from pygame import mixer
import random


class MusicSettings:

    volume_level = 50
    music_paused = False
    spooky_song = "audio/Pokemon BlueRed - Lavender Town.mp3"
    current_track_index = 0
    tracklist = ["audio/Pokemon Ruby- Littleroot Town.mp3", "audio/Pokemon Ruby- Route 101.mp3",
                 "audio/Pokemon Ruby- Route 104.mp3", "audio/Pokemon HGSS - Violet City theme.mp3",
                 "audio/Pokemon HGSS - Global Terminal Theme.mp3"]

    def music_toggle(self):
        print("The music pausing bool has been toggled")
        self.music_paused = not self.music_paused
        if self.music_paused:
            mixer.music.pause()
        elif not self.music_paused:
            mixer.music.unpause()

    def change_music_volume(self, change_int: int):
        self.volume_level += change_int
        if self.volume_level > 100:
            self.volume_level = 100
        if self.volume_level < 0:
            self.volume_level = 0
        mixer.music.set_volume(self.volume_level / 350)

    def randomize_song(self):
        self.current_track_index = random.randint(0, len(self.tracklist)-1)
        print(f"Index chosen: {self.current_track_index}")
        mixer.music.load(self.tracklist[self.current_track_index])
        mixer.music.set_volume(MusicSettings.volume_level / 350)
        mixer.music.play(-1)

    def cycle_track(self):
        mixer.music.stop()
        self.current_track_index += 1
        if self.current_track_index >= len(self.tracklist):
            self.current_track_index = 0
        mixer.music.load(self.tracklist[self.current_track_index])
        mixer.music.set_volume(self.volume_level / 350)
        mixer.music.play(-1)
