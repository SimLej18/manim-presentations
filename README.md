# ManimPresentations

The goal of this repository is to explore ways to make ManimSlides more modular and reduce the time
required to create presentations.

## Main objectives:
* have a clear hierarchy: presentations -> chapters -> scenes
* have shared elements between slides (slide number, presentation title, author, year, event, current chapter, etc.)
* being able to compose Presentations using various chapters and slides
* being able to render and launch the whole presentation with the usual `manim-slides render example.py MyPresentation` 
and `manim-slides MyPresentation` commands

## Components:

### Presentation

A presentation is the actual, complete presentation that you want to create. It is composed of chapters and scenes, but
extends the `manim_slides.Slide` class to be able to render the whole presentation at once.

It has properties like the title, author, year, event it is made for, and a list of chapters.

### Chapter

A chapter is a portion of a presentation that can be composed of multiple scenes. It receives the presentation instance
to access its properties and render mobjects. 