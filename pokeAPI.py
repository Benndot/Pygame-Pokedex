import random
import pygame
import sys
import requests
import io
from urllib.request import urlopen

pygame.init()

clock = pygame.time.Clock()

# you can access PokeAPI both by the Pokemon species' name and by their national Pokédex number


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

        for evnt in pygame.event.get():
            if evnt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)


def main():
    while True:

        pokemon_display()

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

    main()
