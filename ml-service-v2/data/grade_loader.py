"""
Real Grade Data Loader

Loads student grade CSV files and converts letter grades to numeric scores.
Used to calibrate ML training with real Cambodian student data.

Grade ranges (percentage of max score):
    A: 90-100%
    B: 80-89%
    C: 70-79%
    D: 60-69%
    E: 50-59%
    F: 0-49%
"""
import csv
import logging
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

CSV_DIR = Path(__file__).parent / "csv"

# Letter grade → percentage range (of max score)
GRADE_RANGES: Dict[str, Tuple[float, float]] = {
    "A": (0.90, 1.00),
    "B": (0.80, 0.89),
    "C": (0.70, 0.79),
    "D": (0.60, 0.69),
    "E": (0.50, 0.59),
    "F": (0.00, 0.49),
}

# Subject max scores (real Cambodian exam values)
MAX_SCORES = {
    "math": 125, "physics": 75, "chemistry": 75, "biology": 75,
    "english": 50, "khmer": 75, "history": 50,
}

# Map CSV column names (lowercase) to system subject names
COLUMN_MAP = {
    "khmer": "khmer",
    "math": "math",
    "biology": "biology",
    "history": "history",
    "chemistry": "chemistry",
    "physics": "physics",
    "english": "english",
}


def letter_to_percentage(letter: str, randomize: bool = True) -> float:
    """Convert a letter grade to a percentage (0.0–1.0)."""
    grade_range = GRADE_RANGES.get(letter.strip().upper())
    if grade_range is None:
        return 0.0
    low, high = grade_range
    if randomize:
        return float(np.random.uniform(low, high))
    return (low + high) / 2.0


def letter_to_score(letter: str, subject: str, randomize: bool = True) -> float:
    """Convert a letter grade to an actual numeric score for a subject."""
    pct = letter_to_percentage(letter, randomize)
    max_score = MAX_SCORES.get(subject.lower(), 100)
    return round(pct * max_score, 1)


def load_csv(filepath: Optional[Path] = None) -> List[Dict[str, str]]:
    """
    Load a grade CSV and return cleaned rows.
    Automatically removes duplicate header rows scattered in the file.
    """
    if filepath is None:
        filepath = CSV_DIR / "science-grades.csv"
    if not filepath.exists():
        logger.warning(f"CSV not found: {filepath}")
        return []

    rows = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        header_cols = {c.strip() for c in (reader.fieldnames or [])}

        for row in reader:
            # Skip duplicate header rows (value matches a column name)
            first_val = next(iter(row.values()), "").strip()
            if first_val in header_cols:
                continue
            rows.append(row)

    logger.info(f"Loaded {len(rows)} student records from {filepath.name}")
    return rows


def load_all_csvs() -> List[Dict[str, str]]:
    """Load all CSV files from the csv directory."""
    all_rows: List[Dict[str, str]] = []
    if not CSV_DIR.exists():
        return all_rows
    csv_files = sorted(CSV_DIR.glob("*.csv"))
    for csv_file in csv_files:
        all_rows.extend(load_csv(csv_file))
    logger.info(
        f"Total: {len(all_rows)} student records from {len(csv_files)} file(s)"
    )
    return all_rows


def convert_row_to_grades(
    row: Dict[str, str], randomize: bool = True
) -> Dict[str, float]:
    """
    Convert a CSV row of letter grades to numeric scores.
    Returns dict like: {"math": 112.5, "physics": 67.5, ...}
    """
    grades: Dict[str, float] = {}
    for key, value in row.items():
        col = key.strip().lower()
        subject = COLUMN_MAP.get(col)
        if subject is None:
            continue  # skip Result or unknown columns
        letter = value.strip().upper()
        if letter in GRADE_RANGES:
            grades[subject] = letter_to_score(letter, subject, randomize)
        else:
            grades[subject] = 0.0
    return grades


def get_real_grade_distributions() -> Dict[str, Tuple[float, float]]:
    """
    Compute actual mean and std for each subject from all CSV data.
    Returns normalised (0–1) distributions per subject.

    These replace the hardcoded (mean, std) values in the training pipeline.
    """
    rows = load_all_csvs()
    if not rows:
        return {}

    # Collect normalised scores per subject (using midpoint for consistency)
    subject_scores: Dict[str, List[float]] = {s: [] for s in MAX_SCORES}

    for row in rows:
        grades = convert_row_to_grades(row, randomize=False)
        for subject, score in grades.items():
            if score > 0:
                normalised = score / MAX_SCORES[subject]
                subject_scores[subject].append(normalised)

    distributions: Dict[str, Tuple[float, float]] = {}
    for subject, scores in subject_scores.items():
        if scores:
            distributions[subject] = (
                float(np.mean(scores)),
                float(np.std(scores)),
            )
        else:
            distributions[subject] = (0.50, 0.15)

    logger.info("Real grade distributions (normalised 0-1):")
    for s, (m, sd) in sorted(distributions.items()):
        logger.info(f"  {s:12s}: mean={m:.3f}  std={sd:.3f}")

    return distributions


def get_real_students_augmented(n_copies: int = 20) -> List[Dict[str, float]]:
    """
    Return real students as numeric grade dicts, augmented.

    Each student is returned `n_copies` times. Each copy randomly
    samples within the letter-grade range, providing natural variation.

    Returns:
        List of grade dicts [{"math": 112.5, "physics": 67.5, ...}, ...]
    """
    rows = load_all_csvs()
    if not rows:
        return []

    results: List[Dict[str, float]] = []
    for row in rows:
        for _ in range(n_copies):
            results.append(convert_row_to_grades(row, randomize=True))

    logger.info(
        f"Generated {len(results)} augmented samples "
        f"from {len(rows)} real students (×{n_copies})"
    )
    return results
