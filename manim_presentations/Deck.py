from dataclasses import dataclass

from manim import *
from manim_slides import ThreeDSlide

from .Theme import Theme

TITLE_SCENE = "Title"
END_SCENE = "End"


@dataclass(frozen=True)
class Position:
	"""
	Where a unit sits in the whole deck.

	Positions are derived from the deck definition alone, never from what has
	already been rendered. That is what lets a single chapter — or a single
	unit — render with the same slide number and progress bar it has in the
	full presentation.
	"""

	deck: "Deck"
	chapter_index: int
	unit_index: int

	@property
	def chapter(self):
		return self.deck.chapters[self.chapter_index]

	@property
	def unit(self):
		return self.chapter.units[self.unit_index]

	@property
	def number(self):
		"""Slide number shown in the corner. Counts units, not intra-unit pauses."""
		before = sum(len(c) for c in self.deck.chapters[:self.chapter_index])
		return 1 + before + self.unit_index

	@property
	def chapter_fraction(self):
		return (self.unit_index + 1) / len(self.chapter)


class Deck:
	"""
	A whole presentation: metadata plus an ordered list of `Chapter` objects.

	A deck is plain data. Call `register(globals())` at the end of your module
	to turn it into the Manim Scenes that manim-slides renders and plays:

		deck.register(globals())

	That defines one Scene per chapter, named after the chapter, plus `Title`
	and `End`, plus one preview Scene per unit (`Ch1_S2`, ...). Render and play
	the whole thing without naming any of them:

		manim-presentations render deck.py -ql
		manim-presentations present deck.py
	"""

	def __init__(self, title="My Presentation", subtitle="", short_title=None,
	             first_author="Author", other_authors=None, event=None, year=None,
	             chapters=None, theme=None, intro=True, outro=True):
		if not chapters:
			raise ValueError("a deck must contain at least one chapter")

		self.title = title
		self.subtitle = subtitle
		self.short_title = short_title if short_title is not None else _shorten(title)
		self.first_author = first_author
		self.other_authors = list(other_authors) if other_authors else []
		self.event = event
		self.year = year
		self.chapters = list(chapters)
		self.theme = theme if theme is not None else Theme()
		self.intro = intro
		self.outro = outro
		self._preview_names = []

		names = [c.name for c in self.chapters]
		duplicates = {n for n in names if names.count(n) > 1}
		if duplicates:
			raise ValueError(f"duplicate chapter names: {', '.join(sorted(duplicates))}")
		reserved = set(names) & {TITLE_SCENE, END_SCENE}
		if reserved:
			raise ValueError(f"chapter names {', '.join(sorted(reserved))} are reserved")

	# ----------------------------------------------------------------- layout
	@property
	def scene_names(self):
		"""Every Scene of the presentation, in presentation order."""
		names = [c.name for c in self.chapters]
		if self.intro:
			names.insert(0, TITLE_SCENE)
		if self.outro:
			names.append(END_SCENE)
		return names

	def positions(self, chapter_index):
		return [Position(self, chapter_index, i)
		        for i in range(len(self.chapters[chapter_index]))]

	def preview_name(self, chapter_index, unit_index):
		return f"{self.chapters[chapter_index].name}_S{unit_index + 1}"

	@property
	def preview_names(self):
		"""Per-unit preview Scenes, empty until `register(previews=True)` ran."""
		return list(self._preview_names)

	def _preview_slice(self, chapter_index, unit_index):
		"""
		Units a single-unit preview has to replay.

		A unit that follows one with `clears = False` depends on what that unit
		left on screen, so the preview starts at the first unit of the run.
		"""
		units = self.chapters[chapter_index].units
		start = unit_index
		while start > 0 and not units[start - 1].clears:
			start -= 1
		return slice(start, unit_index + 1)

	# --------------------------------------------------- scene generation
	def _chapter_scene(self, chapter_index, unit_slice=None):
		deck, theme = self, self.theme
		chapter = self.chapters[chapter_index]
		positions = self.positions(chapter_index)
		if unit_slice is not None:
			positions = positions[unit_slice]

		class ChapterScene(ThreeDSlide):
			skip_reversing = True
			wait_time_between_slides = 0.1

			def construct(self):
				first = positions[0]

				if chapter.intro:
					card = theme.chapter_intro(chapter)
					self.play(FadeIn(card), run_time=0.5)
					self.next_slide(notes=first.unit.notes)
					self.play(FadeOut(card), run_time=0.25)
					theme.install(self, first)
					self.play(FadeIn(*self.canvas_mobjects), run_time=0.2)
				else:
					self.next_slide(notes=first.unit.notes)
					theme.install(self, first)

				for i, position in enumerate(positions):
					position.unit.bind(self).construct()

					if i + 1 == len(positions):
						self.wait(self.wait_time_between_slides)
						break

					following = positions[i + 1]
					self.next_slide(notes=following.unit.notes)
					if position.unit.clears:
						self.remove(*self.mobjects_without_canvas)
					self.play(*theme.retarget(self, following), run_time=0.2)

		return ChapterScene

	def _card_scene(self, build):
		deck, theme = self, self.theme

		class CardScene(ThreeDSlide):
			skip_reversing = True

			def construct(self):
				self.play(FadeIn(build(deck)), run_time=0.5)

		return CardScene

	def register(self, namespace, previews=True):
		"""
		Define this deck's Scene classes in `namespace` (pass `globals()`).

		`previews=False` leaves out the per-unit Scenes, which keeps
		`manim-slides list-scenes` short on a long deck.
		"""
		scenes = {}
		self._preview_names = []
		if self.intro:
			scenes[TITLE_SCENE] = self._card_scene(self.theme.deck_intro)

		for chapter_index, chapter in enumerate(self.chapters):
			scenes[chapter.name] = self._chapter_scene(chapter_index)
			if previews:
				for unit_index in range(len(chapter)):
					name = self.preview_name(chapter_index, unit_index)
					scenes[name] = self._chapter_scene(
						chapter_index, self._preview_slice(chapter_index, unit_index))
					self._preview_names.append(name)

		if self.outro:
			scenes[END_SCENE] = self._card_scene(self.theme.deck_outro)

		module = namespace.get("__name__", __name__)
		for name, scene in scenes.items():
			scene.__name__ = scene.__qualname__ = name
			scene.__module__ = module  # manim only collects scenes defined in the module
			namespace[name] = scene

		return scenes


def _shorten(title, limit=35):
	flat = title.replace("\n", " ").strip()
	return flat if len(flat) <= limit else flat[:limit].rstrip() + "..."
