import math
import random
import re
import pygame
from pygame import mixer
import sys
import requests
import io
from urllib.request import urlopen
import music_settings

pygame.init()

pygame.display.set_caption("Benndot's Python Pokedex")
window_icon = pygame.image.load("pokePics/pokeball2.png")
pygame.display.set_icon(window_icon)

clock = pygame.time.Clock()

# ---------------------------------------------------------------------------------------------------------------------=
# Gameplay objects

mixer.init()
music_object = music_settings.MusicSettings()
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


# ---------------------------------------------------------------------------------------------------------------------=
# Utility functions and global variables


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


def create_master_list():

    master_list = []

    api_list_size = get_data(f"https://pokeapi.co/api/v2/pokemon?offset=1280&limit="
                             f"{pokedex.d_limit}")["count"]

    api_pokemon_list = get_data(f"https://pokeapi.co/api/v2/pokemon?offset=0&limit={api_list_size}")["results"]

    for index, entry in enumerate(api_pokemon_list, 1):
        entry["dex"] = index
        master_list.append(entry)

    return master_list


pokeAPI_master_list = create_master_list()


def create_onscreen_text(font_size, color, message, x, y, x_adjust: bool = False):

    text = font_size.render(message, True, color)

    if x_adjust:
        text_width = text.get_width()
        x = x - (text_width / 2)

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


# ---------------------------------------------------------------------------------------------------------------------=
# Gameplay functions


def start_screen():

    top_bar_height = 70

    title_photo = pygame.image.load("pokePics/pokedex-spooky.jpg")

    # Scales the start screen image to the screen size
    start_photo = pygame.transform.scale(title_photo, (game_screen.width, game_screen.height - top_bar_height))

    while True:
        game_screen.screen.fill((0, 0, 200))

        create_onscreen_text(medium_font, white, "The Pygame Pokedex", game_screen.width / 2,
                             game_screen.height * 0.015, True)

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

    while True:
        game_screen.screen.fill(thistle_green)

        create_onscreen_text(large_font, blackish, "Music Options", game_screen.width / 2, 0, True)

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
        game_screen.screen.blit(current_track_text, (game_screen.width / 2.9, game_screen.height / 1.6))

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

    offset_choice_label = medium_font.render("Skip to dex number", True, white)
    offset_choice = ""  # Empty string that will take the user's input
    index_search_active: bool = False

    text_search_label = medium_font.render("Search by name", True, white)
    text_search_string = ""  # Empty string that will take the user's input
    text_search_active: bool = False

    while True:

        game_screen.screen.fill(thistle_green)

        create_onscreen_text(large_font, black, "Pokedex Search", game_screen.width / 2, 0, True)

        # Establishing the user inputs for text and indexes and the border boxes that will surround them

        index_search_surface = medium_font.render(offset_choice, True, black)
        text_search_surface = medium_font.render(text_search_string, True, black)

        index_search_x = (game_screen.width - index_search_surface.get_width()) * 0.95
        index_search_y = game_screen.height * .33
        text_search_x = (game_screen.width - text_search_surface.get_width()) * 0.95
        text_search_y = game_screen.height * .60

        game_screen.screen.blit(index_search_surface, (index_search_x, index_search_y))
        game_screen.screen.blit(text_search_surface, (text_search_x, text_search_y))

        game_screen.screen.blit(offset_choice_label, (game_screen.width * 0.7, index_search_y * 0.8))
        game_screen.screen.blit(text_search_label, (game_screen.width * 0.7, text_search_y * 0.9))

        index_search_border = pygame.Rect(index_search_x - (game_screen.height / 72), index_search_y,
                                          index_search_surface.get_width() + (game_screen.height / 72), 50)
        text_search_border = pygame.Rect(text_search_x - (game_screen.height / 72), text_search_y,
                                         text_search_surface.get_width() + (game_screen.height / 72), 50)

        master_list_matches: list = []  # Will contain all regex matches

        search_pattern = re.compile(text_search_string, re.IGNORECASE)
        for poke in pokeAPI_master_list:
            search_bool = search_pattern.search(poke["name"])
            if search_bool:
                master_list_matches.append(poke)

        pokemon_name_height = game_screen.height * 0.13
        height_multi_factor = 1
        pokedex.d_count = 0

        for poke in master_list_matches[pokedex.o_count:]:

            create_onscreen_text(sml_med_font, black, f"#{poke['dex']}", game_screen.width / 4.7,
                                 pokemon_name_height * height_multi_factor)
            poke_button = create_text_button(sml_med_font, white, f"{poke['name']}", game_screen.width / 3.5,
                                             pokemon_name_height * height_multi_factor, blackish, black, False)
            if poke_button:
                pokemon_display(poke['url'])

            pokedex.d_count += 1
            height_multi_factor += 0.72

            if pokedex.d_count >= pokedex.d_limit:
                break

        back_button = create_text_button(medium_font, white, "Back", game_screen.width / 90,
                                         game_screen.height * 0.78, (0, 200, 0), green, False)

        if back_button:
            pokedex.o_count -= 9
            if pokedex.o_count < 0:
                pokedex.o_count = 0

        next_button = create_text_button(medium_font, white, "Next", game_screen.width * .82,
                                         game_screen.height * 0.78, (0, 200, 0), green, False)

        if next_button:
            pokedex.o_count += 9

        music_toggle = create_text_button(sml_med_font, thunderbird_red, "Toggle Music", game_screen.width * .82,
                                          game_screen.height * 0.90, blackish, black, False)

        if music_toggle:
            music_object.music_toggle()

        resize_button = create_text_button(sml_med_font, thunderbird_red, "Resize", game_screen.width / 90,
                                           game_screen.height * 0.90, blackish, black, False)

        if resize_button:
            game_screen.resize_screen()

        randomize_button = create_text_button(sml_med_font, thunderbird_red, "Randomize", game_screen.width / 90,
                                              game_screen.height * 0, blackish, black, False)

        if randomize_button:
            pokemon_display('random')

        options_button = create_text_button(medium_font, white, "Options Menu", game_screen.width * .775, 0,
                                            (0, 200, 0), green, False)

        if options_button:
            options_menu()

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evnt.type == pygame.MOUSEBUTTONDOWN:
                if index_search_border.collidepoint(evnt.pos):
                    index_search_active = not index_search_active
                    if index_search_active and text_search_active:
                        text_search_active = not text_search_active
                if text_search_border.collidepoint(evnt.pos):
                    text_search_active = not text_search_active
                    if text_search_active and index_search_active:
                        index_search_active = not index_search_active
                        offset_choice = ""
                        pokedex.o_count = 0

            if evnt.type == pygame.KEYDOWN:

                if index_search_active:
                    if evnt.key == pygame.K_BACKSPACE:
                        offset_choice = offset_choice[:-1]
                        offset_num = int(offset_choice) if len(offset_choice) >= 1 else 0
                        pokedex.o_count = offset_num - 1 if offset_num - 1 >= 0 else 0
                    else:
                        numbers = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                                   pygame.K_7, pygame.K_8, pygame.K_9]
                        if len(offset_choice) >= 4:
                            pass
                        elif evnt.key in numbers:
                            offset_choice += evnt.unicode
                            offset_num = int(offset_choice)
                            pokedex.o_count = offset_num - 1 if offset_num - 1 >= 0 else 0

                if text_search_active:
                    if evnt.key == pygame.K_BACKSPACE:
                        text_search_string = text_search_string[:-1]
                    else:
                        if len(text_search_string) >= 15:
                            pass
                        else:
                            text_search_string += evnt.unicode

        # Rendering the search bars to the screens

        if index_search_active:
            pygame.draw.rect(game_screen.screen, white, index_search_border, 2)
        else:
            pygame.draw.rect(game_screen.screen, slategray, index_search_border, 2)

        if text_search_active:
            pygame.draw.rect(game_screen.screen, white, text_search_border, 2)
        else:
            pygame.draw.rect(game_screen.screen, slategray, text_search_border, 2)

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
        try:
            current_pokemon.type2 = pokemon_obj["types"][1]["type"]["name"].title()
        except IndexError:
            pass

    except TypeError:
        print("There was an error, deploying placeholders")

    pkmn_type1_text = intermediate_font.render(f"Type 1:    {current_pokemon.type1}", True, white)
    pkmn_type2_text = intermediate_font.render(f"Type 2:    {current_pokemon.type2}", True, white)

    screen_background_image_url = urlopen(current_pokemon.image_url).read()
    screen_background_image_file = io.BytesIO(screen_background_image_url)
    screen_background_image = pygame.image.load(screen_background_image_file)

    # Scales the start screen image to the screen size
    poke_photo = pygame.transform.scale(screen_background_image, (game_screen.width / 2.5,
                                                                  game_screen.width / 2.5))

    while True:

        game_screen.screen.fill(slategray)

        create_onscreen_text(large_font, white, f"#{current_pokemon.dex_no}. {current_pokemon.name}",
                             game_screen.width / 2, game_screen.height / 30, True)

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

    text_search_url = f"https://pokeapi.co/api/v2/pokemon-species/{dex_id}"

    try:
        flavor_text_obj_list = get_data(text_search_url)['flavor_text_entries']

        for flavor_obj in flavor_text_obj_list:
            if flavor_obj["language"]["name"] == "en":
                current_pokemon.dex_entry = flavor_obj["flavor_text"]
                break

        current_pokemon.dex_entry = current_pokemon.dex_entry.replace("\n", " ").replace("\x0c", " ")
        print(current_pokemon.dex_entry)
        print(len(current_pokemon.dex_entry))

    except TypeError:
        print("There was an error, deploying placeholders")

    pokemon_image_url = urlopen(current_pokemon.image_url).read()
    pokemon_image_file = io.BytesIO(pokemon_image_url)
    pokemon_image = pygame.image.load(pokemon_image_file)

    while True:

        game_screen.screen.fill(slategray)

        create_onscreen_text(large_font, white, f"#{current_pokemon.dex_no}. {current_pokemon.name}",
                             game_screen.width / 2, game_screen.height / 30, True)

        create_onscreen_text(medium_font, black, "Base Stats", game_screen.width * 0.02, game_screen.height * 0.002)
        create_onscreen_text(medium_font, black, "_________", game_screen.width * 0.02, game_screen.height * 0.006)

        stat_height_multiplier = 1.00
        for stat in current_pokemon.stats:
            create_onscreen_text(sml_med_font, black, f"{stat[1]}: {stat[2]}", game_screen.width * 0.025,
                                 game_screen.height * 0.08 * stat_height_multiplier)
            stat_height_multiplier += 1

        # Defining and blitting the Pokemon's image to the screen
        scaled_poke_photo = pygame.transform.scale(pokemon_image, (game_screen.width / 2.8, game_screen.width / 2.8))
        game_screen.screen.blit(scaled_poke_photo, ((game_screen.width - scaled_poke_photo.get_width()) / 2,
                                                    game_screen.height / 10 * 1.1))

        # Drawing the Pokédex entry box

        base_height = game_screen.height * 0.65 if len(current_pokemon.dex_entry) <= 150 else game_screen.height * 0.60

        box_height = game_screen.height * 0.25 if len(current_pokemon.dex_entry) < 120 else game_screen.height * 0.32 \
            if 120 <= len(current_pokemon.dex_entry) <= 150 else game_screen.height * 0.38
        entry_rect = pygame.Rect(game_screen.width * 0.25, base_height * 0.98,
                                 game_screen.width * 0.5, box_height)
        pygame.draw.rect(game_screen.screen, black, entry_rect, 2)

        # Pokédex's entry display code block below
        entry_start_x = game_screen.width / 3.5

        line_start_index = 0  # Will change with each new line
        height_offset = 1
        index_counter = 0
        for index, char in enumerate(current_pokemon.dex_entry):
            index_counter += 1
            if char == " " and index_counter >= 35:
                end_index = index + 1
                create_onscreen_text(sml_med_font, black,
                                     current_pokemon.dex_entry[line_start_index+1 if line_start_index != 0 else
                                                               line_start_index: end_index],
                                     entry_start_x,  base_height * height_offset)
                height_offset += 0.12
                line_start_index = index
                index_counter = 0
            if index >= len(current_pokemon.dex_entry)-1:
                create_onscreen_text(sml_med_font, black, current_pokemon.dex_entry[line_start_index+1: -1] + ".",
                                     entry_start_x, base_height * height_offset)
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

    main()
