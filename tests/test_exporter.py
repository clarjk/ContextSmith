"""Tests for Markdown export."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from exporter import (
    SourceMetadata,
    build_context_markdown,
    build_source_markdown,
    export_markdown,
)


class ExporterTests(unittest.TestCase):
    """Verify creation and structure of exported Markdown files."""

    def setUp(self) -> None:
        """Build reusable context and source Markdown fixtures."""
        self.context = build_context_markdown(
            "Garden Notes",
            "Tomatoes need sun.",
            ["tomatoes", "sun"],
        )
        metadata = SourceMetadata(
            input_file="notes.txt",
            created_time="2026-01-01T00:00:00+00:00",
            characters=18,
            lines=1,
            language="English",
            cleaning_rules=("Remove blank lines",),
        )
        self.source = build_source_markdown(metadata)

    def test_generates_context_markdown_structure(self) -> None:
        """Create context Markdown with an empty Summary section."""
        expected = (
            "# Garden Notes\n\n"
            "## Summary\n\n"
            "## Content\n\n"
            "Tomatoes need sun.\n\n"
            "## Keywords\n\n"
            "tomatoes\n"
            "sun\n"
        )

        self.assertEqual(self.context, expected)

    def test_generates_source_markdown_fields(self) -> None:
        """Create source Markdown containing every required field."""
        for field in (
            "Input File",
            "Created Time",
            "Characters",
            "Lines",
            "Language",
            "Cleaning Rules",
        ):
            self.assertIn(field, self.source)

    def test_creates_output_directory_and_both_files(self) -> None:
        """Create a missing output directory and both Markdown files."""
        with TemporaryDirectory() as directory:
            output_directory = Path(directory) / "nested" / "output"
            context_path, source_path = export_markdown(
                output_directory,
                self.context,
                self.source,
            )

            self.assertTrue(output_directory.is_dir())
            self.assertEqual(context_path.name, "context.md")
            self.assertEqual(source_path.name, "source.md")
            self.assertEqual(
                context_path.read_text(encoding="utf-8"),
                self.context,
            )
            self.assertEqual(
                source_path.read_text(encoding="utf-8"),
                self.source,
            )
