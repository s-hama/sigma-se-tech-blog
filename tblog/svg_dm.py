"""Generate dark article SVGs without changing geometry or light originals.

Run from the repository root: python3 -m tblog.svg_dm [--check]
Only Python's standard library is required.
"""

import argparse
from pathlib import Path
import re
import xml.etree.ElementTree as ET


IMAGE_DIR = Path(__file__).resolve().parent.parent / "static" / "tblog" / "img"
SOURCE_NAME = re.compile(r"pid\d+_\d+\.svg\Z")
PAINT_NAMES = r"fill|stroke|color|stop-color|flood-color|lighting-color"
PAINT_ATTRIBUTE = re.compile(
    rf"(?<![\w:-])({PAINT_NAMES})(\s*=\s*)([\"'])(.*?)(\3)", re.I
)
PAINT_DECLARATION = re.compile(
    rf"(?<![\w-])({PAINT_NAMES})(\s*:\s*)([^;}}\"']+)", re.I
)
# Bootstrap 5.3's existing grayscale palette. White fills become dark surfaces;
# the site's gray-700 text/strokes become white. This also preserves reversed
# white labels inside filled bands (pid71_3 and pid76_1).
COLOR_MAP = {
    "#212529": "#ffffff",  # gray-900
    "#343a40": "#f8f9fa",  # gray-800 -> gray-100
    "#495057": "#ffffff",  # gray-700
    "#6c757d": "#dee2e6",  # gray-600 -> gray-300
    "#adb5bd": "#ced4da",  # gray-500 -> gray-400
    "#ced4da": "#adb5bd",
    "#dee2e6": "#6c757d",
    "#e9ecef": "#495057",  # gray-200 -> gray-700
    "#f8f9fa": "#343a40",
    "#ffffff": "#212529",
    "black": "#ffffff",
    "#000000": "#ffffff",
    "white": "#212529",
}


def dark_color(value):
    color = value.strip().lower()
    if color in {"none", "transparent", "currentcolor", "inherit"}:
        return value
    if re.fullmatch(r"#[0-9a-f]{3}", color):
        color = "#" + "".join(char * 2 for char in color[1:])
    rgb = re.fullmatch(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", color)
    if rgb:
        color = "#" + "".join(f"{int(channel):02x}" for channel in rgb.groups())
    if color not in COLOR_MAP:
        raise ValueError(f"Unmapped SVG color {value!r}; review its meaning before adding a grayscale mapping")
    return COLOR_MAP[color]


def render_dark(source):
    root = ET.fromstring(source)
    result = PAINT_ATTRIBUTE.sub(
        lambda m: f"{m[1]}{m[2]}{m[3]}{dark_color(m[4])}{m[5]}", source
    )
    result = PAINT_DECLARATION.sub(
        lambda m: f"{m[1]}{m[2]}{dark_color(m[3])}", result
    )
    # External SVGs cannot inherit the HTML theme. Explicit defaults cover
    # implicit black fills and MathJax paths that use currentColor.
    defaults = "".join(
        f' {name}="#ffffff"' for name in ("color", "fill") if name not in root.attrib
    )
    result = re.sub(r"<svg(?=\s)", lambda m: m[0] + defaults, result, count=1)
    ET.fromstring(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report missing/stale variants without writing")
    args = parser.parse_args()
    outputs = {}
    for source in sorted(IMAGE_DIR.iterdir()):
        if SOURCE_NAME.fullmatch(source.name):
            try:
                outputs[source.with_stem(source.stem + "_dm")] = render_dark(source.read_text())
            except (ValueError, ET.ParseError) as error:
                parser.exit(1, f"{source.name}: {error}\n")
    stale = []
    for target, content in outputs.items():
        if not target.exists() or target.read_text() != content:
            stale.append(target.name)
            if not args.check:
                target.write_text(content)
    if args.check and stale:
        parser.exit(1, "Missing/stale dark SVGs: " + ", ".join(stale) + "\nRun python3 -m tblog.svg_dm\n")
    print(f"{len(outputs)} dark SVGs {'verified' if args.check else 'generated/updated'}.")


if __name__ == "__main__":
    main()
