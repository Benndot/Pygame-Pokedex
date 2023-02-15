import random
import pygame
from pygame import mixer
import sys
import requests
import io
from urllib.request import urlopen

pygame.init()

clock = pygame.time.Clock()

# you can access PokeAPI both by the Pokemon species' name and by their national Pokédex number


class MusicSettings:

    volume_level = 50
    music_paused = False
    spooky_song = "audio/Pokemon BlueRed - Lavender Town.mp3"
    current_track_index = 0
    tracklist = ["audio/Pokemon Ruby- Littleroot Town.mp3", "audio/Pokemon Ruby- Route 101.mp3",
                 "audio/Pokemon Ruby- Route 104.mp3"]

    def music_toggle(self):
        print("The music pausing bool has been toggled")
        self.music_paused = not self.music_paused
        if self.music_paused:
            mixer.music.pause()
        elif not self.music_paused:
            mixer.music.unpause()

    def change_music_volume(self):
        print(self.volume_level)

    def randomize_song(self):
        self.current_track_index = random.randint(0, len(self.tracklist)-1)
        print(f"Index chosen: {self.current_track_index}")
        mixer.music.load(self.tracklist[self.current_track_index])
        mixer.music.set_volume(MusicSettings.volume_level / 350)
        mixer.music.play(-1)


mixer.init()
music_object = MusicSettings()
music_object.randomize_song()


def get_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        print("sucessfully fetched the data")
        return response.json()
    else:
        print(f"Hello person, there's a {response.status_code} error with your request")


screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)


def resize_screen():
    global screen
    global screen_width
    global screen_height
    if screen_width == 1080:
        screen_width = 1600
        screen_height = 900
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    elif screen_width == 1600:
        screen_width = 1920
        screen_height = 1080
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    else:
        screen_width = 1080
        screen_height = 720
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)


# Setting different sized font options to be used later for general text and button labels
large_font = pygame.font.SysFont("comicsansms", 50)
medium_font = pygame.font.SysFont("comicsansms", 30)
small_font = pygame.font.SysFont("comicsansms", 16)

# Establishing a number of reusable rgb values for several colors
slategray = (112, 128, 144)
lightgray = (165, 175, 185)
blackish = (10, 10, 10)
thunderbird_red = (200, 15, 25)
white = (255, 255, 255)
green = (0, 255, 0)
thistle_green = (210, 210, 190)
black = (0, 0, 0)


def create_text_button(font_choice, text_color, msg, x, y, hover_color, default_color, x_adjust: bool):

    mouse = pygame.mouse.get_pos()

    button_msg = font_choice.render(msg, True, text_color)

    button_width = button_msg.get_width() + (button_msg.get_width() * 0.20)
    button_height = button_msg.get_height() + (button_msg.get_height() * 0.20)

    if x_adjust:
        x = x - (button_width / 2)

    # The experimental version
    if x + button_width > mouse[0] > x and y + button_height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, button_width, button_height))
        for evnt in pygame.event.get():
            if evnt.type == pygame.MOUSEBUTTONUP:
                return True
    else:
        pygame.draw.rect(screen, default_color, (x, y, button_width, button_height))

    screen.blit(button_msg, (x + button_width / 10, y + button_height / 10))


def pokemon_search():

    header_text = large_font.render("Pokedex Search", True, black)

    while True:

        screen.fill(thistle_green)

        screen.blit(header_text, ((screen_width - header_text.get_width())/2, 0))

        resize_button = create_text_button(medium_font, thunderbird_red, "Resize", screen_width / 90,
                                           screen_height * 0.85, blackish, black, False)

        if resize_button:
            resize_screen()

        randomize_button = create_text_button(medium_font, thunderbird_red, "Randomize", screen_width / 90,
                                              screen_height * 0.75, blackish, black, False)

        if randomize_button:
            pokemon_display()

        return_button = create_text_button(medium_font, white, "Return", screen_width * .87,
                                           screen_height * 0.85, (0, 200, 0), green, False)

        if return_button:
            print("return")

        music_toggle = create_text_button(medium_font, white, "Toggle Music", screen_width * .775,
                                          screen_height * 0.75, (0, 200, 0), green, False)

        if music_toggle:
            music_object.music_toggle()

        options_button = create_text_button(medium_font, white, "Options Menu", screen_width * .775,
                                            screen_height * 0.65, (0, 200, 0), green, False)

        if options_button:
            options_menu()

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def options_menu():

    title_text = large_font.render("Options Menu", True, blackish)

    while True:
        screen.fill(thistle_green)
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 0))

        music_button = create_text_button(medium_font, white, "Toggle Music", screen_width / 1.97,
                                          screen_height / 6.5, lightgray, slategray, True)
        if music_button:
            music_object.music_toggle()

        # Bool declaration
        music_pause_declaration = "Yes" if music_object.music_paused else "No"
        music_paused_text = medium_font.render(f"Music Paused: " + music_pause_declaration, True, blackish)
        bool_text_x = (screen_width - music_paused_text.get_width()) / 2
        bool_text_y = (screen_height - music_paused_text.get_height()) / 3.8
        screen.blit(music_paused_text, (bool_text_x, bool_text_y))

        # Creating the (purely aesthetic) volume setting, including 2 buttons and the volume level display
        volume_height = screen_height / 2.8
        volume_text = medium_font.render(f"{music_object.volume_level}", True, black)
        volume_text_x = (screen_width / 2) - (volume_text.get_width() / 2) + 5
        screen.blit(volume_text, (volume_text_x, volume_height - 10))

        volume_up_button = create_text_button(small_font, white, "Volume +", screen_width / 2.25,
                                              volume_height, slategray, lightgray, True)

        volume_down_button = create_text_button(small_font, white, "Volume -", screen_width / 1.75,
                                                volume_height, slategray, lightgray, True)

        if volume_up_button:
            print("volume increased!")
            music_object.volume_level += 10
            if music_object.volume_level > 100:
                music_object.volume_level = 100
            mixer.music.set_volume(music_object.volume_level/350)
        if volume_down_button:
            print("volume decreased!")
            music_object.volume_level -= 10
            if music_object.volume_level < 0:
                music_object.volume_level = 0
            mixer.music.set_volume(music_object.volume_level/350)

        if music_object.volume_level == 0:
            muted_text = medium_font.render("(muted)", True, thunderbird_red)
            screen.blit(muted_text, (volume_text_x * .92, volume_height + 25))

        music_changer = create_text_button(large_font, white, "Change Music Track", screen_width / 2,
                                           screen_height / 2.2, slategray, lightgray, True)

        if music_changer:
            print("Track change initiated")
            mixer.music.stop()
            music_object.current_track_index += 1
            if music_object.current_track_index >= len(music_object.tracklist):
                music_object.current_track_index = 0
            mixer.music.load(music_object.tracklist[music_object.current_track_index])
            mixer.music.set_volume(music_object.volume_level/350)
            mixer.music.play(-1)

        current_track_name = music_object.tracklist[music_object.current_track_index][6:-4] if \
            music_object.current_track_index != 13 else "    ????????????????????"
        current_track_text = small_font.render(f'Current Track: ' + current_track_name, True, blackish)
        screen.blit(current_track_text, (screen_width / 2.8, screen_height / 1.6))

        # Return to start menu button
        return_button = create_text_button(medium_font, white, "Return To Start", screen_width / 2,
                                           screen_height / 1.25, slategray, lightgray, True)

        if return_button:
            main()

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def pokemon_display():

    top_bar_height = screen_height / 10

    random_pokemon_index = random.randint(1, 800)

    try:
        pokemon_obj = get_data(f"https://pokeapi.co/api/v2/pokemon/{random_pokemon_index}")
        screen_background_image_url = pokemon_obj["sprites"]["front_default"]
        pokemon_name_string, pokemon_id_number = pokemon_obj["name"].title(), pokemon_obj["id"]
        pokemon_name_text = large_font.render(f"#{pokemon_id_number}. {pokemon_name_string}", True, white)
        pokemon_type1_string = pokemon_obj["types"][0]["type"]["name"].title()
        pokemon_type1_text = large_font.render(pokemon_type1_string, True, white)
        pokemon_type2_string = pokemon_obj["types"][1]["type"]["name"] if not IndexError else "n/a"
        pokemon_type2_text = large_font.render(pokemon_type2_string, True, white)

    except TypeError:
        print("There was an error, deploying placeholders")
        screen_background_image_url = "https://avatars.githubusercontent.com/u/32001362?v=4"
        pokemon_name_string = "Error / Pokemon Not Found"
        pokemon_name_text = large_font.render(pokemon_name_string, True, white)
        pokemon_type1_text = large_font.render("N/A", True, white)
        pokemon_type2_text = large_font.render("N/A", True, white)

    screen_background_image_string = urlopen(screen_background_image_url).read()

    screen_background_image_file = io.BytesIO(screen_background_image_string)

    # print(type(screen_background_image_string))  # bytes class
    # print(type(screen_background_image_file))  # io.BytesI0

    screen_background_image = pygame.image.load(screen_background_image_file)

    print(screen_background_image.get_width(), screen_background_image.get_height())

    # Scales the start screen image to the screen size
    poke_photo = pygame.transform.scale(screen_background_image, (screen_width / 2.5, screen_width / 2.5))

    while True:

        screen.fill(slategray)

        screen.blit(pokemon_name_text, ((screen_width - pokemon_name_text.get_width())/2, screen_height / 30))

        screen.blit(poke_photo, ((screen_width - poke_photo.get_width()) / 2, top_bar_height * 1.1))

        screen.blit(pokemon_type1_text, ((screen_width - pokemon_type1_text.get_width())/2, screen_height * 0.7))

        screen.blit(pokemon_type2_text, ((screen_width - pokemon_type1_text.get_width()) / 2, screen_height * 0.8))

        resize_button = create_text_button(medium_font, thunderbird_red, "Resize", screen_width / 90,
                                           screen_height * 0.85, blackish, black, False)

        if resize_button:
            resize_screen()

        randomize_button = create_text_button(medium_font, thunderbird_red, "Randomize", screen_width / 90,
                                              screen_height * 0.75, blackish, black, False)

        if randomize_button:
            pokemon_display()

        return_button = create_text_button(medium_font, white, "Return", screen_width * .85,
                                           screen_height * 0.85, (0, 200, 0), green, False)

        if return_button:
            print("return")

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def main():
    while True:

        pokemon_search()

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":

    # print(get_data("https://pokeapi.co/api/v2/pokemon/eevee").keys())
    # print(get_data("https://pokeapi.co/api/v2/pokemon/eevee")["sprites"].keys())
    # print(get_data("https://pokeapi.co/api/v2/pokemon/seedot")["types"][1]["type"]["name"])

    print(MusicSettings.volume_level)

    main()
