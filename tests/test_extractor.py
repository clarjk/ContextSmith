"""Tests for title and keyword extraction."""

import unittest

from extractor import (
    extract_keywords,
    extract_title,
    extract_title_and_content,
)


class TitleExtractorTests(unittest.TestCase):
    """Verify title priority and title removal from body content."""

    def test_prefers_markdown_h1(self) -> None:
        """Prefer a Markdown H1 even when it follows an earlier line."""
        text = "Introductory body line\n# Garden Guide\nMore body"

        self.assertEqual(extract_title(text), "Garden Guide")

    def test_uses_short_first_line(self) -> None:
        """Use the first short line when no Markdown H1 exists."""
        self.assertEqual(
            extract_title("Garden Guide\nDetailed body text."),
            "Garden Guide",
        )

    def test_uses_default_title(self) -> None:
        """Use the default when the first line is too long to be a title."""
        text = "A" * 121

        self.assertEqual(extract_title(text), "Untitled Context")

    def test_removes_title_from_content(self) -> None:
        """Return body content without repeating the extracted title line."""
        title, content = extract_title_and_content(
            "Building Better Context\nFirst body line.\nSecond body line."
        )

        self.assertEqual(title, "Building Better Context")
        self.assertEqual(content, "First body line.\nSecond body line.")


class KeywordExtractorTests(unittest.TestCase):
    """Verify deterministic keyword limits and ranking."""

    def test_returns_no_more_than_ten_keywords(self) -> None:
        """Limit default keyword results to ten entries."""
        text = " ".join(f"word{index}" for index in range(15))

        self.assertEqual(len(extract_keywords(text)), 10)

    def test_preserves_stable_order_for_equal_frequencies(self) -> None:
        """Use first appearance as the stable tie-breaking order."""
        text = "beta alpha gamma beta alpha gamma"

        self.assertEqual(
            extract_keywords(text),
            ["beta", "alpha", "gamma"],
        )

    def test_ranks_frequency_before_first_appearance(self) -> None:
        """Rank a more frequent term ahead of an earlier term."""
        text = "garden soil soil compost"

        self.assertEqual(
            extract_keywords(text),
            ["soil", "garden", "compost"],
        )
