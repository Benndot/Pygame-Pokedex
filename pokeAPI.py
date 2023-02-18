import math
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

    def change_music_volume(self, change_int: int):
        self.volume_level += change_int
        if self.volume_level > 100:
            self.volume_level = 100
        if self.volume_level < 0:
            self.volume_level = 0
        mixer.music.set_volume(music_object.volume_level / 350)

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


mixer.init()
music_object = MusicSettings()
music_object.randomize_song()


class GameScreen:
    width = 1080
    height = 720
    screen = pygame.display.set_mode((width, height))

    def resize_screen(self):
        if self.width == 1080:
            self.width = 1600
            self.height = 900
            self.screen = pygame.display.set_mode((self.width, self.height))
        elif self.width == 1600:
            self.width = 1920
            self.height = 1080
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        else:
            self.width = 1080
            self.height = 720
            self.screen = pygame.display.set_mode((self.width, self.height))


game_screen = GameScreen()


class Pokedex:

    def __init__(self, display_counter: int, display_limit: int, offset_counter: int):
        self.d_count = display_counter
        self.d_limit = display_limit
        self.o_count = offset_counter


pokedex = Pokedex(0, 9, 0)


class CurrentPokemon:

    substitute_image = "https://avatars.githubusercontent.com/u/32001362?v=4"

    placeholder_entry = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt 
    ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut 
    aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu 
    fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit 
    anim id est laborum."""

    def __init__(self, dex_no, name, image_url, type1, type2, stat_array, dex_entry):
        self.dex_no = dex_no
        self.name = name
        self.image_url = image_url
        self.type1 = type1
        self.type2 = type2
        self.stats = stat_array
        self.dex_entry = dex_entry


current_pokemon = CurrentPokemon(-1, "Placeholder", CurrentPokemon.substitute_image, "N/A", "N/A",
                                 [["health", "hp", -1], ["attack", "p. atk", -1], ["defense", "p. def", -1],
                                  ["special attack", "s. atk", -1], ["special defense", "s. def", -1],
                                  ["speed", "spd", -1]], CurrentPokemon.placeholder_entry)


def get_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Hello person, there's a {response.status_code} error with your request")


# Setting different sized font options to be used later for general text and button labels
large_font = pygame.font.SysFont("comicsansms", math.ceil(game_screen.height * 0.0695))
intermediate_font = pygame.font.SysFont("comicsansms", math.ceil(game_screen.height * 0.0695 * 0.8))
medium_font = pygame.font.SysFont("comicsansms", math.ceil(game_screen.height * 0.0695 * 0.6))
sml_med_font = pygame.font.SysFont("comicsansms", math.ceil(game_screen.height * 0.0695 * 0.45))
small_font = pygame.font.SysFont("comicsansms", math.ceil(game_screen.height * 0.0695 * 0.33))

# Establishing a number of reusable rgb values for several colors
slategray = (112, 128, 144)
lightgray = (165, 175, 185)
blackish = (20, 20, 20)
thunderbird_red = (200, 15, 25)
white = (255, 255, 255)
green = (0, 255, 0)
thistle_green = (210, 210, 190)
black = (0, 0, 0)


def create_onscreen_text(font_size, color, message, x, y,):

    text = font_size.render(message, True, color)

    game_screen.screen.blit(text, (x, y))


def create_transparent_button(width, height, x, y):

    mouse = pygame.mouse.get_pos()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        s = pygame.Surface((width, height))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill((255, 255, 255))  # this fills the entire surface
        game_screen.screen.blit(s, (x, y))  # (0,0) are the top-left coordinates
        for evnt in pygame.event.get():
            if evnt.type == pygame.MOUSEBUTTONUP:
                return True


def create_text_button(font_choice, text_color, msg, x, y, hover_color, default_color, x_adjust: bool):

    mouse = pygame.mouse.get_pos()

    button_msg = font_choice.render(msg, True, text_color)

    button_width = button_msg.get_width() + (button_msg.get_width() * 0.20)
    button_height = button_msg.get_height() + (button_msg.get_height() * 0.20)

    if x_adjust:
        x = x - (button_width / 2)

    # The experimental version
    if x + button_width > mouse[0] > x and y + button_height > mouse[1] > y:
        pygame.draw.rect(game_screen.screen, hover_color, (x, y, button_width, button_height))
        for evnt in pygame.event.get():
            if evnt.type == pygame.MOUSEBUTTONUP:
                return True
    else:
        pygame.draw.rect(game_screen.screen, default_color, (x, y, button_width, button_height))

    game_screen.screen.blit(button_msg, (x + button_width / 10, y + button_height / 10))


def start_screen():

    start_text = medium_font.render("The Pygame Pokedex", True, white)

    top_bar_height = 70

    title_photo = pygame.image.load("pokePics/pokedex-spooky.jpg")

    # Scales the start screen image to the screen size
    start_photo = pygame.transform.scale(title_photo, (game_screen.width, game_screen.height - top_bar_height))

    while True:
        game_screen.screen.fill((0, 0, 200))
        game_screen.screen.blit(start_text, ((game_screen.width - start_text.get_width()) / 2, game_screen.height / 65))

        menu_button = create_text_button(small_font, blackish, "Open Menu", game_screen.width * .9,
                                         game_screen.height * 0.03, lightgray, slategray, True)

        if menu_button:
            pokemon_search()
            # return

        music_button = create_text_button(small_font, blackish, "Toggle Music", game_screen.width * .78,
                                          game_screen.height * 0.03, lightgray, slategray, True)

        if music_button:
            music_object.music_toggle()

        ghost_button = create_transparent_button(250, 100, game_screen.width / 1.75, game_screen.height / 2.8)

        if ghost_button:
            print("Ghost button clicked!")
            mixer.music.load(music_object.spooky_song)
            mixer.music.set_volume(music_object.volume_level / 350)
            mixer.music.play(-1)
            music_object.current_track_index = 13

        game_screen.screen.blit(start_photo, (0, 70))

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)
        return True


def options_menu():

    title_text = large_font.render("Options Menu", True, blackish)

    while True:
        game_screen.screen.fill(thistle_green)
        game_screen.screen.blit(title_text, ((game_screen.width - title_text.get_width()) / 2, 0))

        music_button = create_text_button(medium_font, white, "Toggle Music", game_screen.width / 1.97,
                                          game_screen.height / 6.5, lightgray, slategray, True)
        if music_button:
            music_object.music_toggle()

        # Bool declaration
        music_pause_declaration = "Yes" if music_object.music_paused else "No"
        music_paused_text = medium_font.render(f"Music Paused: " + music_pause_declaration, True, blackish)
        bool_text_x = (game_screen.width - music_paused_text.get_width()) / 2
        bool_text_y = (game_screen.height - music_paused_text.get_height()) / 3.8
        game_screen.screen.blit(music_paused_text, (bool_text_x, bool_text_y))

        volume_height = game_screen.height / 2.8
        volume_text = medium_font.render(f"{music_object.volume_level}", True, black)
        volume_text_x = (game_screen.width / 2) - (volume_text.get_width() / 2) + 5
        game_screen.screen.blit(volume_text, (volume_text_x, volume_height - 10))

        volume_up_button = create_text_button(small_font, white, "Volume +", game_screen.width / 2.25,
                                              volume_height, slategray, lightgray, True)

        volume_down_button = create_text_button(small_font, white, "Volume -", game_screen.width / 1.75,
                                                volume_height, slategray, lightgray, True)

        if volume_up_button:
            print("volume increased!")
            music_object.change_music_volume(10)
        if volume_down_button:
            print("volume decreased!")
            music_object.change_music_volume(-10)

        if music_object.volume_level == 0:
            muted_text = medium_font.render("(muted)", True, thunderbird_red)
            game_screen.screen.blit(muted_text, (volume_text_x * .92, volume_height + 25))

        music_changer = create_text_button(large_font, white, "Change Music Track", game_screen.width / 2,
                                           game_screen.height / 2.2, slategray, lightgray, True)

        if music_changer:
            print("Track change initiated")
            music_object.cycle_track()

        current_track_name = music_object.tracklist[music_object.current_track_index][6:-4] if \
            music_object.current_track_index != 13 else "    ????????????????????"
        current_track_text = small_font.render(f'Current Track: ' + current_track_name, True, blackish)
        game_screen.screen.blit(current_track_text, (game_screen.width / 2.8, game_screen.height / 1.6))

        # Return to start menu button
        return_button = create_text_button(medium_font, white, "Return To Start", game_screen.width / 2,
                                           game_screen.height / 1.25, slategray, lightgray, True)

        if return_button:
            main()

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def pokemon_search():

    header_text = large_font.render("Pokedex Search", True, black)

    while True:

        pokemon_list_object = get_data(f"https://pokeapi.co/api/v2/pokemon?offset={pokedex.o_count}&limit="
                                       f"{pokedex.d_limit}")

        game_screen.screen.fill(thistle_green)

        game_screen.screen.blit(header_text, ((game_screen.width - header_text.get_width()) / 2, 0))

        pokemon_name_height = game_screen.height * 0.13
        multi_factor = 1
        pokedex.d_count = 0
        for poke in pokemon_list_object["results"]:

            poke_button = create_text_button(sml_med_font, white, f"{poke['name']}", game_screen.width / 3.5,
                                             pokemon_name_height * multi_factor, blackish, black, False)
            if poke_button:
                print(f"{poke['name']}")
                pokemon_display(poke['url'])

            pokedex.d_count += 1
            multi_factor += 0.72

            if pokedex.d_count >= pokedex.d_limit:
                break

        back_button = create_text_button(medium_font, white, "Back", game_screen.width / 90,
                                         game_screen.height * 0.78, (0, 200, 0), green, False)

        if back_button:
            pokedex.o_count -= 9
            if pokedex.o_count < 0:
                pokedex.o_count = 0

        resize_button = create_text_button(sml_med_font, thunderbird_red, "Resize", game_screen.width / 90,
                                           game_screen.height * 0.90, blackish, black, False)

        if resize_button:
            game_screen.resize_screen()

        randomize_button = create_text_button(sml_med_font, thunderbird_red, "Randomize", game_screen.width / 90,
                                              game_screen.height * 0, blackish, black, False)

        if randomize_button:
            pokemon_display('random')

        next_button = create_text_button(medium_font, white, "Next", game_screen.width * .82,
                                         game_screen.height * 0.78, (0, 200, 0), green, False)

        if next_button:
            pokedex.o_count += 9

        music_toggle = create_text_button(sml_med_font, thunderbird_red, "Toggle Music", game_screen.width * .82,
                                          game_screen.height * 0.90, blackish, black, False)

        if music_toggle:
            music_object.music_toggle()

        options_button = create_text_button(medium_font, white, "Options Menu", game_screen.width * .775, 0,
                                            (0, 200, 0), green, False)

        if options_button:
            options_menu()

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def pokemon_display(url):

    top_bar_height = game_screen.height / 10

    if url == "random":
        random_pokemon_index = random.randint(1, 800)
        url = f"https://pokeapi.co/api/v2/pokemon/{random_pokemon_index}"

    try:
        pokemon_obj = get_data(url)
        current_pokemon.image_url = pokemon_obj["sprites"]["front_default"]
        current_pokemon.name, current_pokemon.dex_no = pokemon_obj["name"].title(), pokemon_obj["id"]
        current_pokemon.type1 = pokemon_obj["types"][0]["type"]["name"].title()
        current_pokemon.type2 = "n/a"
        for index, stat in enumerate(pokemon_obj["stats"]):
            current_pokemon.stats[index][2] = stat['base_stat']
        print(current_pokemon.stats)
        try:
            current_pokemon.type2 = pokemon_obj["types"][1]["type"]["name"].title()
        except IndexError:
            pass

    except TypeError:
        print("There was an error, deploying placeholders")

    pkmn_name_text = large_font.render(f"#{current_pokemon.dex_no}. {current_pokemon.name}", True, white)
    pkmn_type1_text = intermediate_font.render(f"Type 1:    {current_pokemon.type1}", True, white)
    pkmn_type2_text = intermediate_font.render(f"Type 2:    {current_pokemon.type2}", True, white)

    screen_background_image_url = urlopen(current_pokemon.image_url).read()
    screen_background_image_file = io.BytesIO(screen_background_image_url)
    screen_background_image = pygame.image.load(screen_background_image_file)

    print(screen_background_image.get_width(), screen_background_image.get_height())

    # Scales the start screen image to the screen size
    poke_photo = pygame.transform.scale(screen_background_image, (game_screen.width / 2.5,
                                                                  game_screen.width / 2.5))

    while True:

        game_screen.screen.fill(slategray)

        game_screen.screen.blit(pkmn_name_text, ((game_screen.width - pkmn_name_text.get_width()) / 2,
                                                 game_screen.height / 30))

        create_onscreen_text(medium_font, black, "Base Stats", game_screen.width * 0.02, game_screen.height * 0.002)
        create_onscreen_text(medium_font, black, "_________", game_screen.width * 0.02, game_screen.height * 0.006)

        stat_height_multiplier = 1.00
        for stat in current_pokemon.stats:
            create_onscreen_text(sml_med_font, black, f"{stat[1]}: {stat[2]}", game_screen.width * 0.025,
                                 game_screen.height * 0.08 * stat_height_multiplier)
            stat_height_multiplier += 1

        game_screen.screen.blit(poke_photo, ((game_screen.width - poke_photo.get_width()) / 2,
                                             top_bar_height * 1.1))

        game_screen.screen.blit(pkmn_type1_text, ((game_screen.width - pkmn_type1_text.get_width()) / 2,
                                                  game_screen.height * 0.7))

        game_screen.screen.blit(pkmn_type2_text, ((game_screen.width - pkmn_type1_text.get_width()) / 2,
                                                  game_screen.height * 0.8))

        resize_button = create_text_button(medium_font, thunderbird_red, "Resize", game_screen.width / 90,
                                           game_screen.height * 0.85, blackish, black, False)

        if resize_button:
            game_screen.resize_screen()

        randomize_button = create_text_button(medium_font, thunderbird_red, "Randomize", game_screen.width / 90,
                                              game_screen.height * 0.75, blackish, black, False)

        if randomize_button:
            pokemon_display('random')

        dex_entry_button = create_text_button(medium_font, white, "Entry", game_screen.width * .85, 0, (0, 200, 0),
                                              green, False)

        if dex_entry_button:
            pokemon_entry(current_pokemon.dex_no)

        return_button = create_text_button(medium_font, white, "Return", game_screen.width * .85,
                                           game_screen.height * 0.85, (0, 200, 0), green, False)

        if return_button:
            pokemon_search()

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def pokemon_entry(dex_id: int):

    top_bar_height = game_screen.height / 10

    try:
        current_pokemon.dex_entry = \
            get_data(f"https://pokeapi.co/api/v2/pokemon-species/{dex_id}")['flavor_text_entries'][0]['flavor_text']

        current_pokemon.dex_entry = current_pokemon.dex_entry.replace("\n", " ")

    except TypeError:
        print("There was an error, deploying placeholders")

    pkmn_name_text = large_font.render(f"#{current_pokemon.dex_no}. {current_pokemon.name}", True, white)

    screen_background_image_url = urlopen(current_pokemon.image_url).read()
    screen_background_image_file = io.BytesIO(screen_background_image_url)
    screen_background_image = pygame.image.load(screen_background_image_file)

    # Scales the start screen image to the screen size
    poke_photo = pygame.transform.scale(screen_background_image, (game_screen.width / 2.5,
                                                                  game_screen.width / 2.5))

    while True:

        game_screen.screen.fill(slategray)

        game_screen.screen.blit(pkmn_name_text, ((game_screen.width - pkmn_name_text.get_width()) / 2,
                                                 game_screen.height / 30))

        create_onscreen_text(medium_font, black, "Base Stats", game_screen.width * 0.02, game_screen.height * 0.002)
        create_onscreen_text(medium_font, black, "_________", game_screen.width * 0.02, game_screen.height * 0.006)

        stat_height_multiplier = 1.00
        for stat in current_pokemon.stats:
            create_onscreen_text(sml_med_font, black, f"{stat[1]}: {stat[2]}", game_screen.width * 0.025,
                                 game_screen.height * 0.08 * stat_height_multiplier)
            stat_height_multiplier += 1

        game_screen.screen.blit(poke_photo, ((game_screen.width - poke_photo.get_width()) / 2,
                                             top_bar_height * 1.1))

        # Pokédex's entry display code block below
        entry_x = game_screen.width / 3

        start_index = 0
        height_offset = 1
        index_counter = 0
        for index, char in enumerate(current_pokemon.dex_entry):
            index_counter += 1
            if char == " " and index_counter >= 30:
                end_index = index + 1
                create_onscreen_text(sml_med_font, black, current_pokemon.dex_entry[start_index: end_index], entry_x,
                                     game_screen.height * 0.6 * height_offset)
                height_offset += 0.15
                start_index = index
                index_counter = 0
            if index >= len(current_pokemon.dex_entry)-1:
                create_onscreen_text(sml_med_font, black, current_pokemon.dex_entry[start_index: -1],
                                     entry_x, game_screen.height * 0.6 * height_offset)
                break

        resize_button = create_text_button(medium_font, thunderbird_red, "Resize", game_screen.width / 90,
                                           game_screen.height * 0.85, blackish, black, False)

        if resize_button:
            game_screen.resize_screen()

        return_button = create_text_button(medium_font, white, "Return", game_screen.width * .85,
                                           game_screen.height * 0.85, (0, 200, 0), green, False)

        if return_button:
            pokemon_search()

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def main():
    while True:

        start_screen()

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":

    print(get_data("https://pokeapi.co/api/v2/pokemon/eevee").keys())
    print(get_data("https://pokeapi.co/api/v2/pokemon-species/21")['flavor_text_entries'][0]['flavor_text'])
    print(get_data("https://pokeapi.co/api/v2/pokemon-species/21")['flavor_text_entries'][0])
    # print(get_data("https://pokeapi.co/api/v2/pokemon/eevee")["stats"])
    # print(get_data("https://pokeapi.co/api/v2/pokemon/eevee")["stats"][0]['base_stat'])
    # print(get_data("https://pokeapi.co/api/v2/pokemon/eevee")["stats"][0]['stat']['name'])
    # print(get_data("https://pokeapi.co/api/v2/pokemon/seedot")["types"][1]["type"]["name"])

    # pokemon_list_object2 = get_data("https://pokeapi.co/api/v2/pokemon")
    # print(pokemon_list_object2["next"])

    main()
