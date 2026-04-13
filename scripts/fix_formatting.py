import json
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
PROBLEMS_PATH = ROOT_DIR / "output" / "problems.json"


GREEK_MAP = {
    "omega": "ω",
    "delta": "δ",
}

EXPO_VARS = r"[a-zA-Z]|ω|δ"


def fix_greek(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        word = match.group(0).lower()
        return GREEK_MAP.get(word, match.group(0))

    return re.sub(r"\b(omega|delta)\b", repl, text, flags=re.IGNORECASE)


def fix_w_frequency(text: str) -> str:
    # Replace standalone w with ω when it appears as a frequency symbol
    return re.sub(r"\b[wW]\b", "ω", text)


def fix_exponentials(text: str) -> str:
    # Ensure patterns like 4e-t, e-2t, 2e3t -> 4e^(-t), e^(-2t), 2e^(3t)
    def repl(match: re.Match[str]) -> str:
        coeff = match.group("coeff") or ""
        sign = match.group("sign")
        body = match.group("body")
        return f"{coeff}e^({sign}{body})"

    pattern = re.compile(
        rf"(?<!\w)(?P<coeff>\d+)?e(?P<sign>[+-])(?P<body>(?:\d+)?(?:{EXPO_VARS})(?:\d+)?)",
        flags=re.IGNORECASE,
    )
    return pattern.sub(repl, text)


def fix_variable_powers(text: str) -> str:
    # s2 -> s^2, t2 -> t^2, w2 -> ω^2 after omega replacement
    def repl(match: re.Match[str]) -> str:
        var = match.group("var")
        power = match.group("pow")
        return f"{var}^{power}"

    pattern = re.compile(rf"(?<!\^)\b(?P<var>[stωδ])(?P<pow>\d+)\b", flags=re.IGNORECASE)
    return pattern.sub(repl, text)


def fix_general_superscripts(text: str) -> str:
    # Best-effort: x2 -> x^2 for single-letter variables (avoid numbers or words)
    def repl(match: re.Match[str]) -> str:
        var = match.group("var")
        power = match.group("pow")
        return f"{var}^{power}"

    pattern = re.compile(rf"(?<!\^)\b(?P<var>[a-zA-Zωδ])(?P<pow>[2-9])\b")
    return pattern.sub(repl, text)


def apply_fixes(text: str) -> str:
    if not text:
        return text
    original = text
    text = fix_greek(text)
    text = fix_w_frequency(text)
    text = fix_exponentials(text)
    text = fix_variable_powers(text)
    text = fix_general_superscripts(text)
    return text if text != original else original


def main() -> None:
    data = json.loads(PROBLEMS_PATH.read_text(encoding="utf-8"))
    modified_fields = 0

    for entry in data:
        for field in ("problem", "solution"):
            if entry.get(field) is None:
                continue
            updated = apply_fixes(entry[field])
            if updated != entry[field]:
                entry[field] = updated
                modified_fields += 1

    PROBLEMS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Modified fields: {modified_fields}")


if __name__ == "__main__":
    main()
