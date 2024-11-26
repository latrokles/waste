import sdl2

from types import MethodType


def patch_test_events(instance, events):
    setattr(instance, "events", events)

    self_redraw = instance.redraw

    def patched_redraw(self):
        if self.events:
            sdl2.SDL_PushEvent(self.events.pop(0))
        self_redraw()

    instance.redraw = MethodType(patched_redraw, instance)
    return instance


def gen_quit():
    e = sdl2.SDL_Event()
    e.type = sdl2.SDL_QUIT
    return e


def gen_key(action, key):
    t = sdl2.SDL_KEYDOWN if action == "down" else sdl2.SDL_KEYUP
    e = sdl2.SDL_Event()
    e.type = t
    e.key.keysym.sym = key
    return e


def gen_text(txt):
    e = sdl2.SDL_Event()
    e.type = sdl2.SDL_TEXTINPUT
    e.text.text = txt.encode("utf-8")
    return e


def gen_mouse_button(action, button):
    t = sdl2.SDL_MOUSEBUTTONDOWN if action == "down" else sdl2.SDL_MOUSEBUTTONUP
    e = sdl2.SDL_Event()
    e.type = t

    match button:
        case "left":
            e.button.button = 1
        case "middle":
            e.button.button = 2
        case "right":
            e.button.button = 3
    return e


def gen_mouse_motion(x, y):
    e = sdl2.SDL_Event()
    e.type = sdl2.SDL_MOUSEMOTION
    e.motion.x = x
    e.motion.y = y
    return e
