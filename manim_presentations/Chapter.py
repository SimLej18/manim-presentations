from dataclasses import dataclass, field


@dataclass
class Chapter:
	"""
	An ordered group of `SlideUnit` instances, rendered as one Manim Scene.

	`name` is the Scene name: it is what you pass to `manim-slides render`,
	so it must be a valid Python identifier and unique within the deck.
	"""

	name: str
	title: str
	short_title: str = None
	units: list = field(default_factory=list)
	intro: bool = True
	"""Whether the chapter opens on a title card. Set to False to start straight
	into the first unit."""

	def __post_init__(self):
		if not self.name.isidentifier():
			raise ValueError(f"chapter name {self.name!r} is not a valid Python identifier")
		if self.short_title is None:
			self.short_title = self.title
		if not self.units:
			raise ValueError(f"chapter {self.name!r} has no units")

	def __len__(self):
		return len(self.units)
