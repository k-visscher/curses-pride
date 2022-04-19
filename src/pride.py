#!/usr/bin/env python3
from __future__ import annotations

import sys
import random
from dataclasses import dataclass

from argparse import ArgumentParser

import curses
import curses.ascii
from curses import wrapper


@dataclass
class PrideFlag:
    stripes: list((int, int, int))

    def draw_on(self, window: curses.window) -> None:
        if not curses.has_colors() or not curses.can_change_color():
            raise RuntimeError("terminal doesn't support colors")

        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)

        window_size = window.getmaxyx()
        stripes_count = len(self.stripes)
        stripe_size = int((window_size[0] - 1) / stripes_count)

        for i, stripe in enumerate(self.stripes):
            stripe = tuple(
                map(
                    lambda color: int((color - 0) * (1000 - 0) / (255 - 0) + 0),
                    stripe,
                )
            )

            color_index = i + 1
            color_pair_index = i + 1
            curses.init_color(color_index, *stripe)
            curses.init_pair(color_pair_index, color_index, color_index)

            for j in range(stripe_size):
                window.addstr(
                    i * stripe_size + j,
                    0,
                    " " * window_size[1],
                    curses.color_pair(color_pair_index),
                )


PRIDE_FLAGS = {
    "agender": PrideFlag(
        [
            (0, 0, 0),
            (186, 186, 186),
            (255, 255, 255),
            (186, 245, 132),
            (255, 255, 255),
            (186, 186, 186),
            (0, 0, 0),
        ],
    ),
    "aromantic": PrideFlag(
        [
            (58, 166, 63),
            (168, 212, 122),
            (255, 255, 255),
            (170, 170, 170),
            (0, 0, 0),
        ],
    ),
    "asexual": PrideFlag(
        [
            (0, 0, 0),
            (164, 164, 164),
            (255, 255, 255),
            (129, 0, 129),
        ],
    ),
    "bisexual": PrideFlag(
        [
            (208, 0, 112), 
            (140, 71, 153), 
            (0, 50, 160)
        ],
    ),
    "gay": PrideFlag(
        [
            (255, 0, 24),
            (255, 165, 44),
            (255, 255, 65),
            (0, 128, 24),
            (0, 0, 249),
            (134, 0, 125),
        ],
    ),
    "lesbian": PrideFlag(
        [
            (214, 41, 0), 
            (255, 155, 85), 
            (255, 255, 255), 
            (212, 97, 166), 
            (165, 0, 98)
        ],
    ),
    "mlm": PrideFlag(
        [
            (7, 141, 112), 
            (152, 232, 193), 
            (255, 255, 255), 
            (123, 173, 226), 
            (61, 26, 120)
        ],
    ),
    "non-binary": PrideFlag(
        [
            (255, 244, 48), 
            (255, 255, 255), 
            (156, 89, 209), 
            (0, 0, 0)
        ],
    ),
    "pansexual": PrideFlag(
        [
            (255, 27, 141),
            (255, 218, 0),
            (27, 179, 255),
        ],
    ),
    "transgender": PrideFlag(
        [
            (85, 205, 252),
            (247, 168, 184),
            (255, 255, 255),
            (247, 168, 184),
            (85, 205, 252),
        ],
    ),
}

parser = ArgumentParser(
    description="curses-pride shows your favourite pride flags in a terminal of your choice."
)
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-c",
    "--cycle",
    dest="cycle",
    action="store_const",
    const=True,
    help="cycles through all of the various pride flags",
)
group.add_argument(
    "-r",
    "--random",
    dest="random",
    action="store_const",
    const=True,
    help="shows a random pride flag",
)
group.add_argument(
    "-f",
    "--flag",
    dest="flag",
    choices=[*PRIDE_FLAGS],
    help="shows a pride flag of your choice",
)

arguments = parser.parse_args(sys.argv[1:])


def draw(pride_flag: PrideFlag) -> None:
    def drawing_routine(window):
        window.clear()

        pride_flag.draw_on(window)

        window.refresh()
        window.getkey()

    return drawing_routine


def draw_all(pride_flags: list[PrideFlag]) -> None:
    def drawing_routine(window: curses.window):
        running = True
        while running:
            for pride_flag in pride_flags:
                window.clear()
                window.timeout(1000)

                pride_flag.draw_on(window)

                window.refresh()
                char = window.getch()
                if char == curses.ascii.ESC:
                    running = False
                    break

    return drawing_routine


if arguments.cycle:
    flags = list(PRIDE_FLAGS.values())
    wrapper(draw_all(flags))
elif arguments.random:
    flag = random.choice(list(PRIDE_FLAGS.values()))
    wrapper(draw(flag))
elif arguments.flag:
    flag = PRIDE_FLAGS[arguments.flag]
    wrapper(draw(flag))
else:
    parser.print_help()
