from docutils.nodes import title
from manim import *
from manim_slides import Slide

from manim_presentations import ModularSlide, Chapter, Presentation


class Slide1(ModularSlide):
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


class MyPresentation(Presentation):
	def __init__(self):
		super().__init__(
			title="My Presentation",
			subtitle="Subtitle",
			first_author="Author",
			other_authors=["Co-author 1", "Co-author 2"],
			event="My Event",
			year="2023",
			chapters=[Chapter1(self), Chapter2(self)]
		)
