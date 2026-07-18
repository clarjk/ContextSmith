"""Shared utility functions for ContextSmith."""

from datetime import datetime, timezone
from pathlib import Path
import re


def read_text_file(path: Path) -> str:
    """Read a UTF-8 text or Markdown file after validating its extension."""
    if path.suffix.lower() not in {".txt", ".md", ".markdown"}:
        raise ValueError("Only .txt, .md, and .markdown files are supported.")
    if not path.exists():
        raise ValueError(f"Input file does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("The input file must use UTF-8 encoding.") from error
    except OSError as error:
        raise ValueError(f"Unable to read input file '{path}': {error}") from error


def utc_timestamp() -> str:
    """Return the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def detect_language(text: str) -> str:
    """Estimate whether text is English, Chinese, mixed, or unknown."""
    latin_count = len(re.findall(r"[A-Za-z]", text))
    chinese_count = len(re.findall(r"[\u3400-\u9fff]", text))
    if not latin_count and not chinese_count:
        return "Unknown"
    if latin_count and chinese_count:
        total = latin_count + chinese_count
        if latin_count / total >= 0.8:
            return "English"
        if chinese_count / total >= 0.8:
            return "Chinese"
        return "Mixed"
    return "English" if latin_count else "Chinese"


def markdown_value(value: str) -> str:
    """Escape newlines so a metadata value stays on one Markdown line."""
    return value.replace("\r", " ").replace("\n", " ").strip()
