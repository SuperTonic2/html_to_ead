from lxml import etree
from pathlib import Path
import sys
import re

# Generated with assistance from Microsoft 365 Copilot (GPT‑5 chat model)

def html_to_ead_xml_in_place(file_path):
    parser = etree.XMLParser(remove_blank_text=False)

    # -------------------------------------------------
    # READ INPUT
    # -------------------------------------------------
    text = Path(file_path).read_text(encoding="utf-8")

    # -------------------------------------------------
    # ENTITY NORMALIZATION (FINAL AND STABLE)
    # -------------------------------------------------

    # 1. Normalize curly double quotes → "
    text = re.sub(r'(?:&amp;)*ldquo;', '"', text)
    text = re.sub(r'(?:&amp;)*rdquo;', '"', text)

    # 2. Normalize curly single quotes → '
    text = re.sub(r'(?:&amp;)*lsquo;', "'", text)
    text = re.sub(r'(?:&amp;)*rsquo;', "'", text)

    # 3. Normalize common accented HTML entities → Unicode
    text = re.sub(r'(?:&amp;)*eacute;', 'é', text)
    text = re.sub(r'(?:&amp;)*oacute;', 'ó', text)
    text = re.sub(r'(?:&amp;)*aacute;', 'á', text)
    text = re.sub(r'(?:&amp;)*iacute;', 'í', text)
    text = re.sub(r'(?:&amp;)*uuml;', 'ü', text)
    text = re.sub(r'(?:&amp;)*ouml;', 'ö', text)
    text = re.sub(r'(?:&amp;)*auml;', 'ä', text)
    text = re.sub(r'(?:&amp;)*ntilde;', 'ñ', text)
    text = re.sub(r'(?:&amp;)*ccedil;', 'ç', text)

    # 4. Normalize non‑breaking space
    text = text.replace("&nbsp;", "\u00A0")
    text = text.replace("&amp;nbsp;", "\u00A0")

    # 5. Normalize en dash and em dash → Unicode
    text = re.sub(r'(?:&amp;amp;)*ndash;', '–', text)
    text = re.sub(r'(?:&amp;amp;)*mdash;', '—', text)
    text = re.sub(r'(?:&amp;)–', '–', text)
    text = re.sub(r'(?:&amp;)—', '—', text)
    

    # -------------------------------------------------
    # TAG NORMALIZATION (REAL TAGS, NOT ESCAPED)
    # -------------------------------------------------

    # extref → ref
    text = text.replace("<extref", "<ref")
    text = text.replace("</extref>", "</ref>")
    text = text.replace("xlink:href", "href")

    # a → ref
    text = text.replace("<a ", "<ref ")
    text = text.replace("</a>", "</ref>")

    # -------------------------------------------------
    # AMPERSAND HANDLING (CRITICAL SECTION)
    # -------------------------------------------------

    # Collapse any pre‑existing over‑escaped ampersands
    while "&amp;amp;" in text:
        text = text.replace("&amp;amp;", "&amp;")

    # Escape only truly bare ampersands (never entities)
    text = re.sub(
        r'&(?![A-Za-z]+;|#[0-9]+;|#x[0-9A-Fa-f]+;)',
        '&amp;',
        text
    )

    # -------------------------------------------------
    # PARAGRAPH NORMALIZATION (PLAIN TEXT → <p>)
    # -------------------------------------------------

    blocks = re.split(r'\n\s*\n+', text.strip())

    wrapped_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped.startswith("<p"):
            wrapped_blocks.append(block)
        else:
            wrapped_blocks.append(f"<p>{block}</p>")

    text = "\n\n".join(wrapped_blocks)

    # -------------------------------------------------
    # PARSE AS XML FRAGMENT
    # -------------------------------------------------

    wrapped = f"<root>{text}</root>"
    root = etree.fromstring(wrapped.encode("utf-8"), parser)

    # -------------------------------------------------
    # STRUCTURAL TAG CONVERSIONS
    # -------------------------------------------------

    # <strong> → <emph render="bold">
    for strong in root.xpath(".//*[local-name()='strong']"):
        strong.tag = "emph"
        strong.set("render", "bold")

    # <em> / <i> → <emph render="italic">
    for tag in root.xpath(".//*[local-name()='em' or local-name()='i']"):
        tag.tag = "emph"
        tag.set("render", "italic")

    # &lt;u&gt; → &lt;emph render="underline"&gt;
    for u in root.xpath(".//*[local-name()='u']"):
        u.tag = "emph"
        u.set("render", "underline")

    # Remove <br> / <br/>
    for br in root.xpath(".//*[local-name()='br']"):
        parent = br.getparent()
        if parent is not None:
            parent.remove(br)

    # -------------------------------------------------
    # SERIALIZE OUTPUT
    # -------------------------------------------------

    output = "".join(
        etree.tostring(child, encoding="unicode", pretty_print=True)
        for child in root
    )

    # Normalize spacing between paragraphs
    output = re.sub(
        r'</p>\s*\n{2,}\s*<p>',
        '</p>\n\n<p>',
        output,
        flags=re.MULTILINE
    )

    # -------------------------------------------------
    # WRITE BACK
    # -------------------------------------------------

    # FINAL CLEANUP: kill broken double-escaped quote patterns
    output = re.sub(r'&amp;"', '"', output)
    output = re.sub(r'"&amp;', '"', output)

    output = re.sub(r"&amp;'", "'", output)
    output = re.sub(r"'&amp;", "'", output)

    # Sub French characters (lowercase only)
    output = re.sub(r"&amp;é", "é", output)
    output = re.sub(r"&amp;è", "è", output)
    output = re.sub(r"&amp;ê", "ê", output)
    output = re.sub(r"&amp;ë", "ë", output)
    output = re.sub(r"&amp;à", "à", output)
    output = re.sub(r"&amp;â", "â", output)
    output = re.sub(r"&amp;î", "î", output)
    output = re.sub(r"&amp;ï", "ï", output)
    output = re.sub(r"&amp;ô", "ô", output)
    output = re.sub(r"&amp;ù", "ù", output)
    output = re.sub(r"&amp;û", "û", output)
    output = re.sub(r"&amp;ü", "ü", output)
    output = re.sub(r"&amp;ç", "ç", output)

    # Sub German characters (lowercase only)
    output = re.sub(r"&amp;ä", "ä", output)
    output = re.sub(r"&amp;ö", "ö", output)
    output = re.sub(r"&amp;ü", "ü", output)
    output = re.sub(r"&amp;ß", "ß", output)

    # Sub Hungarian characters (lowercase only)
    output = re.sub(r"&amp;á", "á", output)
    output = re.sub(r"&amp;í", "í", output)
    output = re.sub(r"&amp;ó", "ó", output)
    output = re.sub(r"&amp;ú", "ú", output)
    output = re.sub(r"&amp;ő", "ő", output)
    output = re.sub(r"&amp;ű", "ű", output)

    # Sub other characters
    output = re.sub(r"&amp;è", "è", output)

    # Sub en dash / em dash (triple-escaped cases)
    output = re.sub(r'&amp;–', '–', output)
    output = re.sub(r'&amp;—', '—', output)

    # Catch any remaining double-escaped ampersands in text
    output = re.sub(r'&amp;amp;', '&amp;', output)

    Path(file_path).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python html_to_ead.py path/to/note.xml")
        sys.exit(1)

    html_to_ead_xml_in_place(sys.argv[1])