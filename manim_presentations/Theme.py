from manim import *


class Theme:
	"""
	Builds every mobject that is not slide content: the persistent overlay and
	the full-frame title cards.

	Subclass it and pass an instance to `Deck(theme=...)` to restyle a deck
	without touching its content.
	"""

	bar_height = 0.05
	bar_padding = 0.25
	overlay_opacity = 0.7

	def __init__(self, title_color=WHITE, title_weight=BOLD, chapter_color=WHITE,
	             progress_color=GREEN):
		self.title_color = title_color
		self.title_weight = title_weight
		self.chapter_color = chapter_color
		self.progress_color = progress_color

	# ------------------------------------------------------------------ parts
	def chapter_bars(self, position):
		"""One bar per chapter, the current one highlighted."""
		deck = position.deck
		total = config.frame_width - (len(deck.chapters) + 1) * self.bar_padding
		width = total / len(deck.chapters)

		bars = VGroup(*[
			RoundedRectangle(width=width, height=self.bar_height,
			                 corner_radius=self.bar_height / 2,
			                 fill_opacity=0.5, fill_color=self.chapter_color,
			                 stroke_width=0)
			for _ in deck.chapters
		]).arrange(RIGHT, buff=self.bar_padding).to_edge(UP, buff=0.5)

		bars[position.chapter_index].set_fill(opacity=1.0)
		return bars

	def progress(self, bars, position):
		"""Filled portion of the current chapter's bar."""
		bar = bars[position.chapter_index]
		return RoundedRectangle(width=bar.width * position.chapter_fraction,
		                        height=self.bar_height, corner_radius=self.bar_height,
		                        fill_opacity=1.0, fill_color=self.progress_color,
		                        stroke_width=0).move_to(bar).align_to(bar, LEFT)

	def chapter_label(self, bars, position):
		return Text(position.chapter.short_title, font_size=20,
		            color=self.title_color, weight=self.title_weight) \
			.to_edge(UP, buff=0.15).align_to(bars, LEFT)

	def slide_number(self, position):
		return Text(str(position.number), font_size=24, color=self.title_color,
		            weight=self.title_weight) \
			.to_corner(DR, buff=0.15).set_opacity(self.overlay_opacity)

	def footer(self, deck):
		parts = [Text(deck.short_title, font_size=16, color=self.title_color),
		         Text(deck.first_author, font_size=16, color=self.title_color,
		              weight=SEMIBOLD)]
		if deck.event:
			parts.append(Text(deck.event, font_size=16, color=self.title_color,
			                  slant=ITALIC))
		if deck.year:
			parts.append(Text(str(deck.year), font_size=16, color=self.title_color))
		return VGroup(*parts).arrange(RIGHT, buff=0.25) \
			.to_corner(DL, buff=0.15).set_opacity(self.overlay_opacity)

	# -------------------------------------------------------------- lifecycle
	def install(self, scene, position):
		"""
		Put the overlay on the manim-slides canvas, showing `position`.

		Canvas mobjects survive `Deck`'s clearing between units, so a unit never
		has to know the overlay exists.
		"""
		bars = self.chapter_bars(position)
		scene.add_to_canvas(bars=bars,
		                    progress=self.progress(bars, position),
		                    chapter_label=self.chapter_label(bars, position),
		                    slide_number=self.slide_number(position),
		                    footer=self.footer(position.deck))
		scene.add_foreground_mobjects(*scene.canvas_mobjects)

	def retarget(self, scene, position):
		"""Animations that move an installed overlay to `position`."""
		canvas = scene.canvas
		return [Transform(canvas["progress"], self.progress(canvas["bars"], position)),
		        Transform(canvas["slide_number"], self.slide_number(position))]

	# ------------------------------------------------------------------ cards
	def _authors(self, deck):
		names = deck.first_author
		if deck.other_authors:
			names += ", " + ", ".join(deck.other_authors)
		return Text(names, font_size=24, color=self.title_color,
		            t2w={deck.first_author: self.title_weight}) \
			.set_opacity(self.overlay_opacity)

	def deck_intro(self, deck):
		return VGroup(
			Paragraph(deck.title, alignment="center", font_size=48, color=self.title_color),
			Text(deck.subtitle, font_size=36, color=self.title_color, weight=self.title_weight),
			self._authors(deck),
		).arrange(DOWN, buff=1)

	def deck_outro(self, deck):
		return VGroup(
			Text("Thank you for your attention!", font_size=36,
			     color=self.title_color, weight=self.title_weight),
			self._authors(deck),
		).arrange(DOWN, buff=0.2)

	def chapter_intro(self, chapter):
		parts = [Text(chapter.title, font_size=36, color=self.title_color,
		              weight=self.title_weight)]
		if chapter.short_title != chapter.title:
			parts.append(Text(chapter.short_title, font_size=24, color=self.title_color,
			                  weight=self.title_weight).set_opacity(self.overlay_opacity))
		return VGroup(*parts).arrange(DOWN, buff=0.2)
