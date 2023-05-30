# Pygame Project 3.0

## Introduction

This project is my return to Pygame a little over a year after my first attempts at it in fall 2021. I decided to try 
something a bit more ambitious now that I know a lot more about programming, and have the tools necessary to create 
some cooler stuff without being railroaded by tutorials. This is the result, so far. 

The First version of this project (1.2.1), which is still included in this project, was more of a structural prototype.
I wanted to create the interface, and didn't really care about having more than a few species to show off. 
However, soon after I reached my goals with it, I got the urge to expand on it. 

## The pokeAPI Pokedex (aka pokedex_2.0.py)

This project is powered by pokeAPI, so all credits to them. If they ever go offline, this program (at least as it is
designed today) does as well. With it, I have created a Pokedex that can access the data of every existing Pokemon
and display each species' data in dynamic pages, complete with its name, image, base stats, typing and dex entry.

The interface and structure of the program is very similar to the 1.0 version. There's a relatively simple title page
that allows the user to toggle the music on and off and enter the pokedex proper. 

The search menu is where the real content is. From there, the user will be greeted with a list of Pokemon species
buttons running down the center of the screen. It will be begin at national dex number 1, but pages can be cycled 
through to eventually reach any Pokemon. To speed up a search, an input for a specific dex number and an input to filter
results based on the species name are offered on the screen's right. At the top right, the user can choose to press the
"randomize" button to land on the page of a randomly selected Pokemon.

When a pokemon's button is clicked (or the user chose randomized), they are brought to the species' data page. There, 
an image of the pokemon is generated, along with a header containing its name and number. Its typing will be displayed
towards the bottom and its base stats are displayed to the left. Pressing the entry button on the right, will display
a sub-page that will display the Pokemon's "flavour text" (aka a short blurb describing the species behaviour, 
appearance, lore, etc).

The program has a musical backdrop consisting of a handful of lighthearted tracks from the games that fit the vibe of a
laidback digital encyclopedia. Which song plays to begin with is random, but all songs can be cycled through in the 
options menu. The options menu also offers the ability to change the music's volume or pause it entirely.

The resize button throughout the app allows the user to cycle through 3 different sizes of display for the window. Not
everything has been perfectly scaled in the code, but it generally works well. 

This program has an "eerie" easter egg that shouldn't be too hard to find. 

## The Pokedex 1.2.1 

The focus on this project so far has centered around creating a "pokedex" out of the pygame window. Dynamically 
generating lists of Pokemon species and then displaying pages of their information and likeness when the names are
selected.

This is 1.2.0-ish version of this program, with a bunch of small tweaks including:
    -Better placement of buttons, visual elements, use of colors
    -No longer resets to start with every return button (aka better navigation between screens)
    -Incorporation of music and controls for the music (Muting, Pausing, Track Changes)
    -A gallery button in the species display to show alternate forms of Pokemon (assuming they have at least one)
    -Conditional text that labels what those alternate forms are
    -An easter egg 
    -Improved language in the code itself for improved readability

Version 1.2.1 adds the following:
    -Switches from a "BUTTONMOUSEUP" button clicking system to "BUTTONMOUSEDOWN" in order to finally fix the 
    "clicking through screens" glitch that was plaguing this project. 
    -Some cleaned up code, deletion of an old, now unneeded button function
    -Slightly improved UI, including a re-arranged options menu and slightly larger "small font" text

#### Features (Pokedex 1.0)

This program is largely similar in function and appearance to the 2.0 version, but the pokemon data it uses is hard 
coded and more limited.

In the Pokemon search pages, you get a list of Pokemon by their number. Currently it's not their actual Pokedex number,
but the sequence in which I added them into the program. Each name is also a button that can be clicked to take you
to that Pokemon's species data page. 

To the right of the page is a search bar that uses regular expressions to filter down the pool of names. Also on the
right of the page is a button to return to the navigation menu and another to cycle through pages of Pokemon, as each
"page" only displays 8 species in order to space things out nicely. 

The Pokemon species' data pages are dynamic and include their species' name, an image, and their typing. Additionally,
for certain species' who have alternative forms (mega evolutions, gigantamax, etc), there is a gallery button that 
cycles through each one.

### Documentation

FUNCTION create_text_button

x_adjusted: Takes a boolean value. If True, it will adjust the X position of the button given to take into account
the size (width) of the button. For example, if one were to give it an X value of screen_width/2, with the adjustment
the button will end up perfectly centered on the screen.

### pokedex 2.0 todos

Make Pokemon entry box width dynamic based on maximum line length

Save pokemon master list to a file (shelve) that updates itself every once in a while based on datetime

Polish UI