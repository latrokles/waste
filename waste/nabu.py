import json
import pathlib
import subprocess

import click

from dataclasses import dataclass
from typing import List

from waste import draw
from waste import gui
from waste.font import UNICODE_8x15


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

DEFAULT_DATA_DIR = "Desktop/OCR"
SUPPORTED_IMAGE_EXTENSIONS = [".heic", ".png", ".jpeg", ".jpg", ".tiff"]
ENCODING = "utf-8"
TEXT_SUFFIX = ".txt"


CELL_W = 9
CELL_H = 15
COLS = 37
ROWS = 5
PAD_X = 2
PAD_Y = 1
WIDTH = CELL_W * (COLS + (2 * PAD_X))
HEIGHT = CELL_H * (ROWS + (2 * PAD_Y))

TEXT_COLOR = draw.BLACK
BACKGROUND = draw.PALE_YELLOW


@click.command()
def nabu():
    config = pathlib.Path.home() / ".nabu.json"
    Nabu(font=UNICODE_8x15, config_pathname=config)


@dataclass
class Config:
    data_dir: pathlib.Path
    supported_image_extensions: List[str]

    @property
    def script_path(self):
        return self.data_dir / "ocr.swift"


class Nabu(gui.Window):
    def __init__(self, font, config_pathname):
        super().__init__(
            "NABU 📷 -> 📃",
            width=WIDTH,
            height=HEIGHT,
            zoom=1,
            background=BACKGROUND,
        )
        self.font = font
        self.config = self.parse_config(config_pathname)
        self.ensure_script_presence()
        self.hide_borders()
        self.disable_resizing()
        self.move(0, 0)
        self.enable_always_on_top()
        self.run()

    def parse_config(self, config_pathname):
        if not config_pathname.exists():
            return Config(
                data_dir=(pathlib.Path.home() / DEFAULT_DATA_DIR),
                supported_image_extensions=SUPPORTED_IMAGE_EXTENSIONS,
            )
        return Config(**json.loads(config_pathname.read_text(ENCODING)))

    def ensure_script_presence(self):
        if self.config.script_path.exists():
            return
        self.config.script_path.write_text(OCR_SWIFT_SCRIPT, ENCODING)

    def redraw(self):
        self.clear()
        self.draw_text(
            2 * CELL_W,
            1 * CELL_H,
            "Drop image file here to extract text.",
            self.font,
            TEXT_COLOR,
            BACKGROUND,
        )

    def on_file_drop(self, pathname):
        self.trigger_processing(pathname)

    def trigger_processing(self, pathname):
        script_path = self.config.script_path
        new_img_pathname = self.copy_to_data_dir(pathname)
        new_txt_pathname = new_img_pathname.with_suffix(TEXT_SUFFIX)

        ocr_cmd = ["swift", str(script_path), str(new_img_pathname)]
        with subprocess.Popen(ocr_cmd, stdout=subprocess.PIPE) as ocr_proc:
            with open(new_txt_pathname, "w", encoding=ENCODING) as output_file:
                for line in ocr_proc.stdout:
                    output_file.write(line.decode(ENCODING))

        launch_cmd = ["open", new_txt_pathname]
        subprocess.Popen(launch_cmd)

    def copy_to_data_dir(self, src_img_pathname):
        dst_pathname = self.config.data_dir / src_img_pathname.name
        dst_pathname.write_bytes(src_img_pathname.read_bytes())
        return dst_pathname


if __name__ == "__main__":
    nabu()
