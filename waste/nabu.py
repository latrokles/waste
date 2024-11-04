import json
import pathlib
import subprocess

import click

from dataclasses import dataclass
from typing import List

from waste.draw import Window, fetch_glyph
from waste.draw import BLACK, PALE_YELLOW


OCR_SWIFT_SCRIPT = """
/*
 * ocr.swift
 *
 * a rather minimal swift script to extract text from images using
 * built-in macos facilities.
 *
 * this script is a rather hacky adaptation of @jackrusher's tinyocr
 * https://github.com/jackrusher/tinyocr
 *
 * usage: swift ocr.swift IMAGE_FILEPATH
 */

import Cocoa
import Vision
import Foundation

func main(file: String) {
    let lang: [String] = ["en"]

    let request = VNRecognizeTextRequest { (request, error) in
        let observations = request.results as? [VNRecognizedTextObservation] ?? []
        let obs : [String] = observations.map { $0.topCandidates(1).first?.string ?? "" }
        print(obs.joined(separator: "\\n"))
    }

    request.recognitionLevel = VNRequestTextRecognitionLevel.accurate
    request.usesLanguageCorrection = true
    request.revision = VNRecognizeTextRequestRevision2
    request.recognitionLanguages = lang

    let url = URL(fileURLWithPath: file)
    print(url)
    guard let imgRef = NSImage(byReferencing: url).cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        fatalError("Error: could not convert NSImage to CGImage - '\(url)'")
    }
    try? VNImageRequestHandler(cgImage: imgRef, options: [:]).perform([request])
}


if CommandLine.argc < 2 {
    print("no images passed")
    exit(1)
} else {
    main(file: CommandLine.arguments[1])
    exit(0)
}
"""


CELL_W = 9
CELL_H = 15
COLS = 50
ROWS = 5
PAD_X = 2
PAD_Y = 1
WIDTH = CELL_W * (COLS + (2 * PAD_X))
HEIGHT = CELL_H * (ROWS + (2 * PAD_Y))

TEXT_COLOR = BLACK
BACKGROUND = PALE_YELLOW


@click.command()
def nabu():
    config = pathlib.Path.home() / ".nabu.json"
    Nabu(config_pathname=config)


@dataclass
class Config:
    data_dir: pathlib.Path
    supported_image_extensions: List[str]

    @property
    def script_path(self):
        return self.data_dir / "ocr.swift"


class Nabu(Window):
    def __init__(self, config_pathname):
        self.config = self.parse_config(config_pathname)
        self.ensure_script_presence()
        super().__init__(
            "NABU 📷 -> 📃",
            width=WIDTH,
            height=HEIGHT,
            zoom=1,
            is_resizable=False,
            has_border=False,
            background=BACKGROUND,
        )
        # TODO set window position to top left corner
        # TODO make window always in top (is this even possible)
        # TODO ensure script location
        # TODO parse configuration from homedir

    def parse_config(self, config_pathname):
        if not config_pathname.exists():
            return Config(
                data_dir=(pathlib.Path.home() / "Desktop/OCR"),
                supported_image_extensions=[
                    ".heic",
                    ".png",
                    ".jpeg",
                    ".jpg",
                    ".tiff"
                ],
            )
        return Config(**json.loads(config_pathname.read_text("utf-8")))

    def ensure_script_presence(self):
        if self.config.script_path.exists():
            return
        self.config.script_path.write_text(OCR_SWIFT_SCRIPT, "utf-8")

    def redraw(self):
        # TODO refactor window code to make this more ergonomic
        self.clear()
        self.draw_text(2 * CELL_W, 1 * CELL_H, "Drop image file here to extract text.")
        super().redraw()

    def handle_drop(self, event):
        # TODO
        # right now text output is going to the location of the image file
        # 1. copy image file to data directory
        # 2. use the new image in the data directory as the file to ocr
        # 3. write the ocr txt to the same data dir
        script_path = self.config.script_path
        src_pathname = event.drop.file.decode("utf-8")
        extension = pathlib.Path(src_pathname).suffix
        dst_pathname = src_pathname.replace(extension, ".txt")

        ocr_cmd = ["swift", str(script_path), src_pathname]
        with subprocess.Popen(ocr_cmd, stdout=subprocess.PIPE) as ocr_proc:
            with open(dst_pathname, "w", encoding="utf-8") as output_file:
                for line in ocr_proc.stdout:
                    output_file.write(line.decode('utf-8'))

        launch_cmd = ["open", dst_pathname]
        subprocess.Popen(launch_cmd)

    def draw_text(self, x, y, text):
        posx = x
        posy = y
        for char in text:
            if char == "\n":
                posx = x
                posy += CELL_H
                continue

            self.draw_glyph(
                posx, posy, fetch_glyph(char), CELL_W, CELL_H, TEXT_COLOR, BACKGROUND
            )
            posx += CELL_W
