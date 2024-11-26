import unittest

import sdl2

from waste import testgui_utils as tgu
from waste.doodle import Doodle


@unittest.skipIf(tgu.skip_gui_tests(), "SKIPGUI is 'true'")
class DoodleTest(unittest.TestCase):
    def setUp(self):
        self.doodle = Doodle()

    def test_handles_quit_event(self):
        with self.assertRaises(SystemExit):
            tgu.patch_test_events(self.doodle, [tgu.gen_quit()]).run()

    def test_quit_command_handling(self):
        events = [
            tgu.gen_text("q"),
            tgu.gen_text("u"),
            tgu.gen_text("i"),
            tgu.gen_text("t"),
            tgu.gen_key("down", sdl2.SDLK_RETURN),
        ]

        with self.assertRaises(SystemExit):
            tgu.patch_test_events(self.doodle, events).run()
