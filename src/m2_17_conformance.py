"""KT M2.17 terminal conformance helpers."""
from dataclasses import dataclass

CORPUS_VERSION = "terminal-corpus-v1"

CP437 = {
    0xB3: "│", 0xC4: "─", 0xDA: "┌", 0xBF: "┐",
    0xC0: "└", 0xD9: "┘", 0xC3: "├", 0xB4: "┤",
    0xC2: "┬", 0xC1: "┴", 0xC5: "┼",
}

def cp437_decode(value):
    if value in CP437:
        return CP437[value]
    return bytes([value]).decode("cp437")

@dataclass(frozen=True)
class GoldenCell:
    x: int
    y: int
    ch: str
    fg: int = 7
    bg: int = 0
    bold: bool = False
    reverse: bool = False

def snapshot(screen):
    out = []
    for y, row in enumerate(screen.cells):
        for x, cell in enumerate(row):
            if cell.ch != " " or cell.bold or cell.reverse or cell.fg != 7 or cell.bg != 0:
                out.append(GoldenCell(x, y, cell.ch, cell.fg, cell.bg, cell.bold, cell.reverse))
    return tuple(out)
