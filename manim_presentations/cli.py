"""
`manim-presentations` — run a deck without naming its scenes.

	manim-presentations render deck.py -ql
	manim-presentations present deck.py
	manim-presentations convert deck.py slides.html
	manim-presentations list deck.py

Each command reads the `Deck` defined in the module and passes its scenes to
manim-slides in presentation order. Unrecognised options are forwarded to
manim-slides untouched, so `-ql`, `--full-screen` and friends still work.
"""

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

from .Deck import Deck


def load_deck(path, deck_name=None):
	"""Import a module by path and return the Deck it defines."""
	path = Path(path).resolve()
	if not path.is_file():
		raise SystemExit(f"no such file: {path}")

	spec = importlib.util.spec_from_file_location(path.stem, path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[spec.name] = module
	sys.path.insert(0, str(path.parent))
	try:
		spec.loader.exec_module(module)
	finally:
		sys.path.pop(0)

	decks = {name: value for name, value in vars(module).items()
	         if isinstance(value, Deck) and not name.startswith("__")}
	if deck_name is not None:
		if deck_name not in decks:
			raise SystemExit(f"{path.name} has no deck named {deck_name!r} "
			                 f"(found: {', '.join(sorted(decks)) or 'none'})")
		return decks[deck_name]
	if not decks:
		raise SystemExit(f"{path.name} defines no Deck")
	if len(decks) > 1:
		raise SystemExit(f"{path.name} defines several decks "
		                 f"({', '.join(sorted(decks))}); pick one with --deck")
	return next(iter(decks.values()))


def resolve_scenes(deck, only):
	"""Scene names to run, in presentation order."""
	if not only:
		return deck.scene_names

	known = set(deck.scene_names) | set(deck.preview_names)
	unknown = [name for name in only if name not in known]
	if unknown:
		raise SystemExit(f"unknown scene(s): {', '.join(unknown)}\n"
		                 f"available: {', '.join(sorted(known))}")
	return list(only)


def slides_folder(forwarded):
	"""The --folder manim-slides will look in, default 'slides'."""
	for i, arg in enumerate(forwarded):
		if arg == "--folder" and i + 1 < len(forwarded):
			return Path(forwarded[i + 1])
		if arg.startswith("--folder="):
			return Path(arg.split("=", 1)[1])
	return Path("slides")


def require_rendered(command, module, scenes, folder):
	"""Fail with a command to run, rather than letting manim-slides guess why."""
	missing = [name for name in scenes if not (folder / f"{name}.json").is_file()]
	if not missing:
		return

	only = "" if len(missing) == len(scenes) else " --only " + " ".join(missing)
	where = "" if folder == Path("slides") else f" in {folder}"
	raise SystemExit(
		f"cannot {command}: {len(missing)} of {len(scenes)} scene(s) have no rendered "
		f"slides{where} ({', '.join(missing)}).\n"
		f"Render them first:\n"
		f"    manim-presentations render {module}{only}"
	)


def run(command, *args):
	argv = [sys.executable, "-m", "manim_slides", command, *args]
	print(" ".join(argv), file=sys.stderr)
	return subprocess.call(argv)


def main(argv=None):
	parser = argparse.ArgumentParser(prog="manim-presentations", description=__doc__,
	                                 formatter_class=argparse.RawDescriptionHelpFormatter)
	commands = parser.add_subparsers(dest="command", required=True)

	def add(name, help_text):
		sub = commands.add_parser(name, help=help_text)
		sub.add_argument("module", help="Python file defining a Deck")
		sub.add_argument("--deck", help="name of the Deck, if the module defines several")
		sub.add_argument("--only", nargs="+", metavar="SCENE",
		                 help="restrict to these scenes (chapters or unit previews)")
		return sub

	add("render", "render the deck's scenes with manim-slides")
	add("present", "play the deck")
	convert = add("convert", "export the deck to a file")
	convert.add_argument("dest", help="output file, e.g. slides.html")
	add("list", "print the deck's scene names")

	args, forwarded = parser.parse_known_args(argv)
	deck = load_deck(args.module, args.deck)
	scenes = resolve_scenes(deck, args.only)

	if args.command == "list":
		previews = set(deck.preview_names)
		for chapter_index, chapter in enumerate(deck.chapters):
			print(f"{chapter.name}\t{chapter.title}")
			for unit_index, unit in enumerate(chapter.units):
				name = deck.preview_name(chapter_index, unit_index)
				label = name if name in previews else "-"
				print(f"  {label}\t{type(unit).__name__}")
		print(f"\npresentation order: {' '.join(deck.scene_names)}")
		if not previews:
			print("per-unit previews are disabled (register(..., previews=False))")
		return 0

	if args.command == "render":
		return run("render", str(args.module), *scenes, *forwarded)

	require_rendered(args.command, args.module, scenes, slides_folder(forwarded))
	if args.command == "convert":
		return run("convert", *scenes, args.dest, *forwarded)
	return run("present", *scenes, *forwarded)


if __name__ == "__main__":
	raise SystemExit(main())
