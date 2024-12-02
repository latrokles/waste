import pathlib

import click
import jinja2
import markdown


HTML_ENGINE = None


@click.group()
def archivist():
    pass


@archivist.command()
@click.option("--src", type=str, required=True)
@click.option("--dst", type=str, required=True)
def publish(src, dst):
    src = pathlib.Path(src).resolve()
    dst = pathlib.Path(dst).resolve()

    if not src.exists():
        raise RuntimeError(f"{src = } does not exist!")

    if not dst.exists():
        raise RuntimeError(f"{dst = } does not exist!")

    initialize_html_renderer(src)
    generate_content(src, dst)
    print("DONE!!!")


def initialize_html_renderer(root):
    global HTML_ENGINE
    template_dir = root / "_templates"
    HTML_ENGINE = jinja2.Environment(loader=jinja2.FileSystemLoader(str(template_dir)))


def generate_content(src, dst):
    for path in src.glob("*"):
        if path.name in (
            ".git",
            "README.md",
            "_templates",
        ):
            continue

        path_in_dst = dst / path.name

        if path.is_dir():
            if not path_in_dst.exists():
                path_in_dst.mkdir()

            generate_content(path, path_in_dst)

        elif path.suffix == ".md":
            markdown_to_html(path, path_in_dst)

        elif path.suffix in (".c", ".py", ".scowl"):
            suffix = path_in_dst.suffix
            path_in_dst = path_in_dst.with_suffix(f"{suffix}.txt")
            path_in_dst.write_text(path.read_text("utf-8"), "utf-8")

        elif path.suffix in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tga"):
            path_in_dst.write_bytes(path.read_bytes())

        else:
            path_in_dst.write_text(path.read_text("utf-8"), "utf-8")
    print(f"Generated `{dst}`!")


def markdown_to_html(src_file, dst_file):
    metadata = {}
    source_data = src_file.read_text("utf-8")
    if source_data.startswith("---"):
        metadata, source_data = extract_metadata(source_data[4:])

    template_name = metadata.get("template", "default.html")
    template = HTML_ENGINE.get_template(template_name)

    rendered_page = template.render(
        title=metadata.get("title", ""),
        date=metadata.get("date", ""),
        tags=metadata.get("tags", "").split(","),
        content=markdown.markdown(source_data, extensions=["fenced_code"]),
    )

    dst_file.with_suffix(".html").write_text(rendered_page, "utf-8")


def extract_metadata(page_data):
    def parse_metadata(md):
        parsed = {}
        for line in md.split("\n"):
            key, *rest = line.split(":")
            parsed[key] = "".join(rest)
        return parsed

    delimiter_pos = page_data.find("---")
    metadata_text = page_data[:delimiter_pos]

    metadata = parse_metadata(metadata_text)
    content = page_data[delimiter_pos + 5 :]
    return metadata, content
