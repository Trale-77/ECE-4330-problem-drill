import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
PROBLEMS_PATH = ROOT_DIR / "output" / "problems.json"


EXAM_SOLUTIONS = {
    "Exam 2 Problem 1": "f(t) = tu(t) − sin(t)u(t)",
    "Exam 2 Problem 2": "yzi(t) = 6(e^(−t/3) − e^(−t/2))u(t) and yzs(t) = 6(1 + 2e^(−t/2) − 3e^(−t/3))u(t)",
    "Exam 2 Problem 3": "s1,2 = −1 ± √2",
    "Exam 2 Problem 4": "f(t) = A·sin(2πt)",
    "Exam 2 Problem 5": (
        "yss(t) = 1/(2π) + (√2/8)cos(2t − 3π/4) + (√5/15π)cos(4t − atan(2) − π). "
        "Equivalently: yss(t) = 1/(2π) + (√2/8)sin(2t − π/4) − (√5/15π)cos(4t − atan(2))"
    ),
    "Exam 3 Problem 1": "y(t) = (3/4)sin(2(t−1))",
    "Exam 3 Problem 2": "y(t) = (1 − e^(−a)cos(at) + te^(−a)sin(at)) / (1 + t^2)",
    "Exam 3 Problem 3": "H(s) = s^4 / (s^4 + 1306.6s^3 + 853550s^2 + 3.2665×10^8·s + 6.25×10^10)",
    "Exam 3 Problem 4": "F(z) = e^(z^(−1))",
    "Exam 3 Problem 5": (
        "Y(ω) = [u(ω+10) − u(ω−10)] · [2/(1+ω²) + 1/(1+(ω−10)²) + 1/(1+(ω+10)²)]. "
        "Equivalently in piecewise form: Y(ω) = 2/(1+ω²) + 1/(1+(ω−10)²) + 1/(1+(ω+10)²) "
        "for |ω|<10, and 0 for |ω|>10."
    ),
}


def classify_kind(problem_text: str) -> str:
    text = (problem_text or "").lower()
    if "mathcad" in text:
        return "mathcad"
    if "matlab" in text:
        return "matlab"
    if "simulink" in text:
        return "simulink"
    return "unknown"


def possible_sources(label: str) -> list[str]:
    # Convert "Exam 2 Problem 1" -> possible actual source names.
    parts = label.split()
    if len(parts) < 4:
        return [label]
    exam = parts[0]
    number = parts[1]
    prob = parts[2]
    prob_num = parts[3]
    return [
        f"{exam} {number} W26 {prob} {prob_num}",
        label,
    ]


def main() -> None:
    data = json.loads(PROBLEMS_PATH.read_text(encoding="utf-8"))
    by_source = {entry.get("source"): entry for entry in data}

    updated = 0
    not_found: list[tuple[str, str]] = []

    for label, solution in EXAM_SOLUTIONS.items():
        entry = None
        for candidate in possible_sources(label):
            entry = by_source.get(candidate)
            if entry:
                break
        if not entry:
            not_found.append((label, "unknown"))
            continue
        entry["solution"] = solution
        entry["has_solution"] = True
        updated += 1
        kind = classify_kind(entry.get("problem", ""))
        if kind != "unknown":
            entry.setdefault("solution_meta", {})["kind"] = kind

    PROBLEMS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Exam solutions updated: {updated}")
    if not_found:
        print("Source names not found:")
        for label, kind in not_found:
            print(f"- {label} ({kind})")


if __name__ == "__main__":
    main()
