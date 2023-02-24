# Pygame Project 3.0

## Introduction

This project is my return to Pygame a little over a year after my first attempts at it in fall 2021. I decided to try 
something a bit more ambitious now that I know a lot more about programming, and have the tools necessary to create 
some cooler stuff without being railroaded by tutorials. This is the result, so far. 

## The pokeAPI Pokedex (aka pokedex_2.0.py)

This is a rebuild / improved sequel to my first Pokedex and the main file of this project. 

The 1.0 (which is still included in this project, was more of a structural prototype. I didn't really care about having 
all the data, I just wanted to create a demo pokedex with a handful of Pokemon. But soon after I reached my goals with
that original, I got the urge to expand it so that's what I did. 

I didn't know for sure, but I strongly suspected that there would be a good Pokemon-themed API and there was. This 
project is powered by pokeAPI, so all credits to them. If they ever go offline, this program (at least as it is
designed today) does as well. With it, I have created a Pokedex that can access the data of every existing Pokemon
and display each species' data in dynamic pages, complete with its name, image, base stats, typing and dex entry.

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

This program functions more-or-less like Pokedex from the Pokemon games and anime. 

It has a start screen acting as a faux Pokedex cover that then navigates to a menu that acts as an intermediary 
that can take you both to the real Pokedex search pages and the options

In the Pokemon search pages, you get a list of Pokemon by their number. Currently it's not their actual Pokedex number,
but the sequence in which I added them into the program. Each name is also a button that can be clicked to take you
to that Pokemon's species data page. 

To the right of the page is a search bar that uses regular expressions to filter down the pool of names. Also on the
right of the page is a button to return to the navigation menu and another to cycle through pages of Pokemon, as each
"page" only displays 8 species in order to space things out nicely. 

The Pokemon species' data pages are dynamic and include their species' name, an image, and their typing. Additionally,
for certain species' who have alternative forms (mega evolutions, gigantamax, etc), there is a gallery button that 
cycles through each one. 

The program has a musical backdrop consisting of a handful of lighthearted tracks from the games. Which song plays 
to begin with is random, but can be cycled through in the options menu. The options menu also offers the ability to
change the music's volume or pause it entirely.

Finally, I have included a spooky easter egg. Shouldn't be too hard to find.

### Documentation

FUNCTION create_text_button

x_adjusted: Takes a boolean value. If True, it will adjust the X position of the button given to take into account
the size (width) of the button. For example, if one were to give it an X value of screen_width/2, with the adjustment
the button will end up perfectly centered on the screen. 

### Pokedex 1.0 Todo List / Current Issues / Goals

Feature: I want to be able to filter the dex list based on pokemon type.

Feature: I would like to add relational data. Like bridges to pre-evolutions and successive forms. Also bridges to 
regional variants.

Feature: Create an options object class to handle all option variables so that globals need not be used.

Feature: Try to remove as many absolute measurements as possible. It would be cool to have the program be able to scale
to different screen sizes eventually.

Bug: Better align name text in the pokedex search page. The longer the name, the more unaligned proportions become.
On a related note, to partially fix the problem, I would like to remove the regional variant declaration in Pokemon's
names and move them to a variable or something that I can add in as text next to the button. 

Bug: I would like to reset the lists before text filters so that the pages don't disappear if you start filtering on
page 2, 3, so on. Just looks weird and requires a button press to get back on track.

### pokeAPI todos

Find a way to allow the user to filter through the list of Pokemon

Makeover the UI to be less horribly ugly

Finding a comprehensive way to get the correct flavour text for each pokemon to display for their entry 
(aka english and with only supported characters)

since API doesn't change very often, probably should just grab the Pokemon list data instead of making more and more
call to it. Maybe even save searches to a file that can be re-accessed without the internet later

Watch out for and fix any potential index errors arising from the Pokemon API list

add pokedex cover page

