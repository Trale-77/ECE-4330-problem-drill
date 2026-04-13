import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import fitz


TOPICS = [
    "ZIR/ZSR",
    "PFE",
    "Fourier Series",
    "Fourier Transform",
    "Butterworth",
    "Z-Transform",
    "Difference Equations",
    "Bilinear Transform",
    "Sampling/Nyquist",
    "Convolution",
    "Signals/Math",
]

ROOT_DIR = Path(__file__).resolve().parent.parent
PDF_DIRS = [ROOT_DIR / "Exams", ROOT_DIR / "Assignments"]
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_PATH = OUTPUT_DIR / "problems.json"
IMAGES_DIR = OUTPUT_DIR / "problem_images"

PROBLEM_START_RE = re.compile(
    r"(?im)^(?:\s*(?:problem|prob\.?|question|q)\s*(\d+)[\.\):\-]?|\s*p\s*(\d+)[\.\):\-]?|\s*(\d+)[\.\)])\s+"
)

SOLUTION_START_RE = re.compile(
    r"(?im)^(?:\s*(?:solution|sol\.?)\s*(\d+)[\.\):\-]?|\s*(?:problem|prob\.?|question|q)\s*(\d+)[\.\):\-]?|\s*p\s*(\d+)[\.\):\-]?|\s*(\d+)[\.\)])\s+"
)

TOPIC_RULES: List[Tuple[str, List[str]]] = [
    ("ZIR/ZSR", ["zero-input", "zero state", "zero-state", "yzi", "yzs", "initial condition"]),
    ("PFE", ["partial fraction", "inverse laplace", "transfer function", "h(s)"]),
    ("Fourier Series", ["fourier series", "periodic", "coefficients", "parseval"]),
    ("Fourier Transform", ["fourier transform", "f(ω)", "h(ω)", "brick-wall", "frequency response"]),
    ("Butterworth", ["butterworth", "magnitude", "filter design", "passband", "stopband"]),
    ("Z-Transform", ["z-transform", "z transform", "f(z)", "h(z)", "x(z)", "y(z)"]),
    ("Difference Equations", ["difference equation", "y[k]", "f[k]", "ltid", "y[n]", "x[n]"]),
    ("Bilinear Transform", ["bilinear", "sampling period", "ts", "tustin"]),
    ("Sampling/Nyquist", ["nyquist", "sampling", "aliasing", "reconstruction"]),
    ("Convolution", ["convolution", "impulse response", "h(t)"]),
]


def normalize_text(text: str) -> str:
    return (
        text.replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\xa0", " ")
    )


def clean_text(text: str) -> str:
    text = normalize_text(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def normalized_pdf_key(path: Path) -> str:
    name = path.stem.lower()
    name = re.sub(r"[_\-\s]*(solutions?|answers?)(?:[_\-\s]*sample)?(?:[_\-\s]*\d+)?$", "", name)
    return re.sub(r"[_\-\s]+", "", name)


def is_solution_pdf(path: Path) -> bool:
    name = path.stem.lower()
    return "solution" in name or "answer" in name


def describe_pdf(path: Path) -> str:
    stem = path.stem
    lower = stem.lower()

    if lower.startswith("ece4330assignment"):
        match = re.search(r"assignment(\d+)", stem, re.IGNORECASE)
        if match:
            return f"Assignment {int(match.group(1))}"
    if lower.startswith("exam") and "w26" in lower:
        match = re.search(r"exam(\d+)", stem, re.IGNORECASE)
        if match:
            return f"Exam {int(match.group(1))} W26"
    if lower.startswith("test_"):
        match = re.search(r"test_(\d+)", stem, re.IGNORECASE)
        if match:
            return f"Test {int(match.group(1))} Sample"
    if lower == "final_sample":
        return "Final Sample"
    if lower == "linearexam1review_gonnieben-tal":
        return "Linear Exam 1 Review"
    if lower == "two_problems_ass5":
        return "Assignment 5 Extra"
    return stem.replace("_", " ")


def extract_text(path: Path) -> str:
    doc = fitz.open(path)
    text = "\n\n".join(clean_text(page.get_text("text")) for page in doc)
    doc.close()
    return text.strip()


def collect_pdfs() -> List[Path]:
    paths: List[Path] = []
    for folder in PDF_DIRS:
        paths.extend(sorted(path for path in folder.glob("*.pdf") if not path.name.startswith("._")))
    return paths


def split_solution_sets(paths: List[Path]) -> Dict[str, List[Path]]:
    grouped: Dict[str, List[Path]] = {}
    for path in paths:
        if is_solution_pdf(path):
            grouped.setdefault(normalized_pdf_key(path), []).append(path)
    return grouped


def make_source(doc_label: str, number: int) -> str:
    return f"{doc_label} Problem {number}"


def extract_number(match: re.Match[str]) -> int:
    for group in match.groups():
        if group:
            return int(group)
    raise ValueError("Problem number missing")


def split_problems(text: str, doc_label: str, start_re: re.Pattern[str] = PROBLEM_START_RE) -> List[dict]:
    matches = list(start_re.finditer(text))
    problems: List[dict] = []

    if not matches:
        stripped = text.strip()
        problems.append(
            {
                "source": make_source(doc_label, 1),
                "problem": stripped,
            }
        )
        return problems

    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        chunk = text[start:end].strip()
        if not chunk:
            continue
        number = extract_number(match)
        problems.append(
            {
                "source": make_source(doc_label, number),
                "problem": chunk,
            }
        )
    return problems


def classify_topic(problem_text: str) -> str:
    lowered = problem_text.lower()
    for topic, keywords in TOPIC_RULES:
        if any(keyword in lowered for keyword in keywords):
            return topic
    return "Signals/Math"


def canonical_source_key(value: str) -> str:
    return slugify(value.replace("problem", "p").replace("question", "p").replace("prob.", "p"))


def doc_label_slug(label: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "", label)


def extract_problem_number(source: str) -> int:
    match = re.search(r"problem\s+(\d+)", source, re.IGNORECASE)
    return int(match.group(1)) if match else 1


def extract_images_for_page(
    doc: fitz.Document,
    page: fitz.Page,
    base_name: str,
    problem_number: int,
    image_counter: Dict[str, int],
) -> List[str]:
    images: List[str] = []
    per_problem_index = 0
    for img in page.get_images(full=True):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.width < 50 or pix.height < 50:
            pix = None
            continue
        if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        per_problem_index += 1
        image_counter["total"] += 1
        filename = f"{base_name}_Problem{problem_number}_img{per_problem_index}.png"
        out_path = IMAGES_DIR / filename
        pix.save(out_path)
        images.append(f"output/problem_images/{filename}")
        pix = None
    return images


def parse_problem_pdf(path: Path) -> Tuple[List[dict], int]:
    doc_label = describe_pdf(path)
    base_name = doc_label_slug(doc_label)
    doc = fitz.open(path)
    records: List[dict] = []
    image_counter = {"total": 0}

    for page in doc:
        page_text = clean_text(page.get_text("text"))
        page_records = split_problems(page_text, doc_label)
        # Ensure we still capture image-only pages
        if not page_records and (page_text or page.get_images(full=True)):
            page_records = [{"source": make_source(doc_label, 1), "problem": page_text}]

        # Extract images once per page and attach to each problem on that page
        for record in page_records:
            record["topic"] = classify_topic(record["problem"])
            record["images"] = []
            if page.get_images(full=True):
                problem_number = extract_problem_number(record["source"])
                record["images"] = extract_images_for_page(doc, page, base_name, problem_number, image_counter)
            records.append(record)

    doc.close()
    return records, image_counter["total"]


def parse_solution_pdf(path: Path) -> Dict[str, str]:
    doc_label = describe_pdf(path)
    text = extract_text(path)
    records = split_problems(text, doc_label, SOLUTION_START_RE)
    return {canonical_source_key(record["source"]): record["problem"] for record in records}


def find_matching_solution_pdf(problem_pdf: Path, candidates: List[Path]) -> List[Path]:
    base_key = normalized_pdf_key(problem_pdf)
    same_folder = [p for p in candidates if p.parent == problem_pdf.parent and is_solution_pdf(p)]
    exact = [p for p in same_folder if normalized_pdf_key(p) == base_key]
    return exact


def attach_solutions(problems: List[dict], solution_maps: List[Dict[str, str]]) -> List[dict]:
    merged_solutions: Dict[str, str] = {}
    for solution_map in solution_maps:
        merged_solutions.update(solution_map)

    result: List[dict] = []
    for problem in problems:
        solution = merged_solutions.get(canonical_source_key(problem["source"]))
        result.append(
            {
                "source": problem["source"],
                "topic": problem["topic"],
                "problem": problem["problem"],
                "has_solution": solution is not None,
                "solution": solution,
                "images": problem.get("images", []),
            }
        )
    return result


def main() -> None:
    pdf_paths = collect_pdfs()
    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)
    total_images = 0
    image_heavy_topics = Counter()
    all_records: List[dict] = []
    for path in pdf_paths:
        if is_solution_pdf(path):
            continue
        problems, image_count = parse_problem_pdf(path)
        total_images += image_count
        solution_paths = find_matching_solution_pdf(path, pdf_paths)
        solutions = [parse_solution_pdf(solution_path) for solution_path in solution_paths]
        all_records.extend(attach_solutions(problems, solutions))

    OUTPUT_PATH.write_text(json.dumps(all_records, indent=2, ensure_ascii=False), encoding="utf-8")

    counts = Counter(record["topic"] for record in all_records)
    for record in all_records:
        if record.get("images"):
            image_heavy_topics[record["topic"]] += 1
    print(f"Wrote {len(all_records)} problems to {OUTPUT_PATH}")
    for topic in TOPICS:
      print(f"{topic}: {counts.get(topic, 0)}")
    print(f"Total images extracted: {total_images}")
    if image_heavy_topics:
        top_topics = ", ".join([f"{topic} ({count})" for topic, count in image_heavy_topics.most_common(3)])
        print(f"Most image-heavy topics: {top_topics}")


if __name__ == "__main__":
    main()
