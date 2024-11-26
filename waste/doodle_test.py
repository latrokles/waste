import unittest

import sdl2

from waste import testgui_utils as tgu
from waste.doodle import Doodle


class WrappedDoodle(Doodle):
    def __init__(self, events):
        self.events = events
        super().__init__()

    def redraw(self):
        if self.events:
            sdl2.SDL_PushEvent(self.events.pop(0))
        super().redraw()


class DoodleTest(unittest.TestCase):
    def test_handles_quit_event(self):
        with self.assertRaises(SystemExit):
            WrappedDoodle([tgu.gen_quit()]).run()

    def test_quit_command_handling(self):
        events = [
            tgu.gen_text("q"),
            tgu.gen_text("u"),
            tgu.gen_text("i"),
            tgu.gen_text("t"),
            tgu.gen_key("down", sdl2.SDLK_RETURN),
        ]

        with self.assertRaises(SystemExit):
            WrappedDoodle(events).run()
