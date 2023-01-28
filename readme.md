# Pygame Project 2.0

This is my return to Pygame a little over a year after the first time that I tried it. I have a more robust coding 
knowledge now to help me figure out some things that I struggled with back in fall 2021. 

## The Pokedex 1.2

The focus on this project so far has centered around creating a "pokedex" out of the pygame window. Dynamically 
generating lists of Pokemon species and then displaying pages of their information and likeness when the names are
selected.

This is 1.2.0-ish version of this program, with a bunch of small tweaks including:
    -Better placement of buttons, visual elements, use of colors
    -No longer resets to start with every return button (aka better navigation between screens)
    -Incorporation of music and controls for the music (Muting, Pausing, Track Changes)
    -A gallery button in the species display to show alternate forms of Pokemon (assuming they have at least one)
    -Conditional text that labels what those alternate forms are
    -An easter egg (:0)
    -Improved language in the code itself for improved readability

#### Features

Text searches on Pokemon names to filter lists. 

Dynamic pages for each Pokemon including name, an image, and their typing. 

Backing music, with options to switch tracks, pause, and change the volume level. 

A spooky easter egg.

### Todo List / Current Issues / Goals

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

Bug: Fix the issue of clicking "through" screens? Pressing a button on one screen and accidentally activating a button
in the same general area on the next screen. Not sure how I would fix that yet. Probably would have to change the 
mouse-clicking system. 

