#!/usr/bin/env python3
"""
Resume-Insight  –  dual-mode version
------------------------------------

• **CLI mode**  : python resume_insight.py --file resume.pdf
• **Agent mode**: from resume_insight import analyze_resume_text

The agent simply passes the résumé’s raw text (already in memory) and
gets back a dict:

    result = analyze_resume_text(resume_text, as_of=2025)
    # {'years_experience': 6, 'predicted_age': 28}
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Set

try:
    from pdfminer.high_level import extract_text as pdf_text  # type: ignore
    from docx import Document  # type: ignore
except ModuleNotFoundError:
    pdf_text = None
    Document = None

YEAR_PATTERN = re.compile(r"\b(19[5-9]\d|20\d{2}|21\d{2})\b")


# --------------------------------------------------------------------------- #
#  Public API for agents
# --------------------------------------------------------------------------- #
def analyze_resume_text(text: str | List[str], *, as_of: int | None = None) -> dict:
    """
    Core heuristic packaged for agents.

    Parameters
    ----------
    text : str | List[str]
        The résumé content – either as a single string or already split lines.
    as_of : int, optional
        Reference year (defaults to UTC current year).

    Returns
    -------
    dict
        {"years_experience": int, "predicted_age": int}
    """
    as_of = as_of or datetime.utcnow().year
    lines = text.splitlines() if isinstance(text, str) else text

    years = _extract_years(lines, up_to=as_of)
    if not years:
        raise ValueError("No 4-digit years detected in résumé text.")

    earliest = min(years)
    years_exp = as_of - earliest
    predicted_age = _estimate_age(earliest, as_of=as_of)

    return {"years_experience": years_exp, "predicted_age": predicted_age}


# --------------------------------------------------------------------------- #
#  Helpers (private)
# --------------------------------------------------------------------------- #
def _extract_years(lines: List[str], *, up_to: int) -> Set[int]:
    years: set[int] = set()
    for line in lines:
        for yr in YEAR_PATTERN.findall(line):
            y = int(yr)
            if 1950 <= y <= up_to:
                years.add(y)
    return years


def _estimate_age(earliest_year: int, *, as_of: int, offset: int = 22) -> int:
    return (as_of - earliest_year) + offset


def _load_text_from_file(path: Path) -> List[str]:
    """Only used in CLI mode."""
    suffix = path.suffix.lower()

    if suffix == ".pdf":
        if pdf_text is None:  # pragma: no cover
            raise RuntimeError("pdfminer.six not installed")
        return pdf_text(str(path)).splitlines()

    if suffix in {".docx", ".doc"}:
        if Document is None:  # pragma: no cover
            raise RuntimeError("python-docx not installed")
        doc = Document(path)
        return [p.text for p in doc.paragraphs]

    raise ValueError(f"Unsupported file type: {suffix}")


# --------------------------------------------------------------------------- #
#  CLI entry-point
# --------------------------------------------------------------------------- #
def _parse_args() -> argparse.Namespace:
    this_year = datetime.utcnow().year
    p = argparse.ArgumentParser(description="Estimate experience & age from résumé.")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--file", type=Path, help="Path to résumé (.pdf or .docx)")
    g.add_argument(
        "--stdin",
        action="store_true",
        help="Read résumé plain-text from STDIN (useful for pipes/agents)",
    )
    p.add_argument("--as-of", type=int, default=this_year, help="Reference year")
    return p.parse_args()


def _cli() -> None:  
    args = _parse_args()
    try:
        if args.file:
            lines = _load_text_from_file(args.file)
            result = analyze_resume_text(lines, as_of=args.as_of)
        else:  
            stdin_text = sys.stdin.read()
            result = analyze_resume_text(stdin_text, as_of=args.as_of)
    except Exception as exc:
        print(f"❌  {exc}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result))


if __name__ == "__main__":  
    _cli()
