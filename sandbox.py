from manim import *
from manim_slides import Slide

class ProgressBarSlide(Slide):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.total_chapters = 5
		self.current_chapter = 1
		self.slides_per_chapter = 2
		self.bar_height = 0.15
		self.bar_spacing = 0.2
		self.screen_width = 14  # Largeur approximative de l'écran Manim
		self.progress_bars = None

	def update_progress_bars(self):
		"""Met à jour l'affichage des barres de progression"""
		if self.progress_bars is None:
			return

		for i, bar in enumerate(self.progress_bars):
			is_current = (i + 1) == self.current_chapter
			new_opacity = 1.0 if is_current else 0.5
			self.play(bar.animate.set_fill(opacity=new_opacity), run_time=0.3)

	def next_chapter(self):
		"""Passe au chapitre suivant et met à jour les barres"""
		if self.current_chapter < self.total_chapters:
			self.current_chapter += 1
			self.update_progress_bars()

	def create_progress_bar(self, bar_width, is_current=False):
		"""Crée une barre de progression pour un chapitre donné"""
		bar = RoundedRectangle(
			width=bar_width,
			height=self.bar_height,
			corner_radius=self.bar_height / 2,
			fill_opacity=1.0 if is_current else 0.5,
			fill_color=WHITE,
			stroke_width=0
		)
		return bar

	def create_progress_bars(self):
		"""Crée toutes les barres de progression"""
		bars = VGroup()

		# Calcul de la largeur de chaque barre pour occuper toute la largeur
		total_spacing = (self.total_chapters - 1) * self.bar_spacing
		available_width = self.screen_width - total_spacing
		bar_width = available_width / self.total_chapters

		start_x = -self.screen_width / 2 + bar_width / 2

		for i in range(self.total_chapters):
			is_current = (i + 1) == self.current_chapter
			bar = self.create_progress_bar(bar_width, is_current)
			x_pos = start_x + i * (bar_width + self.bar_spacing)
			bar.move_to([x_pos, 3.2, 0])
			bars.add(bar)

		self.progress_bars = bars
		return bars

	def construct(self):
		# Barre de progression (persistante)
		progress_bars = self.create_progress_bars()
		self.add(progress_bars)

		# Chapitre 1
		for slide_num in range(1, self.slides_per_chapter + 1):
			title = Text(f"Chapitre {self.current_chapter} - Slide {slide_num}", font_size=48)
			title.move_to([0, 1, 0])

			content = Text(f"Contenu du chapitre {self.current_chapter}, slide {slide_num}", font_size=32)
			content.move_to([0, -1, 0])

			self.play(Write(title))
			self.play(Write(content))
			self.wait()

			if slide_num < self.slides_per_chapter:
				self.next_slide()
				self.play(FadeOut(title), FadeOut(content))
			else:
				self.next_slide()
				self.play(FadeOut(title), FadeOut(content))
				if self.current_chapter < self.total_chapters:
					self.next_chapter()

		# Chapitres suivants
		for chapter in range(2, self.total_chapters + 1):
			for slide_num in range(1, self.slides_per_chapter + 1):
				title = Text(f"Chapitre {self.current_chapter} - Slide {slide_num}", font_size=48)
				title.move_to([0, 1, 0])

				content = Text(f"Contenu du chapitre {self.current_chapter}, slide {slide_num}", font_size=32)
				content.move_to([0, -1, 0])

				self.play(Write(title))
				self.play(Write(content))
				self.wait()

				if slide_num < self.slides_per_chapter:
					self.next_slide()
					self.play(FadeOut(title), FadeOut(content))
				else:
					self.next_slide()
					self.play(FadeOut(title), FadeOut(content))
					if self.current_chapter < self.total_chapters:
						self.next_chapter()


if __name__ == "__main__":
	scene = ProgressBarSlide()
	scene.render()