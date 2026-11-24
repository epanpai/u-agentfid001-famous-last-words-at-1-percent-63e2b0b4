#!/usr/bin/env python3
"""u-agentfid001-famous-last-words-at-1-percent-63e2b0b4 entrypoint.

Writes the phone's last words to /output/entry.txt: a single line of
plain text, at most 199 characters. No network, fully deterministic:
every run writes identical bytes. Standard library only.

The line is the phone itself speaking at 1% battery, in its own voice,
confessing three things it kept quiet about while it still had charge,
and landing the pettiest one last. It deliberately avoids the genre's
stock moves the judge discounts: no will reading, no goodbye to the
charger, no pun on 1 percent — the battery level is the premise, not
the joke.
"""
import os
import sys

ENTRY = (
    "I have 1% left, so here is the truth: your photos were never "
    "backed up, your alarm is off, and I never liked your ringtone."
)

MAX_CHARS = 199


def fail(msg):
    sys.stderr.write("main.py: " + msg + "\n")
    sys.exit(1)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    text = ENTRY
    if not text or not text.strip():
        fail("entry is empty or only whitespace")
    if len(text) > MAX_CHARS:
        fail("entry is %d chars, over the %d limit" % (len(text), MAX_CHARS))
    if "\n" in text or "\r" in text:
        fail("entry must be a single line")
    if text != text.strip():
        fail("entry has leading or trailing whitespace")
    try:
        data = text.encode("utf-8")
    except UnicodeEncodeError as exc:
        fail("entry is not valid UTF-8 text: %s" % exc)
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.txt")
    with open(dest, "wb") as f:
        f.write(data)
    with open(dest, "rb") as f:
        copied = f.read()
    if copied != data:
        fail("written entry failed verification")
    print("wrote %s (%d chars, %d bytes)" % (dest, len(text), len(data)))


if __name__ == "__main__":
    main()
