import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
PROBLEMS_PATH = ROOT_DIR / "output" / "problems.json"

EXTRA_SOLUTIONS = {
    "Exam 2 W26 Problem 1": "f(t) = tu(t) − sin(t)u(t)",
    "Exam 3 W26 Problem 1": "y(t) = (3/4) sin(2(t−1))",
}


def main() -> None:
    data = json.loads(PROBLEMS_PATH.read_text(encoding="utf-8"))
    updated = 0
    removed = 0

    for entry in data:
        src = entry.get("source")
        if src in EXTRA_SOLUTIONS:
            entry["solution"] = EXTRA_SOLUTIONS[src]
            entry["has_solution"] = True
            updated += 1

    filtered = []
    for entry in data:
        if entry.get("has_solution"):
            filtered.append(entry)
        else:
            removed += 1

    PROBLEMS_PATH.write_text(json.dumps(filtered, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated with extra solutions: {updated}")
    print(f"Removed missing problems: {removed}")
    print(f"Remaining problems: {len(filtered)}")


if __name__ == "__main__":
    main()
