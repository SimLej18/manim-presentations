class SlideUnit:
	"""
	One unit of content in a presentation. Not a Scene.

	Write `construct` exactly as you would in a Manim Scene: inside it, `self`
	forwards every unknown attribute to the Scene that is currently rendering
	the unit, so `self.play`, `self.add`, `self.wait`, `self.next_slide` and
	`self.camera` all behave normally.

	Because units are ordinary objects, they can take constructor arguments and
	be reused:

		class Bullets(SlideUnit):
			def __init__(self, *lines):
				self.lines = lines

			def construct(self):
				...
	"""

	notes = ""
	"""Presenter notes, shown for this unit during `manim-slides present`."""

	clears = True
	"""
	Whether the mobjects this unit added are removed when it ends.

	Set it to False to keep them on screen for the next unit. Use that to split
	one continuous build-up over several units, each with its own slide number:
	the first units keep their mobjects, the last one clears them.

	Mobjects registered on the manim-slides canvas (`self.add_to_canvas`) are
	never cleared by this.
	"""

	def __getattr__(self, name):
		scene = self.__dict__.get("_scene")
		if scene is None:
			raise AttributeError(
				f"{type(self).__name__}.{name} was accessed outside of a render. "
				f"Scene attributes are only available inside construct()."
			)
		return getattr(scene, name)

	def bind(self, scene):
		"""Attach the unit to the Scene that is about to render it."""
		self.__dict__["_scene"] = scene
		return self

	def construct(self):
		raise NotImplementedError(f"{type(self).__name__} has no construct() method")
