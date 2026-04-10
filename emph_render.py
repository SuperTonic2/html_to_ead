from lxml import etree
import sys
from pathlib import Path

# Generated with assistance from Microsoft 365 Copilot (GPT‑5 chat model)

def process_emph_in_file(file_path):
    parser = etree.XMLParser(remove_blank_text=False)

    # Read file contents
    text = Path(file_path).read_text(encoding="utf-8")

    # FIX: normalize HTML non-breaking space to Unicode
    text = text.replace("&nbsp;", "\u00A0")

    # Wrap fragment so it parses as XML
    wrapped = f"<root>{text}</root>"
    root = etree.fromstring(wrapped.encode("utf-8"), parser)

    # Find <emph> without @render (namespace-agnostic)
    emph_elements = root.xpath(".//*[local-name() = 'emph' and not(@render)]")

    for emph in emph_elements:
        parent = emph.getparent()

        # Rule 1: header — sole content of a <p>
        if (
            parent is not None
            and parent.tag.lower() == "p"
            and len(parent) == 1
            and (parent.text is None or parent.text.strip() == "")
            and emph.tail is None
        ):
            emph.set("render", "bold")
        else:
            emph.set("render", "italic")

    # Serialize only the fragment (children of dummy root)
    output = "".join(
        etree.tostring(child, encoding="unicode", pretty_print=True)
        for child in root
    )

    # Overwrite the same file
    Path(file_path).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python emph_render.py path/to/fragment.xml")
        sys.exit(1)

    process_emph_in_file(sys.argv[1])