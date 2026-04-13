import json
import os
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Dict, List

import fitz
import pytesseract
from PIL import Image


ROOT_DIR = Path(__file__).resolve().parent.parent
ASSIGNMENTS_DIR = ROOT_DIR / "Assignments"
EXAMS_DIR = ROOT_DIR / "Exams"
OUTPUT_DIR = ROOT_DIR / "output"
IMAGES_DIR = OUTPUT_DIR / "problem_images"
PROBLEMS_PATH = OUTPUT_DIR / "problems.json"
TESSERACT_PATH = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

SOLUTION_START_RE = re.compile(
    r"(?im)^(?:\s*(?:solution|sol\.?)\s*([0-9]+)[\.\):\-]?"
    r"|\s*(?:problem|prob\.?|question|q)\s*([0-9]+)[\.\):\-]?"
    r"|\s*p\s*([0-9]+)[\.\):\-]?"
    r"|\s*([0-9]+)[\.\)])\s+(?=\S)"
)

LECTURE_ITEM_RE = re.compile(r"(?m)^([0-9]+)\.\s+(?=\S)")
SOLUTION_LABEL_RE = re.compile(r"(?im)^solution\s*:\s*")


def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFKD", text)


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


def ocr_page(page: fitz.Page) -> str:
    pix = page.get_pixmap(dpi=200)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return pytesseract.image_to_string(img)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def canonical_source_key(value: str) -> str:
    return slugify(value.replace("problem", "p").replace("question", "p").replace("prob.", "p"))


def is_solution_pdf(path: Path) -> bool:
    name = path.stem.lower()
    return "solution" in name or "answer" in name


def describe_pdf(path: Path) -> str:
    stem = path.stem
    lower = stem.lower()

    if lower.startswith("test") and "answer" in lower:
        match = re.search(r"test_?([0-9]+)", stem, re.IGNORECASE)
        if match:
            return f"Test {int(match.group(1))} Sample"
    if lower.startswith("ece4330assignment"):
        match = re.search(r"assignment([0-9]+)", stem, re.IGNORECASE)
        if match:
            return f"Assignment {int(match.group(1))}"
    if lower.startswith("exam") and "w26" in lower:
        match = re.search(r"exam([0-9]+)", stem, re.IGNORECASE)
        if match:
            return f"Exam {int(match.group(1))} W26"
    if lower.startswith("test_"):
        match = re.search(r"test_([0-9]+)", stem, re.IGNORECASE)
        if match:
            sample_n = re.search(r"sample([0-9]+)", stem, re.IGNORECASE)
            if sample_n:
                return f"Test {int(match.group(1))} Sample {int(sample_n.group(1))}"
            return f"Test {int(match.group(1))} Sample"
    if lower == "final_sample":
        return "Final Sample"
    if "final" in lower and "answer" in lower:
        return "Final Sample"
    if lower == "linearexam1review_gonnieben-tal":
        return "Linear Exam 1 Review"
    if lower == "two_problems_ass5":
        return "Assignment 5 Extra"
    return stem.replace("_", " ")


def extract_number(match: re.Match[str]) -> int:
    for group in match.groups():
        if group:
            return int(group)
    raise ValueError("Missing number")


def extract_images_for_page(
    doc: fitz.Document,
    page: fitz.Page,
    base_name: str,
    solution_number: int,
    image_counter: Dict[str, int],
) -> List[str]:
    images: List[str] = []
    per_solution_index = 0
    for img in page.get_images(full=True):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.width < 50 or pix.height < 50:
            pix = None
            continue
        if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        per_solution_index += 1
        image_counter["total"] += 1
        filename = f"{base_name}_Solution{solution_number}_img{per_solution_index}.png"
        pix.save(IMAGES_DIR / filename)
        images.append(f"output/problem_images/{filename}")
        pix = None
    return images


def word_fingerprint(text: str, max_chars: int = 600) -> set:
    normalized = normalize_unicode(text[:max_chars]).lower()
    return set(re.findall(r"[a-z0-9]{2,}", normalized))


def content_similarity(text_a: str, text_b: str) -> float:
    a = word_fingerprint(text_a)
    b = word_fingerprint(text_b)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def collect_solution_pdfs() -> List[Path]:
    assignment_solutions = [
        p for p in ASSIGNMENTS_DIR.glob("*.pdf")
        if is_solution_pdf(p) and not p.name.startswith("._")
    ]
    exam_solutions = [
        p for p in EXAMS_DIR.glob("*.pdf")
        if is_solution_pdf(p) and not p.name.startswith("._")
    ]
    root_solutions = [
        p for p in BASE_DIR.glob("*.pdf")
        if is_solution_pdf(p) and not p.name.startswith("._")
    ]
    return sorted(assignment_solutions + exam_solutions + root_solutions)


def split_by_solution_label(text: str) -> List[str]:
    parts = SOLUTION_LABEL_RE.split(text)
    return [p.strip() for p in parts if len(p.strip()) >= 20]


def extract_exam_solutions(path: Path) -> Dict[str, dict]:
    doc_label = describe_pdf(path)
    base_name = re.sub(r"[^a-zA-Z0-9]+", "", doc_label)
    doc = fitz.open(path)
    image_counter = {"total": 0}

    solution_map: Dict[str, dict] = {}
    current_number: int | None = None

    for page in doc:
        page_text = clean_text(page.get_text("text"))
        if len(page_text) < 40:
            page_text = clean_text(ocr_page(page))
        matches = list(SOLUTION_START_RE.finditer(page_text))
        if matches:
            for idx, match in enumerate(matches):
                start = match.start()
                end = matches[idx + 1].start() if idx + 1 < len(matches) else len(page_text)
                chunk = page_text[start:end].strip()
                if not chunk:
                    continue
                current_number = extract_number(match)
                key = canonical_source_key(f"{doc_label} Problem {current_number}")
                if key not in solution_map:
                    solution_map[key] = {"solution_text": "", "images": []}
                if chunk:
                    solution_map[key]["solution_text"] += ("\n" + chunk) if solution_map[key]["solution_text"] else chunk
                if page.get_images(full=True):
                    solution_map[key]["images"].extend(
                        extract_images_for_page(doc, page, base_name, current_number, image_counter)
                    )
        else:
            if current_number is not None:
                key = canonical_source_key(f"{doc_label} Problem {current_number}")
                if key not in solution_map:
                    solution_map[key] = {"solution_text": "", "images": []}
                if page_text:
                    solution_map[key]["solution_text"] += ("\n" + page_text) if solution_map[key]["solution_text"] else page_text
                if page.get_images(full=True):
                    solution_map[key]["images"].extend(
                        extract_images_for_page(doc, page, base_name, current_number, image_counter)
                    )

    doc.close()
    return solution_map


def extract_assignment_solutions(path: Path) -> List[dict]:
    base_name = re.sub(r"[^a-zA-Z0-9]+", "", describe_pdf(path))
    doc = fitz.open(path)
    image_counter = {"total": 0}

    chunks: List[dict] = []
    for page in doc:
        page_text = clean_text(page.get_text("text"))
        if len(page_text) < 40:
            page_text = clean_text(ocr_page(page))
        label_chunks = split_by_solution_label(page_text)
        if label_chunks:
            for chunk in label_chunks:
                chunks.append(
                    {
                        "solution_text": chunk,
                        "images": extract_images_for_page(
                            doc, page, base_name, len(chunks) + 1, image_counter
                        )
                        if page.get_images(full=True)
                        else [],
                    }
                )
            continue

        matches = list(LECTURE_ITEM_RE.finditer(page_text))
        if matches:
            for idx, match in enumerate(matches):
                start = match.start()
                end = matches[idx + 1].start() if idx + 1 < len(matches) else len(page_text)
                chunk = page_text[start:end].strip()
                if len(chunk) < 20:
                    continue
                chunks.append(
                    {
                        "solution_text": chunk,
                        "images": extract_images_for_page(
                            doc, page, base_name, len(chunks) + 1, image_counter
                        )
                        if page.get_images(full=True)
                        else [],
                    }
                )
        else:
            if page_text:
                chunks.append(
                    {
                        "solution_text": page_text,
                        "images": extract_images_for_page(
                            doc, page, base_name, len(chunks) + 1, image_counter
                        )
                        if page.get_images(full=True)
                        else [],
                    }
                )
            elif page.get_images(full=True):
                chunks.append(
                    {
                        "solution_text": "",
                        "images": extract_images_for_page(
                            doc, page, base_name, len(chunks) + 1, image_counter
                        ),
                    }
                )

    doc.close()
    return chunks


def match_assignment_solutions(
    assignment_label: str,
    solution_chunks: List[dict],
    problems: List[dict],
    threshold: float = 0.08,
) -> Dict[str, dict]:
    matched: Dict[str, dict] = {}
    used_chunks: set = set()

    relevant = [p for p in problems if p.get("source", "").startswith(assignment_label + " Problem")]
    relevant = sorted(
        relevant,
        key=lambda d: int(re.search(r"problem\s+(\d+)", d["source"], re.IGNORECASE).group(1)),
    )

    for prob in relevant:
        best_score = threshold
        best_idx = None
        for i, chunk in enumerate(solution_chunks):
            if i in used_chunks:
                continue
            score = content_similarity(prob["problem"], chunk["solution_text"])
            if score > best_score:
                best_score = score
                best_idx = i
        if best_idx is not None:
            used_chunks.add(best_idx)
            matched[canonical_source_key(prob["source"])] = solution_chunks[best_idx]

    remaining_probs = [p for p in relevant if canonical_source_key(p["source"]) not in matched]
    remaining_chunks = [c for i, c in enumerate(solution_chunks) if i not in used_chunks]
    for prob, chunk in zip(remaining_probs, remaining_chunks):
        matched[canonical_source_key(prob["source"])] = chunk

    return matched


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)
    if TESSERACT_PATH.exists():
        pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_PATH)
    data = json.loads(PROBLEMS_PATH.read_text(encoding="utf-8"))
    solution_pdfs = collect_solution_pdfs()

    solution_map: Dict[str, dict] = {}
    assignment_chunks: Dict[str, List[dict]] = {}

    for path in solution_pdfs:
        if path.parent == ASSIGNMENTS_DIR and "assignment" in path.stem.lower():
            assignment_label = describe_pdf(path)
            assignment_chunks[assignment_label] = extract_assignment_solutions(path)
        else:
            solution_map.update(extract_exam_solutions(path))

    for assignment_label, chunks in assignment_chunks.items():
        solution_map.update(match_assignment_solutions(assignment_label, chunks, data))

    solved_count = 0
    solved_with_images = 0
    missing_sources: List[str] = []
    per_topic_solved: Counter = Counter()
    per_topic_total: Counter = Counter()

    for entry in data:
        per_topic_total[entry["topic"]] += 1
        key = canonical_source_key(entry["source"])
        has_text = bool(solution_map.get(key, {}).get("solution_text"))
        has_images = bool(solution_map.get(key, {}).get("images"))
        if key in solution_map and (has_text or has_images):
            entry["solution"] = solution_map[key]["solution_text"]
            entry["solution_images"] = solution_map[key].get("images", [])
            entry["has_solution"] = True
            solved_count += 1
            per_topic_solved[entry["topic"]] += 1
            if entry["solution_images"]:
                solved_with_images += 1
        else:
            entry["has_solution"] = False
            entry["solution_images"] = entry.get("solution_images", [])
            missing_sources.append(entry["source"])

    PROBLEMS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    total = len(data)
    print(f"Total problems: {total}")
    print(f"With solution text: {solved_count}")
    print(f"With solution images: {solved_with_images}")
    print(f"Missing solutions: {total - solved_count}")
    if missing_sources:
        print("Missing sources:")
        for source in sorted(set(missing_sources)):
            print(f"- {source}")
    print("By topic:")
    for topic in sorted(per_topic_total.keys()):
        solved = per_topic_solved.get(topic, 0)
        total_topic = per_topic_total[topic]
        print(f"- {topic}: {solved} solved / {total_topic} total")


if __name__ == "__main__":
    main()
