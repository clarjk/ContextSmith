"""Markdown export functions for ContextSmith."""

from dataclasses import dataclass
from pathlib import Path

from config import CONTEXT_FILENAME, SOURCE_FILENAME
from utils import markdown_value


@dataclass(frozen=True, slots=True)
class SourceMetadata:
    """Describe the source and processing details of one conversion."""

    input_file: str
    created_time: str
    characters: int
    lines: int
    language: str
    cleaning_rules: tuple[str, ...]


def build_context_markdown(
    title: str,
    content: str,
    keywords: list[str],
) -> str:
    """Build context.md without generating or summarizing source content."""
    keyword_block = "\n".join(keywords)
    return (
        f"# {title}\n\n"
        "## Summary\n\n"
        "## Content\n\n"
        f"{content}\n\n"
        "## Keywords\n\n"
        f"{keyword_block}\n"
    )


def build_source_markdown(metadata: SourceMetadata) -> str:
    """Build source.md from conversion metadata."""
    rules = ", ".join(metadata.cleaning_rules)
    return (
        "# Metadata\n\n"
        f"- Input File: {markdown_value(metadata.input_file)}\n"
        f"- Created Time: {metadata.created_time}\n"
        f"- Characters: {metadata.characters}\n"
        f"- Lines: {metadata.lines}\n"
        f"- Language: {metadata.language}\n"
        f"- Cleaning Rules: {rules}\n"
    )


def export_markdown(
    output_directory: Path,
    context_markdown: str,
    source_markdown: str,
) -> tuple[Path, Path]:
    """Write context.md and source.md to an output directory."""
    try:
        output_directory.mkdir(parents=True, exist_ok=True)
        context_path = output_directory / CONTEXT_FILENAME
        source_path = output_directory / SOURCE_FILENAME
        context_path.write_text(context_markdown, encoding="utf-8")
        source_path.write_text(source_markdown, encoding="utf-8")
    except OSError as error:
        message = f"Unable to create or write output directory '{output_directory}'"
        raise ValueError(f"{message}: {error}") from error
    return context_path, source_path
