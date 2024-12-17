import json
import socket
import subprocess
import time


class Player:
    def __init__(self):
        self._sock = "/tmp/mpvsocket"
        self._cmd = ("mpv", "--idle", f"--input-ipc-server={self._sock}")

        self.process = subprocess.Popen(self._cmd, start_new_session=True, shell=False)
        self.ipc = socket.socket(socket.AF_UNIX)
        time.sleep(0.5)
        self.ipc.connect(self._sock)

    def get_progress(self):
        # TODO implement it using https://mpv.io/manual/master/#commands-with-named-arguments
        pass

    def play_url(self, url, video=False):
        video_mode = "auto" if video else "no"
        self._send(["set_property", "video", video_mode])
        self._send(["loadfile", url])

    def play_file(self, filepath):
        if not filepath.exists():
            return
        self._send(["loadfile", str(filepath)])

    def pause(self):
        self._send(["set_property", "pause", True])

    def resume(self):
        self._send(["set_property", "pause", False])

    def stop(self):
        self._send(["stop"])

    def shutdown(self):
        self.ipc.close()
        self.process.terminate()

    def _send(self, command_args):
        command = json.dumps({"command": command_args})
        self.ipc.send((command + "\n").encode("utf-8"))
