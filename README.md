# README

These are some quick Python scripts made to accelerate the process of updating tagging of notes in ArchivesSpace finding aid from HTML to EAD3. They are fairly purpose-built and limited, but I'm putting them out into the world on the off chance they're useful for someone else.
Scripts were generated with assistance from Microsoft 365 Copilot (GPT‑5 chat model).

## Repository Files

### html_to_ead.py

The main conversion script. Takes HTML or HTML‑escaped text fragments and normalizes them into EAD‑friendly XML, handling common HTML tags and converting them to appropriate EAD markup. It also cleans messy character encodings (quotes, accented characters, dashes, ampersands).

### emph_render.py

Assigns render attributes to <emph> elements. Distinguishes between header‑style emphasis (entire paragraph emphasis → render="bold") and inline emphasis (everything else → render="italic").

### note.xml

Paste text into this file before running html_to_ead.py or emph_render.py. After processing, this same file is rewritten in place with the cleaned, EAD‑compatible XML output.

### cmds.txt

Shows the command‑line order for running html_to_ead.py and emph_render.py.
