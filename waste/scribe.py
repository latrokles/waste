"""
Very simple tool to extract text from images in
a set of directories. Only works on macos.
"""
import pathlib
import subprocess
import time

import click

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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

SUPPORTED_IMAGE_EXTENSIONS = [".heic", ".png", ".jpeg", ".jpg", ".tiff"]


class OCRTrigger(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        if event.event_type == "created":
            pathname = pathlib.Path(event.src_path)
            if pathname.suffix not in SUPPORTED_IMAGE_EXTENSIONS:
                return

            print(f"Image file created {event.src_path}: {event=}.")
            return OCRTrigger.trigger_ocr(pathname)

    @staticmethod
    def trigger_ocr(pathname):
        img_path = str(pathname)
        img_extension = pathname.suffix
        txt_path = img_path.replace(img_extension, ".txt")
        script_path= get_ocr_dir() / "ocr.swift"

        print(f"Extracting text from {img_path=} to {txt_path=}")
        ocr_cmd = ["swift", script_path, img_path, ">", txt_path]
        with subprocess.Popen(ocr_cmd, stdout=subprocess.PIPE) as ocr_proc:
            with open(txt_path, "w", encoding="utf-8") as output_file:
                for line in ocr_proc.stdout:
                    output_file.write(line.decode('utf-8'))


def get_ocr_dir():
    return pathlib.Path.home() / "Desktop/OCR"


def get_script_path():
    return get_ocr_dir() / "ocr.swift"


def ensure_script_presence():
    script_pathname = get_script_path()
    if script_pathname.exists():
        return
    script_pathname.write_text(OCR_SWIFT_SCRIPT, "utf-8")


@click.command()
def scribe():
    ensure_script_presence()
    observer = Observer()
    observer.schedule(OCRTrigger(), str(get_ocr_dir()), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except Exception as e:
        print(e)
        observer.stop()
    observer.join()
