import pathlib

import click
import markdown


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

    generate_content(src, dst)


def generate_content(src, dst):
    print(f"generating static pages from {src=} to {dst=}")

    for path in src.glob("*"):
        if path.name in (".git", "README.md", "_templates",):
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

        else:
            path_in_dst.write_text(path.read_text("utf-8"), "utf-8")


def markdown_to_html(src_file, dst_file):
    frontmatter = {}
    source_data = src_file.read_text("utf-8")
    if source_data.startswith("---"):
        frontmatter, source_data = extract_frontmatter(source_data[4:])

    dst_file = dst_file.with_suffix(".html")
    dst_file.write_text(markdown.markdown(source_data), "utf-8")


def extract_frontmatter(page_data):
    def parse_frontmatter(fm):
        parsed = {}
        for line in fm.split("\n"):
            key, *rest = line.split(":")
            parsed[key] = "".join(rest)
        return parsed

    delimiter_pos = page_data.find("---")
    frontmatter_text = page_data[:delimiter_pos]

    frontmatter = parse_frontmatter(frontmatter_text)
    content = page_data[delimiter_pos + 5:]
    return frontmatter, content
