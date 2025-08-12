"""
Little sample presentation using manim_presentations.
This is a test file to check that the presentation works as expected.
It defines two chapters, each with a few basic slides.

It can be run with the following commands from the root of the repository:
`manim-slides render tests/TestPresentation.py TestPresentation`
`manim-slides TestPresentation`
"""

from manim import *

from manim_presentations import ModularSlide, Chapter, Presentation


class Slide1(ModularSlide):
	notes = """This is a test note to see if it appears in the render."""

	def construct(self):
		content = Text("This is the first slide of chapter 1", font_size=48)
		self.inner_canvas.add(content)
		self.play(Write(content))


class Slide2(ModularSlide):
	def construct(self):
		content = Text("This is the second slide of chapter 1", font_size=48)
		self.inner_canvas.add(content)
		self.play(Write(content))


class Slide3(ModularSlide):
	def construct(self):
		content = Text("This is the first slide of chapter 2", font_size=48)
		self.inner_canvas.add(content)
		self.play(Write(content))


class Slide4(ModularSlide):
	notes = """Another test note to see if it appears in the render."""

	def construct(self):
		content = Text("This is the second slide of chapter 2", font_size=48)
		self.inner_canvas.add(content)
		self.play(Write(content))

class Slide5(ModularSlide):
	def construct(self):
		content = Text("This is the third slide of chapter 2", font_size=48)
		self.inner_canvas.add(content)
		self.play(Write(content))


class Chapter1(Chapter):
	def __init__(self, presentation=None):
		super().__init__(presentation)
		self.scenes = [Slide1, Slide2]


class Chapter2(Chapter):
	def __init__(self, presentation=None):
		super().__init__(presentation)
		self.scenes = [Slide3, Slide4, Slide5]


class TestPresentation(Presentation):
	def __init__(self):
		super().__init__(
			title="My Presentation",
			subtitle="Subtitle",
			first_author="Author",
			other_authors=["Co-author 1", "Co-author 2"],
			event="My Event",
			year="2025",
			chapters=[Chapter1(), Chapter2()]
		)

class TestPresentation2(Presentation):  # Try empty presentation
	def __init__(self):
		super().__init__(
			title="My Presentation",
			subtitle="Subtitle",
			first_author="Author",
			other_authors=["Co-author 1", "Co-author 2"],
			event="My Event",
			year="2025",
			chapters=[]
		)

class TestPresentation3(Presentation):  # Try without other_authors and with long title
	def __init__(self):
		super().__init__(
			title="An extremely long title that would\n definitely not fit at\n the bottom ot the slide",
			subtitle="Subtitle",
			first_author="Author",
			other_authors=[],
			event="My Event",
			year="2025",
			chapters=[Chapter1()]
		)
