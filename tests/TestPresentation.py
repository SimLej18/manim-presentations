"""
Sample deck used to check that manim_presentations works.

	manim-presentations render tests/TestPresentation.py -ql
	manim-presentations present tests/TestPresentation.py

	manim-slides render tests/TestPresentation.py Chapter1 -ql   # one chapter
	manim-slides render tests/TestPresentation.py Chapter2_S2 -ql # one unit
"""

from manim import *

from manim_presentations import Deck, Chapter, SlideUnit


class Bullets(SlideUnit):
	"""One headline, then one extra line per pause."""

	def __init__(self, headline, *lines, notes="", clears=True):
		self.headline = headline
		self.lines = lines
		self.notes = notes
		self.clears = clears

	def construct(self):
		previous = Text(self.headline, font_size=48)
		self.play(Write(previous), run_time=0.25)

		for line in self.lines:
			self.next_slide()
			following = Text(line, font_size=36).next_to(previous, DOWN, buff=0.5)
			self.play(Write(following), run_time=0.25)
			previous = following


class Aside(SlideUnit):
	"""Keeps what the previous unit left on screen, and adds to it."""

	clears = True

	def construct(self):
		note = Text("...and this unit reused it.", font_size=28, color=YELLOW)
		self.play(Write(note.to_edge(DOWN, buff=1.5)), run_time=0.25)


deck = Deck(
	title="My Presentation",
	subtitle="Subtitle",
	first_author="Author",
	other_authors=["Co-author 1", "Co-author 2"],
	event="My Event",
	year="2025",
	chapters=[
		Chapter("Chapter1", "Chapter 1: Where it all begins", "Chapter 1", units=[
			Bullets("This is the first slide of chapter 1",
			        "It even has a second line!",
			        notes="This is a test note to see if it appears in the render."),
			Bullets("This is the second slide of chapter 1"),
		]),
		Chapter("Chapter2", "Chapter 2: Where everything comes to an end", "Chapter 2", units=[
			Bullets("This is the first slide of chapter 2"),
			Bullets("This is the second slide of chapter 2",
			        "It even has a second line!",
			        "And a third one!",
			        notes="Another test note to see if it appears in the render."),
			# clears=False hands its mobjects to the next unit, which still gets
			# its own slide number.
			Bullets("This is the third slide of chapter 2", clears=False),
			Aside(),
		]),
	],
)

deck.register(globals())
