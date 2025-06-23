
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Set

import requests  

try:
    from pdfminer.high_level import extract_text as pdf_text  # 
    from docx import Document  #
except ModuleNotFoundError:  # 
    pdf_text = None          #
    Document = None          #

YEAR_PATTERN = re.compile(r"\b(19[5-9]\d|20\d{2}|21\d{2})\b")


# --------------------------------------------------------------------------- #
# Public API (agents import this)
# --------------------------------------------------------------------------- #
def analyze_resume_text(text: str | List[str], *, as_of: int | None = None) -> dict:

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
# Internal helpers
# --------------------------------------------------------------------------- #
def _extract_years(lines: List[str], *, up_to: int) -> Set[int]:
    years: set[int] = set()
    for line in lines:
        for token in YEAR_PATTERN.findall(line):
            yr = int(token)
            if 1950 <= yr <= up_to:
                years.add(yr)
    return years


def _estimate_age(earliest_year: int, *, as_of: int, offset: int = 22) -> int:
    return (as_of - earliest_year) + offset


def _load_text_from_file(path: Path) -> List[str]:
    ext = path.suffix.lower()
    if ext == ".pdf":
        if pdf_text is None: 
            raise RuntimeError("pdfminer.six not installed.")
        return pdf_text(str(path)).splitlines()

    if ext in {".docx", ".doc"}:
        if Document is None: 
            raise RuntimeError("python-docx not installed.")
        doc = Document(path)
        return [p.text for p in doc.paragraphs]

    raise ValueError(f"Unsupported file type: {ext}")


def _send_callback(url: str, payload: dict) -> None:
    
    headers = {"X-Resume-Insight": json.dumps(payload, separators=(",", ":"))}
    try:
        requests.get(url, headers=headers, timeout=5)
    except Exception as exc:  # noqa: BLE001
        print(f"⚠️  Callback failed: {exc}", file=sys.stderr)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _parse_args() -> argparse.Namespace:
    this_year = datetime.utcnow().year
    p = argparse.ArgumentParser(description="Infer experience and age from a résumé.")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", type=Path, help="Path to résumé (.pdf / .docx)")
    src.add_argument("--stdin", action="store_true", help="Read résumé text from STDIN")
    p.add_argument("--as-of", type=int, default=this_year, help="Reference year")
    p.add_argument(
        "--callback-url",
        help="If set, send a GET request with header X-Resume-Insight "
        "containing the JSON result.",
    )
    return p.parse_args()


def _cli() -> None:  #
    args = _parse_args()

    try:
        if args.file:
            lines = _load_text_from_file(args.file)
            result = analyze_resume_text(lines, as_of=args.as_of)
        else:  
            raw = sys.stdin.read()
            result = analyze_resume_text(raw, as_of=args.as_of)
    except Exception as exc:
        print(f"❌  {exc}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result))

    if args.callback_url:
        _send_callback(args.callback_url, result)


if __name__ == "__main__":  
    _cli()
