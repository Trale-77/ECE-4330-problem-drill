import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import fitz
import pytesseract
from PIL import Image

from insert_solutions import SOLUTIONS as MANUAL_SOLUTIONS


PROJECT_DIR = Path(__file__).resolve().parent.parent
HOMEBASE_DIR = PROJECT_DIR.parents[2]
SOURCE_DIR = HOMEBASE_DIR / "02 Projects" / "Schoolwork" / "Linear Material"
ASSIGNMENTS_DIR = SOURCE_DIR / "Assignments"
EXAMS_DIR = SOURCE_DIR / "Exams"
OUTPUT_DIR = PROJECT_DIR / "output"
IMAGES_DIR = OUTPUT_DIR / "problem_images"
OUTPUT_PATH = OUTPUT_DIR / "problems.json"
TESSERACT_PATH = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")

PROBLEM_START_RE = re.compile(r"^\s*(?:problem|prob\.?|question|q|p)?\s*(\d{1,2})[\.\):\-]\s*(.*)$", re.IGNORECASE)
NUMBER_ONLY_RE = re.compile(r"^\s*(\d{1,2})[\.\):\-]\s*(.*)$")
SOLUTION_LABEL_RE = re.compile(r"(?im)^solution\s*:\s*")

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

VISUAL_HINTS = [
    "following",
    "shown below",
    "below",
    "figure",
    "diagram",
    "plot",
    "graph",
    "circuit",
    "waveform",
    "block diagram",
    "system shown",
]

MANUAL_EXAM_SOLUTIONS = {
    "Exam 2 W26 Problem 1": "f(t) = tu(t) - sin(t)u(t)",
    "Exam 2 W26 Problem 2": "yzi(t) = 6(e^(-t/3) - e^(-t/2))u(t) and yzs(t) = 6(1 + 2e^(-t/2) - 3e^(-t/3))u(t)",
    "Exam 2 W26 Problem 3": "s1,2 = -1 ± sqrt(2)",
    "Exam 2 W26 Problem 4": "f(t) = A·sin(2πt)",
    "Exam 2 W26 Problem 5": "yss(t) = 1/(2π) + (sqrt(2)/8)cos(2t - 3π/4) + (sqrt(5)/(15π))cos(4t - atan(2) - π)",
    "Exam 3 W26 Problem 1": "y(t) = (3/4)sin(2(t-1))",
    "Exam 3 W26 Problem 2": "y(t) = (1 - e^(-a)cos(at) + te^(-a)sin(at)) / (1 + t^2)",
    "Exam 3 W26 Problem 3": "H(s) = s^4 / (s^4 + 1306.6s^3 + 853550s^2 + 3.2665×10^8·s + 6.25×10^10)",
    "Exam 3 W26 Problem 4": "F(z) = e^(z^(-1))",
    "Exam 3 W26 Problem 5": "Y(ω) = [u(ω+10) - u(ω-10)] · [2/(1+ω²) + 1/(1+(ω-10)²) + 1/(1+(ω+10)²)]",
}

MANUAL_PROBLEM_TEXT = {
    "Assignment 1 Problem 1": "1. The following numbers are irrational: ππ, ee, (√2)^(√2). However, in general, if we raise an irrational number to an irrational power we may get a rational number; give an example without using a calculator/computer.",
    "Assignment 1 Problem 10": "10. Starting from Euler's identity, e^(jθ) = cos(θ) + j sin(θ), show that cos(θ) = (1/2)[e^(jθ) + e^(-jθ)] and sin(θ) = (1/(2j))[e^(jθ) - e^(-jθ)].",
    "Assignment 1 Problem 11": "11. Show that e^(jx) - 1 = e^(jx/2) (e^(jx/2) - e^(-jx/2)) = 2j sin(x/2) e^(jx/2). Also, show that e^(jx) + 1 = e^(jx/2) (e^(jx/2) + e^(-jx/2)) = 2 cos(x/2) e^(jx/2).",
    "Assignment 2 Problem 11": "11. Evaluate t e^(-t) δ̇(t) = ?",
    "Assignment 5 Problem 8": "8. Let f(t) ↔ F(s). Show that: d/dt f(t) ↔ sF(s) - f(0-) [if Re(s) > 0].",
    "Final Sample Problem 2": "2. Consider the LTIC system H(s) = 1/(s^2 + 2). Determine yzs(t) if f(t) = u(t).",
    "Final Sample Problem 4": "4. Consider the system in P-3. Determine yss[k] if f(t) = 1 + 2 cos((10π/3)t). Assume Ts = 0.1. (You may use a calculator.)",
    "Test 1 Sample 1 Problem 4": "4. (15 points) Evaluate ∫_1^2 t^2 δ(2t - 3) dt.",
}

MANUAL_CLEAN_SOLUTION_SOURCES = {
    "Final Sample Problem 1",
    "Final Sample Problem 4",
    "Assignment 2 Problem 13",
    "Assignment 2 Problem 14",
    "Assignment 2 Problem 16",
    "Assignment 8 Problem 5",
    "Assignment 8 Problem 10",
    "Test 2 Sample 2 Problem 1",
}

MANUAL_DROP_SOURCES = {
    "Linear Exam 1 Review Problem 1",
    "Test 2 Sample Problem 1",
    "Test 3 Sample Problem 1",
}

if TESSERACT_PATH.exists():
    pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_PATH)


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


def canonical_source_key(value: str) -> str:
    return slugify(value.replace("problem", "p").replace("question", "p").replace("prob.", "p"))


def describe_problem_pdf(path: Path) -> str:
    stem = path.stem
    lower = stem.lower()

    if lower.startswith("ece4330assignment"):
        match = re.search(r"assignment(\d+)", lower)
        if match:
            return f"Assignment {int(match.group(1))}"
    if lower == "two_problems_ass5":
        return "Assignment 5 Extra"
    if lower.startswith("exam") and "w26" in lower:
        match = re.search(r"exam(\d+)", lower)
        if match:
            return f"Exam {int(match.group(1))} W26"
    if lower.startswith("test_"):
        match = re.search(r"test_(\d+)", lower)
        if match:
            sample_match = re.search(r"sample(\d+)$", lower)
            if sample_match:
                return f"Test {int(match.group(1))} Sample {int(sample_match.group(1))}"
            return f"Test {int(match.group(1))} Sample"
    if lower == "final_sample":
        return "Final Sample"
    if lower == "linearexam1review_gonnieben-tal":
        return "Linear Exam 1 Review"
    return stem.replace("_", " ")


def describe_solution_pdf(path: Path) -> str:
    lower = path.stem.lower()
    if lower.startswith("ece4330assignment"):
        match = re.search(r"assignment(\d+)", lower)
        if match:
            return f"Assignment {int(match.group(1))}"
    if lower.startswith("exam") and "w26" in lower:
        match = re.search(r"exam(\d+)", lower)
        if match:
            return f"Exam {int(match.group(1))} W26"
    if lower.startswith("test_") or lower.startswith("test"):
        match = re.search(r"test_?(\d+)", lower)
        if match:
            sample_match = re.search(r"sample(\d+)", lower)
            if sample_match and path.stem.lower().startswith("test_"):
                return f"Test {int(match.group(1))} Sample {int(sample_match.group(1))}"
            return f"Test {int(match.group(1))} Sample"
    if "final" in lower:
        return "Final Sample"
    return path.stem.replace("_", " ")


def read_page_lines(page: fitz.Page) -> List[dict]:
    lines: List[dict] = []
    data = page.get_text("dict")
    for block in data.get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            if not spans:
                continue
            text = "".join(span.get("text", "") for span in spans).strip()
            if not text:
                continue
            x0 = min(span["bbox"][0] for span in spans)
            y0 = min(span["bbox"][1] for span in spans)
            x1 = max(span["bbox"][2] for span in spans)
            y1 = max(span["bbox"][3] for span in spans)
            lines.append({"text": text, "x0": x0, "y0": y0, "x1": x1, "y1": y1})
    lines.sort(key=lambda item: (item["y0"], item["x0"]))
    return lines


def ocr_page(page: fitz.Page) -> str:
    pix = page.get_pixmap(dpi=220)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    try:
        return clean_text(pytesseract.image_to_string(img))
    except pytesseract.TesseractNotFoundError:
        return ""


def is_good_problem_start(line: dict, left_margin: float) -> Optional[Tuple[int, str]]:
    text = line["text"]
    if line["x0"] > left_margin + 18:
        return None
    match = PROBLEM_START_RE.match(text) or NUMBER_ONLY_RE.match(text)
    if not match:
        return None
    number = int(match.group(1))
    trailing = (match.group(2) or "").strip()
    letters = len(re.findall(r"[A-Za-z]", trailing))
    if not trailing:
        return number, trailing
    if letters >= 3 or len(trailing) >= 18:
        return number, trailing
    return None


def detect_segments(lines: List[dict]) -> List[Tuple[int, int, int]]:
    if not lines:
        return []
    left_margin = min(line["x0"] for line in lines if len(line["text"]) >= 2)
    starts: List[Tuple[int, int]] = []
    for idx, line in enumerate(lines):
        start = is_good_problem_start(line, left_margin)
        if start:
            number, _ = start
            starts.append((idx, number))

    if not starts:
        return []

    segments: List[Tuple[int, int, int]] = []
    for pos, (idx, number) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        segments.append((number, idx, end))
    return segments


def lines_to_text(lines: List[dict], start: int, end: int) -> str:
    return clean_text("\n".join(line["text"] for line in lines[start:end]))


def extract_problem_number(source: str) -> int:
    match = re.search(r"Problem\s+(\d+)", source, re.IGNORECASE)
    return int(match.group(1)) if match else 1


def classify_topic(problem_text: str) -> str:
    lowered = problem_text.lower()
    for topic, keywords in TOPIC_RULES:
        if any(keyword in lowered for keyword in keywords):
            return topic
    return "Signals/Math"


def word_fingerprint(text: str, max_chars: int = 600) -> set:
    normalized = text[:max_chars].lower()
    return set(re.findall(r"[a-z0-9]{2,}", normalized))


def content_similarity(text_a: str, text_b: str) -> float:
    a = word_fingerprint(text_a)
    b = word_fingerprint(text_b)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def doc_label_slug(label: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "", label)


def make_source(label: str, number: int) -> str:
    return f"{label} Problem {number}"


def save_embedded_images(doc: fitz.Document, page: fitz.Page, prefix: str, number: int, kind: str) -> List[str]:
    images: List[str] = []
    index = 0
    for img in page.get_images(full=True):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.width < 50 or pix.height < 50:
            pix = None
            continue
        if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        index += 1
        filename = f"{prefix}_{kind}{number}_img{index}.png"
        pix.save(IMAGES_DIR / filename)
        images.append(f"output/problem_images/{filename}")
        pix = None
    return images


def save_page_render(page: fitz.Page, prefix: str, number: int, kind: str) -> str:
    filename = f"{prefix}_{kind}{number}_page.png"
    out_path = IMAGES_DIR / filename
    pix = page.get_pixmap(dpi=180, alpha=False)
    pix.save(out_path)
    return f"output/problem_images/{filename}"


def page_has_visuals(page: fitz.Page) -> bool:
    return bool(page.get_images(full=True) or page.get_drawings())


def should_render_page(problem_text: str) -> bool:
    stripped = problem_text.strip()
    if not stripped:
        return True
    lowered = stripped.lower()
    return len(stripped) < 90 and any(term in lowered for term in VISUAL_HINTS)


def looks_bad_problem_text(problem_text: str) -> bool:
    text = problem_text.strip()
    if not text:
        return True
    if "|" in text:
        return True
    if any(bad in text for bad in ["ð", "â", "Ï", "Ì", "�"]):
        return True
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    short_lines = sum(1 for line in lines if len(line) <= 12)
    if len(lines) >= 4 and short_lines >= 3:
        return True
    if len(text) < 140 and sum(ch in text for ch in "=^_[]Σ∫δπω") >= 2:
        return True
    if re.search(r"[A-Za-z0-9]\n[\)\]\+\-\=/]", text):
        return True
    if re.search(r"[\(\[]\n[A-Za-z0-9]", text):
        return True
    return False


def save_problem_scan(page: fitz.Page, prefix: str, number: int, lines: List[dict], start: int, end: int) -> str:
    return save_segment_scan(page, prefix, number, lines, start, end, "Problem")


def looks_bad_solution_text(solution_text: str) -> bool:
    text = solution_text.strip()
    if not text:
        return True
    if "|" in text:
        return True
    if any(bad in text for bad in ["Ã°", "Ã¢", "Ã", "ÃŒ", "ï¿½"]):
        return True
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    short_lines = sum(1 for line in lines if len(line) <= 14)
    if len(lines) >= 5 and short_lines >= 3:
        return True
    if re.search(r"[A-Za-z0-9]\n[\)\]\+\-\=/]", text):
        return True
    if re.search(r"[\(\[]\n[A-Za-z0-9]", text):
        return True
    if len(text) < 180 and sum(ch in text for ch in "=^_[]Î£âˆ«Î´Ï€Ï‰") >= 3:
        return True
    return False


def save_segment_scan(
    page: fitz.Page, prefix: str, number: int, lines: List[dict], start: int, end: int, kind: str
) -> str:
    segment = lines[start:end]
    top = max(0, min(line["y0"] for line in segment) - 12)
    bottom = min(page.rect.height, max(line["y1"] for line in segment) + 18)
    clip = fitz.Rect(32, top, page.rect.width - 24, bottom)
    filename = f"{prefix}_{kind}{number}_scan.png"
    out_path = IMAGES_DIR / filename
    pix = page.get_pixmap(matrix=fitz.Matrix(2.6, 2.6), clip=clip, alpha=False)
    pix.save(out_path)
    return f"output/problem_images/{filename}"


def save_solution_scan(page: fitz.Page, prefix: str, number: int, lines: List[dict], start: int, end: int) -> str:
    return save_segment_scan(page, prefix, number, lines, start, end, "Solution")


def extract_problem_records(path: Path) -> List[dict]:
    label = describe_problem_pdf(path)
    prefix = doc_label_slug(label)
    doc = fitz.open(path)
    records: List[dict] = []
    current: Optional[dict] = None

    for page in doc:
        lines = read_page_lines(page)
        page_text = lines_to_text(lines, 0, len(lines)) if lines else ""
        segments = detect_segments(lines)

        if not page_text and page_has_visuals(page):
            page_text = ocr_page(page)

        if not segments:
            if current is None:
                current = {
                    "source": make_source(label, 1),
                    "problem": page_text,
                    "images": [],
                    "problem_scan": "",
                }
            else:
                if page_text:
                    current["problem"] = clean_text(f"{current['problem']}\n{page_text}")

            images = save_embedded_images(doc, page, prefix, extract_problem_number(current["source"]), "Problem")
            if not images and page_has_visuals(page) and should_render_page(current["problem"]):
                current["problem_scan"] = save_page_render(
                    page, prefix, extract_problem_number(current["source"]), "Problem"
                )
            elif not current.get("problem_scan"):
                current["problem_scan"] = save_page_render(
                    page, prefix, extract_problem_number(current["source"]), "Problem"
                )
            current["images"].extend(images)
            continue

        for pos, (number, start_idx, end_idx) in enumerate(segments):
            chunk = lines_to_text(lines, start_idx, end_idx)
            if current is not None and extract_problem_number(current["source"]) != number:
                records.append(current)
                current = None

            if current is None:
                current = {"source": make_source(label, number), "problem": chunk, "images": [], "problem_scan": ""}
            else:
                current["problem"] = clean_text(f"{current['problem']}\n{chunk}")

            images = save_embedded_images(doc, page, prefix, number, "Problem")
            if not current.get("problem_scan"):
                current["problem_scan"] = save_problem_scan(page, prefix, number, lines, start_idx, end_idx)
            current["images"].extend(images)

            if pos + 1 < len(segments):
                records.append(current)
                current = None

    if current is not None:
        records.append(current)

    doc.close()

    for record in records:
        record["problem"] = clean_text(record["problem"])
        record["images"] = sorted(set(record["images"]))
        record["problem_scan"] = record.get("problem_scan", "")

    return records


def extract_solution_segments(path: Path) -> Dict[str, dict]:
    label = describe_solution_pdf(path)
    prefix = doc_label_slug(label)
    doc = fitz.open(path)
    result: Dict[str, dict] = {}
    current_key: Optional[str] = None

    for page in doc:
        lines = read_page_lines(page)
        page_text = lines_to_text(lines, 0, len(lines)) if lines else ""
        segments = detect_segments(lines)
        if not page_text and page_has_visuals(page):
            page_text = ocr_page(page)

        if not segments:
            if current_key is None:
                continue
            if page_text:
                result[current_key]["solution"] = clean_text(f"{result[current_key]['solution']}\n{page_text}")
            number = extract_problem_number(result[current_key]["source"])
            images = save_embedded_images(doc, page, prefix, number, "Solution")
            if not images and page_has_visuals(page):
                images = [save_page_render(page, prefix, number, "Solution")]
            result[current_key]["solution_images"].extend(images)
            if not result[current_key].get("solution_scan"):
                result[current_key]["solution_scan"] = save_page_render(page, prefix, number, "Solution")
            continue

        for pos, (number, start_idx, end_idx) in enumerate(segments):
            chunk = lines_to_text(lines, start_idx, end_idx)
            source = make_source(label, number)
            key = canonical_source_key(source)
            if key not in result:
                result[key] = {
                    "source": source,
                    "solution": "",
                    "solution_images": [],
                    "solution_scan": "",
                    "solution_text_bad": False,
                }
            result[key]["solution"] = clean_text(f"{result[key]['solution']}\n{chunk}") if result[key]["solution"] else chunk
            images = save_embedded_images(doc, page, prefix, number, "Solution")
            if not images and page_has_visuals(page):
                images = [save_page_render(page, prefix, number, "Solution")]
            result[key]["solution_images"].extend(images)
            result[key]["solution_text_bad"] = looks_bad_solution_text(result[key]["solution"])
            if not result[key]["solution_scan"]:
                result[key]["solution_scan"] = save_solution_scan(page, prefix, number, lines, start_idx, end_idx)
            current_key = key
            if pos + 1 < len(segments):
                current_key = None

    doc.close()

    for item in result.values():
        item["solution"] = clean_text(item["solution"])
        item["solution_images"] = sorted(set(item["solution_images"]))
        item["solution_text_bad"] = looks_bad_solution_text(item["solution"])
        item["solution_scan"] = item.get("solution_scan", "")

    return result


def split_by_solution_label(text: str) -> List[str]:
    parts = SOLUTION_LABEL_RE.split(text)
    return [clean_text(part) for part in parts if clean_text(part)]


def extract_assignment_solution_chunks(path: Path) -> List[dict]:
    label = describe_solution_pdf(path)
    prefix = doc_label_slug(label)
    doc = fitz.open(path)
    chunks: List[dict] = []

    for page in doc:
        lines = read_page_lines(page)
        page_text = lines_to_text(lines, 0, len(lines)) if lines else ""
        if len(page_text) < 40:
            page_text = ocr_page(page)

        labeled_chunks = split_by_solution_label(page_text)
        if labeled_chunks:
            for chunk in labeled_chunks:
                number = len(chunks) + 1
                images = save_embedded_images(doc, page, prefix, number, "Solution")
                if not images and page_has_visuals(page):
                    images = [save_page_render(page, prefix, number, "Solution")]
                chunks.append(
                    {
                        "solution": chunk,
                        "solution_images": images,
                        "solution_scan": save_page_render(page, prefix, number, "Solution"),
                        "solution_text_bad": looks_bad_solution_text(chunk),
                    }
                )
            continue

        segments = detect_segments(lines)
        if segments:
            for number, start_idx, end_idx in segments:
                chunk = lines_to_text(lines, start_idx, end_idx)
                images = save_embedded_images(doc, page, prefix, number, "Solution")
                if not images and page_has_visuals(page):
                    images = [save_page_render(page, prefix, number, "Solution")]
                chunks.append(
                    {
                        "solution": chunk,
                        "solution_images": images,
                        "solution_scan": save_solution_scan(page, prefix, number, lines, start_idx, end_idx),
                        "solution_text_bad": looks_bad_solution_text(chunk),
                    }
                )
            continue

        if page_text or page_has_visuals(page):
            number = len(chunks) + 1
            images = save_embedded_images(doc, page, prefix, number, "Solution")
            if not images and page_has_visuals(page):
                images = [save_page_render(page, prefix, number, "Solution")]
            chunks.append(
                {
                    "solution": page_text,
                    "solution_images": images,
                    "solution_scan": save_page_render(page, prefix, number, "Solution"),
                    "solution_text_bad": looks_bad_solution_text(page_text),
                }
            )

    doc.close()
    for chunk in chunks:
        chunk["solution"] = clean_text(chunk["solution"])
        chunk["solution_images"] = sorted(set(chunk["solution_images"]))
        chunk["solution_text_bad"] = looks_bad_solution_text(chunk["solution"])
        chunk["solution_scan"] = chunk.get("solution_scan", "")
    return chunks


def merge_problem_only_records(records: List[dict]) -> List[dict]:
    grouped: Dict[str, List[dict]] = defaultdict(list)
    for record in records:
        grouped[record["source"]].append(record)

    merged: List[dict] = []
    for source, items in grouped.items():
        best_problem = max(items, key=lambda item: quality_score(item.get("problem", "")))
        topic_counts = Counter(classify_topic(item.get("problem", "")) for item in items)
        images: List[str] = []
        for item in items:
            images.extend(item.get("images") or [])
        merged.append(
            {
                "source": source,
                "topic": topic_counts.most_common(1)[0][0],
                "problem": clean_text(best_problem.get("problem", "")),
                "images": sorted(set(images)),
                "problem_scan": best_problem.get("problem_scan", ""),
                "problem_text_bad": best_problem.get("problem_text_bad", False),
            }
        )
    return sorted(merged, key=lambda item: item["source"])


def quality_score(text: str) -> int:
    stripped = text.strip()
    if not stripped:
        return 0
    letter_count = len(re.findall(r"[A-Za-z]", stripped))
    digit_count = len(re.findall(r"\d", stripped))
    return min(len(stripped), 2000) + (letter_count * 2) + digit_count


def merge_duplicate_records(records: List[dict]) -> List[dict]:
    grouped: Dict[str, List[dict]] = defaultdict(list)
    for record in records:
        grouped[record["source"]].append(record)

    merged: List[dict] = []
    for source, items in grouped.items():
        best_problem = max(items, key=lambda item: quality_score(item.get("problem", "")))
        best_solution = max(items, key=lambda item: quality_score(item.get("solution", "")))
        topic_counts = Counter(item.get("topic", "Signals/Math") for item in items)
        images: List[str] = []
        solution_images: List[str] = []
        for item in items:
            images.extend(item.get("images") or [])
            solution_images.extend(item.get("solution_images") or [])
        merged.append(
            {
                "source": source,
                "topic": topic_counts.most_common(1)[0][0],
                "problem": clean_text(best_problem.get("problem", "")),
                "has_solution": bool(clean_text(best_solution.get("solution", "")) or solution_images),
                "solution": clean_text(best_solution.get("solution", "")),
                "images": sorted(set(images)),
                "solution_images": sorted(set(solution_images)),
                "solution_scan": best_solution.get("solution_scan", ""),
                "solution_text_bad": best_solution.get("solution_text_bad", False),
                "problem_scan": best_problem.get("problem_scan", ""),
                "problem_text_bad": best_problem.get("problem_text_bad", False),
            }
        )
    return sorted(merged, key=lambda item: item["source"])


def apply_manual_solutions(records: List[dict]) -> None:
    combined = {}
    combined.update(MANUAL_SOLUTIONS)
    combined.update(MANUAL_EXAM_SOLUTIONS)
    for record in records:
        source = record["source"]
        if source in combined:
            record["solution"] = combined[source]
            record["has_solution"] = True


def apply_manual_problem_text(records: List[dict]) -> None:
    for record in records:
        source = record["source"]
        if source in MANUAL_PROBLEM_TEXT:
            record["problem"] = MANUAL_PROBLEM_TEXT[source]


def finalize_problem_text_flags(records: List[dict]) -> None:
    for record in records:
        if record.get("source") in MANUAL_PROBLEM_TEXT:
            record["problem_text_bad"] = False
        else:
            record["problem_text_bad"] = looks_bad_problem_text(record.get("problem", ""))


def finalize_solution_text_flags(records: List[dict]) -> None:
    for record in records:
        if record.get("source") in MANUAL_CLEAN_SOLUTION_SOURCES:
            record["solution_text_bad"] = False
        else:
            record["solution_text_bad"] = looks_bad_solution_text(record.get("solution", ""))
        record["solution_scan"] = record.get("solution_scan", "")


def remove_unusable_records(records: List[dict]) -> List[dict]:
    cleaned: List[dict] = []
    for record in records:
        if "Problem 0" in record["source"]:
            continue
        if record["source"] in MANUAL_DROP_SOURCES:
            continue
        cleaned.append(record)
    return cleaned


def collect_problem_pdfs() -> List[Path]:
    assignment_paths = sorted(
        path
        for path in ASSIGNMENTS_DIR.glob("*.pdf")
        if not path.name.startswith("._") and "solution" not in path.stem.lower()
    )
    exam_paths = sorted(
        path
        for path in EXAMS_DIR.glob("*.pdf")
        if not path.name.startswith("._") and "answer" not in path.stem.lower()
    )
    return assignment_paths + exam_paths


def collect_solution_pdfs() -> List[Path]:
    assignment_paths = sorted(
        path for path in ASSIGNMENTS_DIR.glob("*solution*.pdf") if not path.name.startswith("._")
    )
    exam_paths = sorted(
        path for path in EXAMS_DIR.glob("*answer*.pdf") if not path.name.startswith("._")
    )
    return assignment_paths + exam_paths


def attach_solutions(problem_records: List[dict], solution_records: Dict[str, dict]) -> List[dict]:
    attached: List[dict] = []
    for record in problem_records:
        key = canonical_source_key(record["source"])
        solution = solution_records.get(key, {})
        attached.append(
            {
                "source": record["source"],
                "topic": classify_topic(record["problem"]),
                "problem": record["problem"],
                "has_solution": bool(clean_text(solution.get("solution", "")) or solution.get("solution_images")),
                "solution": clean_text(solution.get("solution", "")),
                "images": sorted(set(record.get("images") or [])),
                "solution_images": sorted(set(solution.get("solution_images") or [])),
                "solution_scan": solution.get("solution_scan", ""),
                "solution_text_bad": solution.get("solution_text_bad", False),
                "problem_scan": record.get("problem_scan", ""),
                "problem_text_bad": record.get("problem_text_bad", False),
            }
        )
    return attached


def match_assignment_solutions(assignment_label: str, solution_chunks: List[dict], problems: List[dict]) -> Dict[str, dict]:
    matched: Dict[str, dict] = {}
    used_chunks: set = set()

    relevant = [item for item in problems if item["source"].startswith(f"{assignment_label} Problem ")]
    relevant = sorted(relevant, key=lambda item: extract_problem_number(item["source"]))

    for problem in relevant:
        best_score = 0.08
        best_idx = None
        for idx, chunk in enumerate(solution_chunks):
            if idx in used_chunks:
                continue
            score = content_similarity(problem["problem"], chunk["solution"])
            if score > best_score:
                best_score = score
                best_idx = idx
        if best_idx is not None:
            used_chunks.add(best_idx)
            matched[canonical_source_key(problem["source"])] = solution_chunks[best_idx]

    remaining_probs = [item for item in relevant if canonical_source_key(item["source"]) not in matched]
    remaining_chunks = [chunk for idx, chunk in enumerate(solution_chunks) if idx not in used_chunks]
    for problem, chunk in zip(remaining_probs, remaining_chunks):
        matched[canonical_source_key(problem["source"])] = chunk

    return matched


def summarize(records: List[dict]) -> None:
    duplicate_sources = [source for source, count in Counter(record["source"] for record in records).items() if count > 1]
    short_problems = [record["source"] for record in records if len(record["problem"].strip()) <= 40]
    no_solution = [record["source"] for record in records if not record["has_solution"]]
    no_images = [record["source"] for record in records if not record["images"]]
    suspicious = [
        record["source"]
        for record in records
        if not record["images"] and any(term in record["problem"].lower() for term in VISUAL_HINTS)
    ]

    print(f"Total records: {len(records)}")
    print(f"Duplicate sources remaining: {len(duplicate_sources)}")
    print(f"Short problems remaining: {len(short_problems)}")
    print(f"Missing solutions remaining: {len(no_solution)}")
    print(f"No problem images: {len(no_images)}")
    print(f"Suspicious no-image problems: {len(suspicious)}")
    if short_problems:
        print("Short problems:")
        for source in short_problems:
            print(f"  {source}")
    if no_solution:
        print("Missing solutions:")
        for source in no_solution:
            print(f"  {source}")
    if suspicious:
        print("Suspicious no-image:")
        for source in suspicious:
            print(f"  {source}")


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(exist_ok=True)

    problem_records: List[dict] = []
    for path in collect_problem_pdfs():
        problem_records.extend(extract_problem_records(path))

    merged_problems = merge_problem_only_records(problem_records)
    solution_records: Dict[str, dict] = {}
    assignment_solution_chunks: Dict[str, List[dict]] = defaultdict(list)
    for path in collect_solution_pdfs():
        if path.parent == ASSIGNMENTS_DIR and "assignment" in path.stem.lower():
            assignment_solution_chunks[describe_solution_pdf(path)].extend(extract_assignment_solution_chunks(path))
        else:
            solution_records.update(extract_solution_segments(path))

    for assignment_label, chunks in assignment_solution_chunks.items():
        solution_records.update(match_assignment_solutions(assignment_label, chunks, merged_problems))

    attached = attach_solutions(merged_problems, solution_records)
    merged = merge_duplicate_records(attached)
    apply_manual_solutions(merged)
    apply_manual_problem_text(merged)
    finalize_problem_text_flags(merged)
    finalize_solution_text_flags(merged)
    merged = remove_unusable_records(merged)
    OUTPUT_PATH.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    summarize(merged)


if __name__ == "__main__":
    main()
