"""Command-line entry point for ContextSmith."""

import argparse
from pathlib import Path
import sys

from cleaner import clean_text, cleaning_rule_names
from config import CleaningConfig, DEFAULT_OUTPUT_DIRECTORY, __version__
from exporter import (
    SourceMetadata,
    build_context_markdown,
    build_source_markdown,
    export_markdown,
)
from extractor import extract_keywords, extract_title_and_content
from utils import detect_language, read_text_file, utc_timestamp


def build_parser() -> argparse.ArgumentParser:
    """Create the ContextSmith command-line parser."""
    parser = argparse.ArgumentParser(
        description="Clean, structure, and export text as LLM-ready Markdown."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"ContextSmith {__version__}",
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help="UTF-8 .txt, .md, or .markdown file",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(DEFAULT_OUTPUT_DIRECTORY),
        help="Output directory (default: output)",
    )
    parser.add_argument(
        "--keep-emoji",
        action="store_true",
        help="Keep emoji instead of removing them",
    )
    return parser


def read_pasted_text() -> str:
    """Read multiline pasted text until a line containing only .done."""
    print("Paste content below. Enter .done on a new line to finish:")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == ".done":
            break
        lines.append(line)
    return "\n".join(lines)


def get_interactive_input() -> tuple[str, str]:
    """Prompt the user to select a file or paste content."""
    print(f"ContextSmith v{__version__}")
    print("1. Open a text or Markdown file")
    print("2. Paste content")
    choice = input("Choose 1 or 2: ").strip()
    if choice == "1":
        path = Path(input("Input file path: ").strip()).expanduser()
        return read_text_file(path), str(path)
    if choice == "2":
        return read_pasted_text(), "Pasted content"
    raise ValueError("Please choose 1 or 2.")


def process_content(
    text: str,
    source_name: str,
    output_directory: Path,
    config: CleaningConfig,
) -> tuple[Path, Path]:
    """Clean, structure, and export one text input."""
    cleaned = clean_text(text, config)
    if not cleaned:
        raise ValueError("No content remains after cleaning.")
    title, content = extract_title_and_content(cleaned)
    keywords = extract_keywords(content)
    context_markdown = build_context_markdown(title, content, keywords)
    metadata = SourceMetadata(
        input_file=source_name,
        created_time=utc_timestamp(),
        characters=len(content),
        lines=len(content.splitlines()),
        language=detect_language(content),
        cleaning_rules=tuple(cleaning_rule_names(config)),
    )
    source_markdown = build_source_markdown(metadata)
    return export_markdown(output_directory, context_markdown, source_markdown)


def main() -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    arguments = parser.parse_args()
    config = CleaningConfig(remove_emoji=not arguments.keep_emoji)
    try:
        if arguments.input:
            text = read_text_file(arguments.input)
            source_name = str(arguments.input)
        else:
            text, source_name = get_interactive_input()
        context_path, source_path = process_content(
            text,
            source_name,
            arguments.output,
            config,
        )
    except (EOFError, OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Created: {context_path}")
    print(f"Created: {source_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
