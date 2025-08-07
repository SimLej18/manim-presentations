from manim import *
from manim_slides import Slide

from manim_presentations import ModularSlide


class Presentation(ModularSlide):
	def __init__(self, title="My Presentation", subtitle="Subtitle", first_author="Author", other_authors=None,
	             event=None, year=None, chapters=None):
		super().__init__(self)

		self.title = title
		self.subtitle = subtitle
		self.first_author = first_author
		self.other_authors = other_authors if other_authors is not None else []
		self.event = event
		self.year = year
		self.chapters = chapters if chapters is not None else []
		self.current_chapter = 1
		self.current_slide = 1
		self.current_slide_in_chapter = 1
		self.inner_canvas = Group()  # Initialize the canvas for the presentation

		self.bar_height = 0.05  # Height of the progress bar
		self.bar_padding = 0.25  # Padding around the progress bar

		self.chapter_bars = self.build_chapter_bars()
		self.sub_text = self.build_sub_text()
		self.slide_number = self.build_slide_number()

	def next_slide(self, incr=True):
		# Increment the current slide number
		super().next_slide()

		if incr:
			self.current_slide += 1
			self.current_slide_in_chapter += 1

			# Update the slide number text
			slide_number_anim = self.update_slide_number(play=False)

			# Update the progress bar for the current chapter
			if self.current_chapter < len(self.chapters) and self.current_slide_in_chapter == len(self.chapters[self.current_chapter].scenes):
				# If we reached the end of the chapter, move to the next chapter
				self.current_chapter += 1
				self.current_slide_in_chapter = 1

				# Show the chapter title
				self.chapter_intro()

				chapter_bars_anim = self.update_chapter_bars(play=False)

				self.play(slide_number_anim, chapter_bars_anim, run_time=0.2)
			else:
				self.play(slide_number_anim, run_time=0.2)


	def build_slide_number(self):
		# Build the text at the bottom of each slide, adding elements in the foreground
		slide_nb_text = Text(f"{self.current_slide}", font_size=24, color=LIGHT_GRAY).to_corner(DR, buff=0.15)
		return slide_nb_text

	def update_slide_number(self, play=True):
		# Update the slide number text
		new_slide_nb_text = Text(f"{self.current_slide}", font_size=24, color=LIGHT_GRAY).to_corner(DR, buff=0.15)
		if play:
			self.play(Transform(self.slide_number, new_slide_nb_text), run_time=0.15)
			return None
		else:
			return Transform(self.slide_number, new_slide_nb_text)

	def show_slide_number(self):
		# Show the slide number text
		self.slide_number.set_opacity(1.0)

	def hide_slide_number(self):
		# Hide the slide number text
		self.slide_number.set_opacity(0.0)

	def build_sub_text(self):
		# Build the text at the bottom of each slide, adding elements in the foreground
		title_text = Text(self.title, font_size=24)
		first_author_text = Text(self.first_author, font_size=24, color=LIGHT_GRAY)
		event_text = Text(self.event, font_size=24, slant=ITALIC) if self.event else None
		year_text = Text(self.year, font_size=24) if self.year else None

		elements = [elem for elem in [title_text, first_author_text, event_text, year_text] if elem is not None]

		sub_text = VGroup(*elements).arrange(RIGHT, buff=0.25).to_corner(DL, buff=0.15)

		return sub_text

	def show_sub_text(self):
		# Show the sub text at the bottom of each slide
		self.sub_text.set_opacity(1.0)

	def hide_sub_text(self):
		# Hide the sub text at the bottom of each slide
		self.sub_text.set_opacity(0.0)

	def build_chapter_bar(self, bar_width):
		"""Crée une barre de progression pour un chapitre donné"""
		return RoundedRectangle(
			width=bar_width,
			height=self.bar_height,
			corner_radius=self.bar_height / 2,
			fill_opacity=0.5,
			fill_color=WHITE,
			stroke_width=0
		)

	def build_chapter_bars(self):
		# Cumulative length of all bars (screen - padding)
		total_bar_length = 14 - (len(self.chapters) + 1) * self.bar_padding

		# Width of each bar based on the number of chapters
		bar_width = total_bar_length / len(self.chapters)

		chapter_bars = VGroup()

		for i in range(len(self.chapters)):
			chapter_bars.add(self.build_chapter_bar(bar_width))

		# Position the elements
		chapter_bars.arrange(RIGHT, buff=self.bar_padding).to_edge(UP, buff=0.15)

		return chapter_bars

	def update_chapter_bars(self, play=True):
		current_bar = self.chapter_bars[self.current_chapter - 1]
		if play:
			self.play(current_bar.animate.set_fill(opacity=1.0), run_time=0.15)
			return None
		else:
			return current_bar.animate.set_fill(opacity=1.0)

	def show_chapter_bars(self):
		# Show the progress bar at the top of the presentation
		self.chapter_bars.set_opacity(0.5)
		self.update_chapter_bars()  # Set current chapter bar to full opacity

	def hide_chapter_bars(self):
		# Hide the progress bar at the top of the presentation
		self.chapter_bars.set_opacity(0.0)

	def build_presentation_intro(self):
		# Display the title, subtitle, and author information at the start of the presentation
		title_text = Text(self.title, font_size=48, color=WHITE)
		subtitle_text = Text(self.subtitle, font_size=36, color=WHITE)
		authors_full_str = self.first_author + (", " + ", ".join(self.other_authors) if self.other_authors else "")
		authors_text = Text(authors_full_str, font_size=24, color=LIGHT_GRAY, t2w={self.first_author:SEMIBOLD}) if self.other_authors else None

		all_elems = VGroup(title_text, subtitle_text, authors_text).arrange(DOWN, buff=0.2)

		return all_elems

	def build_chapter_intro(self):
		# Display the chapter title at the start of each chapter
		chapter_title_text = Text(self.chapters[self.current_chapter - 1].chapter_title, font_size=36, color=WHITE)
		chapter_short_title_text = Text(self.chapters[self.current_chapter - 1].chapter_short_title, font_size=24, color=LIGHT_GRAY)

		all_elems = VGroup(chapter_title_text, chapter_short_title_text).arrange(DOWN, buff=0.2)

		return all_elems

	def build_presentation_conclusion(self):
		# Display a conclusion message at the end of the presentation
		conclusion_text = Text("Thank you for your attention!", font_size=36, color=WHITE)
		authors_full_str = self.first_author + (", " + ", ".join(self.other_authors) if self.other_authors else "")
		authors_text = Text(authors_full_str, font_size=24, color=LIGHT_GRAY, t2w={self.first_author:SEMIBOLD}) if self.other_authors else None

		all_elems = VGroup(conclusion_text, authors_text).arrange(DOWN, buff=0.2)

		return all_elems

	def chapter_intro(self):
		self.hide_chapter_bars()
		self.hide_sub_text()
		self.hide_slide_number()

		chapter_elems = self.build_chapter_intro()
		self.play(FadeIn(chapter_elems), run_time=0.5)
		self.next_slide(incr=False)
		self.play(FadeOut(chapter_elems), run_time=0.25)

		self.show_chapter_bars()
		self.show_sub_text()
		self.show_slide_number()

	def presentation_intro(self):
		intro_elems = self.build_presentation_intro()
		self.play(FadeIn(intro_elems), run_time=0.5)
		self.next_slide(incr=False)
		self.play(FadeOut(intro_elems), run_time=0.25)

	def presentation_conclusion(self):
		conclusion_elems = self.build_presentation_conclusion()
		self.play(FadeIn(conclusion_elems), run_time=0.5)

	def construct(self):
		self.presentation_intro()

		self.add_foreground_mobjects(self.chapter_bars, self.sub_text, self.slide_number)

		# For the first chapter only, we need to show the chapter bars and sub text
		self.chapter_intro()

		for i, chapter in enumerate(self.chapters):
			chapter.setup()
			chapter.construct()
			chapter.tear_down()
			self.next_slide(incr=i < len(self.chapters) - 1)

		self.clear()
		self.presentation_conclusion()
		self.wait(0.1)  # Need a small wait so that manim realize we have animations, as they are hidden in chapters
