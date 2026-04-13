import json
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
PROBLEMS_PATH = ROOT_DIR / "output" / "problems.json"

SENTENCE_END_RE = re.compile(r"[.!?;:]$")
MATH_START_RE = re.compile(r"^[\d\w\(\[\+\-=/^.,]|^ω|^δ", re.IGNORECASE)
ORPHAN_RE = re.compile(r"^[\d\w]$|^\d+$")
SHORT_MATH_TOKEN_RE = re.compile(r"^[\dA-Za-z\(\)\[\]=+\-/*·•,]+$|^Ï‰$|^Î´$", re.IGNORECASE)
SYMBOL_ONLY_RE = re.compile(r"^[•·]+$")


def clean_spaces(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def join_fraction_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if (
            i + 1 < len(lines)
            and line.isdigit()
            and lines[i + 1].strip().isdigit()
            and out
            and out[-1].strip()
            and out[-1].strip()[-1] not in ".!?:;"
        ):
            out[-1] = f"{out[-1].rstrip()} {line}/{lines[i + 1].strip()}"
            i += 2
            continue
        out.append(line)
        i += 1
    return out


def should_join(prev_line: str, next_line: str) -> bool:
    if not prev_line or not next_line:
        return False
    if SENTENCE_END_RE.search(prev_line.strip()):
        return False
    if MATH_START_RE.search(next_line.strip()):
        return True
    return False


def collapse_vertical_math(lines: list[str]) -> list[str]:
    collapsed: list[str] = []
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        if buffer:
            collapsed.append(" ".join(buffer))
            buffer = []

    for line in lines:
        token = line.strip()
        if token and len(token) <= 3 and SHORT_MATH_TOKEN_RE.match(token):
            buffer.append(token)
            continue
        flush()
        collapsed.append(line)

    flush()
    return collapsed


def merge_split_word(prev_line: str, next_line: str) -> str | None:
    if len(prev_line.strip()) == 1 and prev_line.strip().isalpha() and next_line and next_line[0].isalpha():
        return f"{prev_line.strip()}{next_line.lstrip()}"
    return None


def fix_linebreaks(text: str) -> str:
    if not text:
        return text

    lines = [line.strip() for line in text.splitlines() if line.strip()]

    cleaned_lines: list[str] = []
    for line in lines:
        line = line.replace("", "").replace("•", "").replace("·", "")
        line = (
            line.replace("", "+")
            .replace("", "=")
            .replace("", "-")
            .replace("", ">=")
            .replace("", "<=")
        )
        if re.fullmatch(r"\(?\s*shown\s+below\s*\)?", line, flags=re.IGNORECASE):
            continue
        compact = line.replace(" ", "")
        if SYMBOL_ONLY_RE.fullmatch(compact) or (len(compact) <= 2 and not any(ch.isalnum() for ch in compact)):
            continue
        cleaned_lines.append(line)

    cleaned_lines = join_fraction_lines(cleaned_lines)
    cleaned_lines = collapse_vertical_math(cleaned_lines)

    merged: list[str] = []
    i = 0
    while i < len(cleaned_lines):
        line = cleaned_lines[i]
        if i + 1 < len(cleaned_lines):
            merged_word = merge_split_word(line, cleaned_lines[i + 1])
            if merged_word:
                line = merged_word
                i += 2
                if merged and not SENTENCE_END_RE.search(merged[-1].strip()):
                    merged[-1] = f"{merged[-1]} {line}"
                else:
                    merged.append(line)
                continue
        if i + 1 < len(cleaned_lines) and should_join(line, cleaned_lines[i + 1]):
            joiner = "" if line.endswith("-") else " "
            line = f"{line.rstrip('-')}{joiner}{cleaned_lines[i + 1].lstrip()}"
            i += 2
            # Keep merging while the rule continues to match
            while i < len(cleaned_lines) and should_join(line, cleaned_lines[i]):
                joiner = "" if line.endswith("-") else " "
                line = f"{line.rstrip('-')}{joiner}{cleaned_lines[i].lstrip()}"
                i += 1
            merged.append(line)
            continue

        # Orphaned single digit/variable line: attach to previous line if it looks like math continuation
        if merged and ORPHAN_RE.match(line) and not SENTENCE_END_RE.search(merged[-1].strip()):
            merged[-1] = f"{merged[-1]} {line}"
        else:
            merged.append(line)
        i += 1

    return clean_spaces("\n".join(merged))


def main() -> None:
    data = json.loads(PROBLEMS_PATH.read_text(encoding="utf-8"))
    modified_fields = 0

    for entry in data:
        for field in ("problem", "solution"):
            value = entry.get(field)
            if value is None:
                continue
            updated = fix_linebreaks(value)
            if updated != value:
                entry[field] = updated
                modified_fields += 1

    PROBLEMS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Modified fields: {modified_fields}")


if __name__ == "__main__":
    main()
