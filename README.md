# Discount Slide Deck Maker
Just a short project a did in a few hours for a demonstration, it's just a discount version of more powerful slide deck creators such as Powerpoint or Google Slides, but can be used on the commandline with text input for the slides.
As a disclaimer, this is not intended to be a serious project. Please do not use this for making slides, there's many oddities and unnecessary restrictions as this was for demo purposes.

# How to use
Create an input.txt file. In it, follow the following rules:

There are two types of slides, normal and title slides. Title slides will have up to lines of text in the middle of the screen, and can include a single picture above it a link is included as markdown. You denote them with %title at the top of a section. Normal slides are denoted with %normal at the top of a section.
Sections are bodys of text that make up a slide. Title slides must have at least two lines of text for example, with the rest being thrown out (unless it contains a link to an image to include on the slide). If you want to include an empty line, leave the line empty with only two spaces "  " in the line itself, or else there will be issues when parsing.
Normal slides can have as much text as you want, although there's no autofit function for the text at the moment. If you include an image, it will be at the right on the slide.

Run main.py and it will automatically compile your slides into gen.html, though the input and output files can be specified with the commandline arguments --input/-i and --output/-o respectively. Open gen.html in a webbrowser, and use left click to advance the slide number, and right click to retreat the slide number.
