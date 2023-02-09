import pygame
from pygame import mixer
import sys
import re
import random
from datetime import date

# TODO: Add more detail to display pages, type sorting, better transition back to main menu

pygame.init()

clock = pygame.time.Clock()

# Some option page global variables (maybe combine into some kind of options class later)
music_paused = False
volume_level = 50

def music_toggle():
    global music_paused
    print("The music pausing bool has been toggled")
    music_paused = not music_paused
    if music_paused:
        mixer.music.pause()
    elif not music_paused:
        mixer.music.unpause()

# Music section
spooky_song = "audio/Pokemon BlueRed - Lavender Town.mp3"
tracklist = ["audio/Pokemon Ruby- Littleroot Town.mp3", "audio/Pokemon Ruby- Route 101.mp3",
             "audio/Pokemon Ruby- Route 104.mp3"]
tracklist_index = random.randint(0, len(tracklist) - 1)
mixer.init()
mixer.music.load(tracklist[tracklist_index])
mixer.music.set_volume(volume_level/350)
mixer.music.play(-1)


class PokeImages:  # For the expanded photo system
    def __init__(self, form, photo):
        self.form = form
        self.photo = photo


img_castform_base = PokeImages("Base", "pokePics/castform_base.png")
img_castform_sun = PokeImages("Sunny Form", "pokePics/castform_sunny.png")
img_castform_rain = PokeImages("Rainy Form", "pokePics/castform_rain.png")
img_castform_snow = PokeImages("Snowy Form", "pokePics/castform_snowy.png")
castform_gallery = [img_castform_base, img_castform_sun, img_castform_rain, img_castform_snow]

img_beedrill_base = PokeImages("Base", "pokePics/Beedrill.png")
img_beedrill_mega = PokeImages("Mega Evolution", "pokePics/Beedrill-Mega.png")
beedrill_gallery = [img_beedrill_base, img_beedrill_mega]

img_glalie_base = PokeImages("Base", "pokePics/Glalie.png")
img_glalie_mega = PokeImages("Mega Evolution", "pokePics/Glalie-Mega.png")
glalie_gallery = [img_glalie_base, img_glalie_mega]

img_sableye_base = PokeImages("Base", "pokePics/Sableye.png")
img_sableye_mega = PokeImages("Mega Evolution", "pokePics/Sableye-Mega.png")
sableye_gallery = [img_sableye_base, img_sableye_mega]

img_pikachu_base = PokeImages("Base", "pokePics/pikachu.png")
img_pikachu_giant = PokeImages("Gigantamax Form", "pokePics/Pikachu-Gigantamax.png")
pikachu_gallery = [img_pikachu_base, img_pikachu_giant]

img_mewtwo_base = PokeImages("Base", "pokePics/Mewtwo.png")
img_mewtwo_megax = PokeImages("Mega Evolution X", "pokePics/Mewtwo-Mega_X.png")
img_mewtwo_megay = PokeImages("Mega Evolution Y", "pokePics/Mewtwo-Mega_Y.png")
mewtwo_gallery = [img_mewtwo_base, img_mewtwo_megax, img_mewtwo_megay]

img_charizard_base = PokeImages("Base", "pokePics/Charizard.png")
img_charizard_megax = PokeImages("Mega Evolution X", "pokePics/Charizard-Mega_X.png")
img_charizard_megay = PokeImages("Mega Evolution Y", "pokePics/Charizard-Mega_Y.png")
img_charizard_giant = PokeImages("Gigantamax Form", "pokePics/Charizard-Gigantamax.png")
charizard_gallery = [img_charizard_base, img_charizard_megax, img_charizard_megay, img_charizard_giant]


# Creating Pokemon class(es?) and class instances
class PokemonSpecies:
    def __init__(self, species_name, image, typing, alt_forms):
        self.species_name = species_name
        self.image: pygame.image or list[str] = image
        self.typing: list[str, str] = typing
        self.alt: list = alt_forms


charmander = PokemonSpecies("Charmander", pygame.image.load("pokePics/Charmander.png"), ["Fire"], [False])
charmeleon = PokemonSpecies("Charmeleon", pygame.image.load("pokePics/Charmeleon.png"), ["Fire"], [False])
charizard = PokemonSpecies("Charizard", pygame.image.load("pokePics/Charizard.png"), ["Fire", "Flying"],
                           charizard_gallery)

weedle = PokemonSpecies("Weedle", pygame.image.load("pokePics/Weedle.png"), ["Bug", "Poison"], [False])
kakuna = PokemonSpecies("Kakuna", pygame.image.load("pokePics/kakuna.png"), ["Bug", "Poison"], [False])
beedrill = PokemonSpecies("Beedrill", pygame.image.load("pokePics/Beedrill.png"), ["Bug", "Poison"], beedrill_gallery)

geodude = PokemonSpecies("Geodude", pygame.image.load("pokePics/geodude.png"), ["Ground", "Rock"], [False])
graveler = PokemonSpecies("Graveler", pygame.image.load("pokePics/graveler.png"), ["Ground", "Rock"], [False])

cleffa = PokemonSpecies("Cleffa", pygame.image.load("pokePics/Cleffa.png"), ["Fairy"], [False])
clefairy = PokemonSpecies("Clefairy", pygame.image.load("pokePics/Clefairy.png"), ["Fairy"], [False])
clefable = PokemonSpecies("Clefable", pygame.image.load("pokePics/Clefable.png"), ["Fairy"], [False])

farfetchd_kanto = PokemonSpecies("Farfetch'd (Kanto)", pygame.image.load("pokePics/farfetchd.png"),
                                 ["Normal", "Flying"], [True])
farfetchd_galar = PokemonSpecies("Farfetch'd (Galar)", pygame.image.load("pokePics/Farfetch'd-Galar.png"),
                                 ["Fighting"], [True])
sirfetchd = PokemonSpecies("Sirfetch'd", pygame.image.load("pokePics/Sirfetch'd.png"), ["Fighting"], [False])

pikachu = PokemonSpecies("Pikachu", pygame.image.load("pokePics/pikachu.png"), ["Electric"], pikachu_gallery)
raichu = PokemonSpecies("Raichu", pygame.image.load("pokePics/Raichu.png"), ["Electric"], [True])

hoppip = PokemonSpecies("Hoppip", pygame.image.load("pokePics/Hoppip.png"), ["Grass", "Flying"], [False])
skipbloom = PokemonSpecies("Skipbloom", pygame.image.load("pokePics/Skiploom.png"), ["Grass", "Flying"], [False])
jumpluff = PokemonSpecies("Jumpluff", pygame.image.load("pokePics/Jumpluff.png"), ["Grass", "Flying"], [False])

sableye = PokemonSpecies("Sableye", pygame.image.load("pokePics/Sableye.png"), ["Dark", "Ghost"], sableye_gallery)

snorunt = PokemonSpecies("Snorunt", pygame.image.load("pokePics/Snorunt.png"), ["Ice"], [False])
glalie = PokemonSpecies("Glalie", pygame.image.load("pokePics/Glalie.png"), ["Ice"], glalie_gallery)
froslass = PokemonSpecies("Froslass", pygame.image.load("pokePics/Froslass.png"), ["Ice", "Ghost"], [False])

castform = PokemonSpecies("Castform", pygame.image.load("pokePics/castform_base.png"), ["Normal"], castform_gallery)

bidoof = PokemonSpecies("Bidoof", pygame.image.load("pokePics/Bidoof.png"), ["Normal", "Water"], [False])
bibarel = PokemonSpecies("Bibarel", pygame.image.load("pokePics/Bibarel.png"), ["Normal", "Water"], [False])

shieldon = PokemonSpecies("Shieldon", pygame.image.load("pokePics/Shieldon.png"), ["Steel"], [False])
bastiodon = PokemonSpecies("Bastiodon", pygame.image.load("pokePics/Bastiodon.png"), ["Steel"], [False])

mew = PokemonSpecies("Mew", pygame.image.load("pokePics/Mew.png"), ["Psychic"], [False])
mewtwo = PokemonSpecies("Mewtwo", pygame.image.load("pokePics/Mewtwo.png"), ["Psychic"], mewtwo_gallery)

entei = PokemonSpecies("Entei", pygame.image.load("pokePics/Entei.png"), ["Fire"], [False])

pokemon_list = [charmander, charmeleon, charizard, weedle, kakuna, beedrill, geodude, graveler, cleffa, clefairy,
                clefable, farfetchd_kanto, farfetchd_galar, sirfetchd, pikachu, raichu, hoppip, skipbloom, jumpluff,
                sableye, snorunt, glalie, froslass, castform, bidoof, bibarel, shieldon, bastiodon, mew, mewtwo, entei]

# Screen specifications
screen_width = 1070
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Pokedex")

# Setting different sized font options to be used later for general text and button labels
large_font = pygame.font.SysFont("comicsansms", 50)
medium_font = pygame.font.SysFont("comicsansms", 30)
small_font = pygame.font.SysFont("comicsansms", 15)

# Establishing the start screen image
title_photo = pygame.image.load("pokePics/pokedex-spooky.jpg")
menu_photo = pygame.image.load("pokePics/pokeball2.png")

# Establishing a number of reusable rgb values for several colors
slategray = (112, 128, 144)
lightgray = (165, 175, 185)
blackish = (10, 10, 10)
thunderbird_red = (200, 15, 25)
white = (255, 255, 255)
thistle_green = (210, 210, 190)
black = (0, 0, 0)


def create_transparent_button(width, height, x, y):
    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed(3)

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        s = pygame.Surface((width, height))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill((255, 255, 255))  # this fills the entire surface
        screen.blit(s, (x, y))  # (0,0) are the top-left coordinates
        if click[0] == 1:
            return True


def create_text_button_adjusted(font_choice, text_color, msg, x, y, hover_color, default_color):
    # font_choice is a selection from the global variables for the fonts that I set, describing style and size
    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed(3)

    button_msg = font_choice.render(msg, True, text_color)

    button_width = button_msg.get_width() + (button_msg.get_width() * 0.20)
    button_height = button_msg.get_height() + (button_msg.get_height() * 0.20)

    # Experimental
    adjusted_x = x - (button_width / 2)

    # The experimental version
    if adjusted_x + button_width > mouse[0] > adjusted_x and y + button_height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (adjusted_x, y, button_width, button_height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, default_color, (adjusted_x, y, button_width, button_height))

    screen.blit(button_msg, (adjusted_x + button_width / 10, y + button_height / 10))


def create_text_button_absolute(font_choice, text_color, msg, x, y, hover_color, default_color):
    # font_choice is a selection from the global variables for the fonts that I set, describing style and size
    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed(3)

    button_msg = font_choice.render(msg, True, text_color)

    button_width = button_msg.get_width() + (button_msg.get_width() * 0.20)
    button_height = button_msg.get_height() + (button_msg.get_height() * 0.20)

    # The experimental version
    if x + button_width > mouse[0] > x and y + button_height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, button_width, button_height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, default_color, (x, y, button_width, button_height))

    screen.blit(button_msg, (x + button_width / 10, y + button_height / 10))


def create_button(x, y, width, height, hover_color, default_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)

    # Essentially the below means "if the mouse is positioned within the confines of the button on the screen"
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, default_color, (x, y, width, height))


# ----------------------------------------------------------------------------------------------------------------------


def start_screen():
    global music_paused
    global tracklist_index

    start_text = medium_font.render("The Pygame Pokedex", True, white)

    today = date.today()
    today_text = "Today is " + today.strftime("%A") + ", " + today.strftime("%B") + " " + today.strftime("%d") + \
                 ", " + today.strftime("%Y")
    today_text = small_font.render(today_text, True, lightgray)

    top_bar_height = 70

    # Scales the start screen image to the screen size
    start_photo = pygame.transform.scale(title_photo, (screen_width, screen_height - top_bar_height))

    while True:
        screen.fill((0, 0, 200))
        screen.blit(start_text, ((screen_width - start_text.get_width()) / 2, screen_height / 65))
        screen.blit(today_text, (5, 10))

        menu_button = create_text_button_adjusted(small_font, blackish, "Open Menu", screen_width * .9, 12, lightgray,
                                                  slategray)

        if menu_button:
            game_menu()
            return

        music_button = create_text_button_adjusted(small_font, blackish, "Toggle Music", screen_width * .8, 12,
                                                   lightgray, slategray)

        if music_button:
            music_toggle()

        ghost_button = create_transparent_button(250, 100, screen_width / 1.75, screen_height / 2.5)

        if ghost_button:
            print("Ghost button clicked!")
            mixer.music.load(spooky_song)
            mixer.music.set_volume(volume_level / 350)
            mixer.music.play(-1)
            tracklist_index = 13

        screen.blit(start_photo, (0, 70))

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)
        return True


def game_menu():
    title_text = medium_font.render("Main Menu", True, slategray)
    start_text = medium_font.render("Search Pokemon", True, white)
    options_text = medium_font.render("Game Options", True, white)

    menu_photo_scaled = pygame.transform.scale(menu_photo, (300, 300))

    while True:
        screen.fill(black)
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 0))

        screen.blit(menu_photo_scaled, ((screen_width - menu_photo_scaled.get_width()) / 2, screen_height / 4))

        # Start button code
        start_button_width, start_button_height = start_text.get_width() + 50, start_text.get_height() + 20
        start_text_x, start_text_y = (screen_width - start_text.get_width()) / 4, title_text.get_height() + 50
        start_button = create_button(start_text_x - start_text.get_width() / 8, start_text_y, start_button_width,
                                     start_button_height, lightgray, slategray)
        screen.blit(start_text, (start_text_x, start_text_y))

        if start_button:
            pokedex_search()

        # Options button code
        options_button_width, options_button_height = options_text.get_width() + 50, options_text.get_height() + 20
        options_text_x, options_text_y = (screen_width - options_text.get_width()) / 1.25, \
            options_text.get_height() + 50
        options_button = create_button(options_text_x - options_text.get_width() / 8, options_text_y,
                                       options_button_width, options_button_height, lightgray, slategray)
        screen.blit(options_text, (options_text_x, options_text_y))

        if options_button:
            options_menu()

        # Mouse position tracking
        mouse_pos = pygame.mouse.get_pos()

        mouse_position_text = large_font.render(str(mouse_pos), True, white)
        screen.blit(mouse_position_text, ((screen_width - mouse_position_text.get_width()) / 2, 500))

        mouse_sum_text = large_font.render(f"{mouse_pos[0] + mouse_pos[1]}", True, white)
        screen.blit(mouse_sum_text, ((screen_width - mouse_sum_text.get_width()) / 2,
                                     500 + mouse_sum_text.get_height()))

        # Quitting boilerplate code
        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def options_menu():
    global volume_level
    global tracklist_index

    title_text = large_font.render("Options Menu", True, blackish)

    while True:
        screen.fill(thistle_green)
        screen.blit(title_text, ((screen_width - title_text.get_width()) / 2, 0))

        music_button = create_text_button_adjusted(medium_font, white, "Toggle Music", screen_width / 1.97,
                                                   screen_height / 6.5, lightgray, slategray)
        if music_button:
            music_toggle()

        # Bool declaration
        music_pause_declaration = "Yes" if music_paused else "No"
        music_paused_text = medium_font.render(f"Music Paused: " + music_pause_declaration, True, blackish)
        bool_text_x = (screen_width - music_paused_text.get_width()) / 2
        bool_text_y = (screen_height - music_paused_text.get_height()) / 3.8
        screen.blit(music_paused_text, (bool_text_x, bool_text_y))

        # Return to start menu button
        return_button = create_text_button_adjusted(medium_font, white, "Return To Start", screen_width / 2,
                                                    screen_height / 1.25, slategray, lightgray)

        if return_button:
            main()

        # Creating the (purely aesthetic) volume setting, including 2 buttons and the volume level display
        volume_height = screen_height / 2.8
        volume_text = medium_font.render(f"{volume_level}", True, black)
        volume_text_x = (screen_width / 2) - (volume_text.get_width() / 2) + 5
        screen.blit(volume_text, (volume_text_x, volume_height - 10))

        volume_up_button = create_text_button_adjusted(small_font, white, "Volume +", screen_width / 2.25,
                                                       volume_height, slategray, lightgray)

        volume_down_button = create_text_button_adjusted(small_font, white, "Volume -", screen_width / 1.75,
                                                         volume_height, slategray, lightgray)

        if volume_up_button:
            print("volume increased!")
            volume_level += 10
            if volume_level > 100:
                volume_level = 100
            mixer.music.set_volume(volume_level/350)
        if volume_down_button:
            print("volume decreased!")
            volume_level -= 10
            if volume_level < 0:
                volume_level = 0
            mixer.music.set_volume(volume_level/350)

        if volume_level == 0:
            muted_text = medium_font.render("(muted)", True, thunderbird_red)
            screen.blit(muted_text, (volume_text_x * .92, volume_height + 25))

        music_changer = create_text_button_adjusted(large_font, white, "Change Music Track", screen_width / 2,
                                                    screen_height / 2.2, slategray, lightgray)

        if music_changer:
            print("Track change initiated")
            mixer.music.stop()
            tracklist_index += 1
            if tracklist_index >= len(tracklist):
                tracklist_index = 0
            mixer.music.load(tracklist[tracklist_index])
            mixer.music.set_volume(volume_level/350)
            mixer.music.play(-1)

        current_track_name = tracklist[tracklist_index][6:-4] if tracklist_index != 13 else "    ????????????????????"
        current_track_text = small_font.render(f'Current Track: ' + current_track_name, True, blackish)
        screen.blit(current_track_text, (screen_width / 2.8, screen_height / 1.6))

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def pokedex_search():
    start_text = medium_font.render("Pokedex: List View", True, slategray)

    poke_index_tracker = 0

    search_box_label = medium_font.render("Text Search", True, white)

    search_string = ""  # Empty string that will take the user's input

    search_active: bool = False  # NOT IMPLEMENTED. To make it so that the search rect must be active to input text

    while True:
        screen.fill(lightgray)
        screen.blit(start_text, ((screen_width - start_text.get_width()) / 2, 0))

        # Establishing the user input text and the border box that will surround it
        search_surface = medium_font.render(search_string, True, white)
        search_x = (screen_width - search_surface.get_width()) * 0.95
        search_y = screen_height * .33
        screen.blit(search_box_label, (screen_width * 0.8, search_y - 60))
        search_border = pygame.Rect(search_x - 10, search_y, search_surface.get_width() + 10, 50)
        screen.blit(search_surface, (search_x, search_y))

        # Creating a regular expression filter based around the search inputs
        search_matches: list[PokemonSpecies] = []  # Will contain all regex matches

        search_pattern = re.compile(search_string, re.IGNORECASE)
        for poke in pokemon_list:
            search_bool = search_pattern.search(poke.species_name)
            if search_bool:
                search_matches.append(poke)

        # Button to cycle through Pokédex pages
        cycle_button = create_text_button_adjusted(medium_font, white, "Next Page", screen_width - 150, 600, slategray,
                                                   lightgray)

        if cycle_button:
            poke_index_tracker += 8
            if poke_index_tracker >= len(search_matches):
                poke_index_tracker = 0

        # Return to start menu button
        return_button = create_text_button_adjusted(medium_font, white, "Return To Menu", screen_width - 150, 10,
                                                    slategray, lightgray)

        if return_button:
            return_to_screen(game_menu)

        species_name_height = 85
        for index, poke in enumerate(search_matches[poke_index_tracker:], poke_index_tracker+1):
            if species_name_height <= 680:
                poke_button = create_text_button_absolute(medium_font, white, f"{index}. {poke.species_name}", 75,
                                                          species_name_height, slategray, slategray)
                species_name_height += 75

                if poke_button:
                    species_display(poke)

        # Pygame event handling section

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evnt.type == pygame.MOUSEBUTTONDOWN:
                if search_border.collidepoint(evnt.pos):
                    search_active = not search_active

            if evnt.type == pygame.KEYDOWN:
                if search_active:
                    if evnt.key == pygame.K_BACKSPACE:
                        search_string = search_string[:-1]
                    else:
                        if len(search_string) > 12:
                            pass
                        else:
                            search_string += evnt.unicode

        if search_active:
            pygame.draw.rect(screen, white, search_border, 2)
        else:
            pygame.draw.rect(screen, slategray, search_border, 2)

        pygame.display.update()
        clock.tick(15)


def species_display(active_pokemon: PokemonSpecies):

    pokemon_name = active_pokemon.species_name
    pokemon_name_title = large_font.render(pokemon_name, True, white)
    pokemon_image = active_pokemon.image
    pokemon_image = pygame.transform.scale(pokemon_image, (400, 400))
    pokemon_typing = active_pokemon.typing

    gallery_index = 0  # Keeps track of the index of the gallery, if any exists

    type_primary = pokemon_typing[0]
    type_primary_text = medium_font.render(f"Type 1: {type_primary}", True, white)
    type_secondary = pokemon_typing[1] if len(pokemon_typing) > 1 else "N/A"
    type_secondary_text = medium_font.render(f"Type 2: {type_secondary}", True, white)

    while True:

        screen.fill(black)

        screen.blit(pokemon_name_title, ((screen_width - pokemon_name_title.get_width()) / 2, screen_height / 20))

        screen.blit(pokemon_image, ((screen_width - 400) / 2, (screen_height - 400) / 2))

        return_button = create_text_button_adjusted(medium_font, white, "Return To Menu", screen_width * 0.85,
                                                    screen_height * 0.02, slategray, lightgray)

        screen.blit(type_primary_text, (screen_width / 3.2, 625))
        screen.blit(type_secondary_text, (screen_width / 1.8, 625))

        if return_button:
            return_to_screen(pokedex_search)  # Clicking activates a second button through screen

        gallery_button = create_text_button_adjusted(medium_font, white, "Gallery", screen_width * 0.08,
                                                    screen_height * 0.02, slategray, lightgray)

        if gallery_button and len(active_pokemon.alt) > 1:
            gallery_index += 1
            if gallery_index >= len(active_pokemon.alt):
                gallery_index = 0
            pokemon_image = pygame.image.load(active_pokemon.alt[gallery_index].photo)
            pokemon_image = pygame.transform.scale(pokemon_image, (400, 400))

        if len(active_pokemon.alt) > 1:
            alt_form_text = medium_font.render(active_pokemon.alt[gallery_index].form, True, white)
            if active_pokemon.alt[gallery_index].form != "Base":
                screen.blit(alt_form_text, ((screen_width - alt_form_text.get_width()) / 2, screen_height / 7.5))

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def haunting():

    while True:

        screen.fill(black)

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def return_to_screen(desired_screen):
    while True:

        desired_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def main():
    while True:

        start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


if __name__ == "__main__":

    main()
