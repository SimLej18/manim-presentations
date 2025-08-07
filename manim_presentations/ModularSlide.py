from manim import *
from manim_slides import Slide


class ModularSlide(Slide):
	"""
	Abstract class for a modular slide. Extend it with a construct() method to build your slide.
	"""
	skip_reversing = True

	def __init__(self, ctx=None):
		super().__init__()
		if ctx:
			# update self so that methods of the parent Presentation class have priority
			self.ctx = ctx
		else:
			self.ctx = self
			self.inner_canvas = Group()

	def construct(self):
		# N.b: if called from a Presentation, the canvas might already be added to the Presentation's canvas
		self.add(self.inner_canvas)

	def tear_down(self):
		# By default, clear the canvas after the slide is done
		self.inner_canvas.remove(*self.inner_canvas.submobjects)
