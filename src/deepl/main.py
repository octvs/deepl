import argparse
import os
import re
import subprocess
import sys

import deepl


def side_by_side(strings, total_width, gap=4):
    w = (total_width - gap - 1) // 2
    separator = " " * (gap // 2) + "|" + " " * (gap // 2)
    result = []
    while any(strings):
        line = []
        for i, s in enumerate(strings):
            buf = s[:w]
            try:
                n = buf.index("\n")
                line.append(buf[:n].ljust(w))
                strings[i] = s[n + 1 :]
            except ValueError:
                line.append(buf.ljust(w))
                strings[i] = s[w:]
        result.append(separator.join(line))
    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--from",
        type=str,
        default="de",
        help="source language",
        dest="_from",
    )
    parser.add_argument(
        "-t",
        "--to",
        type=str,
        default="en",
        help="target language",
        dest="_to",
    )
    args = parser.parse_args()

    auth_key = re.search(
        "api: (.*)",
        subprocess.run(
            ["pass", "deepl"], capture_output=True, text=True
        ).stdout,
    ).group(1)
    translator = deepl.Translator(auth_key)
    input = sys.stdin.read()

    if args._to == "en":
        args._to += "-us"

    result = translator.translate_text(
        input,
        source_lang=args._from.capitalize(),
        target_lang=args._to.capitalize(),
    )
    try:
        width = os.get_terminal_size().columns
        if width > 100:
            print(side_by_side([input, result.text], width))
        else:
            print(input)
            print("-" * (width - 10))
            print(result.text)

    except OSError:
        print(result.text)


if __name__ == "__main__":
    main()
