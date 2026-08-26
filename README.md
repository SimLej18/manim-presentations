# ManimPresentations

A small layer on top of [manim-slides](https://github.com/jeertmans/manim-slides) for building
presentations out of reusable pieces, and for rendering any one of those pieces on its own —
with the real overlay, the real slide number, in the real position it has in the deck.

## Main objectives

* a clear hierarchy: deck → chapters → slides
* shared elements across slides (slide number, chapter progress, title, author, event, year)
* compose decks out of chapters and slides that can be reused elsewhere
* render and present the deck without naming its scenes
* render any single chapter or single slide, and see exactly what the full deck will show

## State of the project

This is a _personal project_ that I started to make my life easier when creating presentations
with Manim. It may be useful to others, but do not consider it a complete, elegant or polished
solution. If you have suggestions, ideas or feedback, feel free to open a discussion.

## Installation

```bash
pip install manim-presentations
```

Or, from a clone:

```bash
pip install -e .
```

## A deck in one file

```python
from manim import *
from manim_presentations import Deck, Chapter, SlideUnit


class Bullets(SlideUnit):
	def __init__(self, headline, *lines, notes=""):
		self.headline = headline
		self.lines = lines
		self.notes = notes

	def construct(self):
		previous = Text(self.headline, font_size=48)
		self.play(Write(previous), run_time=0.25)
		for line in self.lines:
			self.next_slide()
			following = Text(line, font_size=36).next_to(previous, DOWN, buff=0.5)
			self.play(Write(following), run_time=0.25)
			previous = following


deck = Deck(
	title="My Presentation",
	subtitle="Subtitle",
	first_author="Author",
	event="My Event",
	year="2025",
	chapters=[
		Chapter("Intro", "Chapter 1: Where it all begins", "Chapter 1", units=[
			Bullets("First slide", "It even has a second line!", notes="Say hello."),
			Bullets("Second slide"),
		]),
	],
)

deck.register(globals())
```

```bash
manim-presentations render deck.py -ql     # render everything
manim-presentations present deck.py        # play it
```

The command lives in the environment you installed into, so activate it first
(`source .venv/bin/activate`), or use `uv run manim-presentations ...`. If your shell still
reports an unknown command right after installing, it has cached its `PATH` — run `rehash`
or open a new shell. `python -m manim_presentations ...` works either way and takes the same
arguments.

## Commands

`manim-presentations` reads the `Deck` in your file and hands its scenes to manim-slides in the
right order, so you never type scene names. Any option it does not recognise is forwarded to
manim-slides, so `-ql`, `--full-screen` and the rest still work.

```bash
manim-presentations render deck.py -ql
manim-presentations render deck.py --only Intro -ql        # one chapter
manim-presentations render deck.py --only Intro_S2 -ql     # one slide
manim-presentations present deck.py
manim-presentations convert deck.py slides.html
manim-presentations list deck.py                           # scene names, in order
```

The generated scenes are ordinary Manim scenes, so the manim-slides commands work directly too:

```bash
manim-slides render deck.py Intro -ql
manim-slides present Title Intro End
```

## Components

### SlideUnit

One unit of content, and the thing the slide number counts. It is **not** a Scene: inside
`construct`, `self` forwards to the Scene currently rendering the unit, so `self.play`,
`self.add`, `self.wait`, `self.next_slide` and `self.camera` behave as usual.

Units are ordinary objects, so they take constructor arguments and can be reused:

```python
Bullets("Results"), Bullets("Method", "Two steps", notes="...")
```

* `notes` — presenter notes for this unit.
* `clears` — whether the unit's mobjects are removed when it ends. Default `True`.

`self.next_slide()` inside a unit is a **pause**: the audience presses a key, but the slide
number does not move. The number advances at unit boundaries. To split one continuous build-up
across several numbers, set `clears = False` on the units that should hand their mobjects to the
next one:

```python
Chapter("Proof", "The proof", units=[
	Steps("Setup", clears=False),   # slide 4, mobjects stay on screen
	Steps("Conclusion"),            # slide 5, builds on them, then clears
])
```

Anything registered with `self.add_to_canvas(...)` survives regardless — that is where the
overlay lives.

### Chapter

An ordered group of units, rendered as one Scene.

```python
Chapter("Method", "Chapter 2: How it works", "Method", units=[...], intro=True)
```

* `name` — the Scene name, so it must be a valid Python identifier and unique in the deck.
* `title` / `short_title` — long form for the chapter card, short form for the overlay.
  `short_title` defaults to `title`.
* `intro` — whether the chapter opens on a title card. Set to `False` to start on the first unit.

### Deck

The presentation itself: metadata plus chapters. `register(globals())` turns it into scenes —
one per chapter, plus `Title` and `End`, plus one preview scene per unit (`Method_S3`).

```python
deck.register(globals())                    # with per-unit previews
deck.register(globals(), previews=False)    # chapters only
```

`intro=False` / `outro=False` on the `Deck` drop the `Title` and `End` scenes.

Every scene knows its own position in the deck, computed from the deck definition rather than
from what has already been rendered. That is why a single chapter or a single unit renders with
the slide number and progress bar it has in the full presentation. A unit preview also replays
any preceding units marked `clears = False`, so it shows what that unit actually sits on.

### Theme

Everything that is not slide content: the chapter bars, the progress bar, the chapter label, the
slide number, the footer, and the three full-frame cards. Subclass it and pass an instance to
`Deck(theme=...)` to restyle a deck without touching a single slide.

## Upgrading from 0.1

0.2 replaces `ModularSlide` / `Chapter` / `Presentation` with `SlideUnit` / `Chapter` / `Deck`.
The presentation is no longer one giant Scene; each chapter is its own Scene and manim-slides
plays them in sequence.

| 0.1 | 0.2 |
| --- | --- |
| `class Slide1(ModularSlide)` | `class Slide1(SlideUnit)` — and instantiate it: `Slide1()` |
| `self.inner_canvas.add(x)` | delete the line; unit mobjects are cleared automatically |
| `self.scenes = [Slide1, Slide2]` | `units=[Slide1(), Slide2()]` |
| `class Chapter1(Chapter)` with `__init__` | `Chapter("Chapter1", "Long title", "Short", units=[...])` |
| `class MyTalk(Presentation)` with `__init__` | `deck = Deck(...)` then `deck.register(globals())` |
| `next_slide(incr=True)` | split into two units; use `clears=False` to keep mobjects |
| `manim-slides render talk.py MyTalk` | `manim-presentations render talk.py` |
