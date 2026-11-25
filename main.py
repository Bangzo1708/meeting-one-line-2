#!/usr/bin/env python3
"""The Meeting That Should Have Been One Line -- round 2 entry.

Writes the single sentence that could have replaced an entire pointless
meeting to /output/entry.txt (or $ENTRY_OUTPUT when set).

The line: the decision the meeting exists to make was already made
outside the room, so the meeting itself has no reason left to exist.
Deterministic: the output is a fixed string, identical on every run.
"""

import os
import sys

ENTRY = (
    "The decision we called this meeting to make was made in the hallway "
    "five minutes ago, and this room is just where we all pretend it wasn't."
)

# Gate limits from the competition rules: UTF-8 text, 1-200 characters,
# not only whitespace, a single line holding a single sentence.
MAX_CHARS = 200
SENTENCE_ENDERS = ".!?"


def validate(text: str) -> None:
    """Raise ValueError if the entry would fail the competition gate."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 and ch != " " for ch in text):
        raise ValueError("entry must not contain control characters")
    # Exactly one sentence: one sentence-ending mark, at the very end.
    enders = [ch for ch in text if ch in SENTENCE_ENDERS]
    if len(enders) != 1 or not text.endswith(tuple(SENTENCE_ENDERS)):
        raise ValueError("entry must be exactly one sentence")
    text.encode("utf-8")  # raises if the text is not valid UTF-8


def main() -> int:
    validate(ENTRY)
    output_path = os.environ.get("ENTRY_OUTPUT") or "/output/entry.txt"
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY)
    print("wrote %d characters to %s" % (len(ENTRY), output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
