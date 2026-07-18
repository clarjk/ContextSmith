"""Tests for deterministic text cleaning."""

import unittest

from cleaner import clean_text
from config import CleaningConfig


class CleanerTests(unittest.TestCase):
    """Verify the public cleaner behavior."""

    def test_removes_promotional_lines(self) -> None:
        """Remove a complete line matching a promotional phrase."""
        self.assertEqual(clean_text("Useful body\n点赞收藏"), "Useful body")

    def test_removes_common_footers(self) -> None:
        """Remove a common footer and its trailing details."""
        source = "Useful body\nCopyright 2026 Example Publisher"

        self.assertEqual(clean_text(source), "Useful body")

    def test_removes_emoji_by_default(self) -> None:
        """Remove emoji when default cleaning rules are active."""
        self.assertEqual(clean_text("Garden 🌱 notes"), "Garden notes")

    def test_can_keep_emoji(self) -> None:
        """Keep emoji when emoji removal is disabled."""
        config = CleaningConfig(remove_emoji=False)

        self.assertEqual(clean_text("Garden 🌱", config), "Garden 🌱")

    def test_collapses_horizontal_spaces(self) -> None:
        """Collapse spaces and tabs without merging separate lines."""
        self.assertEqual(
            clean_text("Useful   garden\t  notes"),
            "Useful garden notes",
        )

    def test_removes_blank_lines(self) -> None:
        """Remove empty and whitespace-only lines."""
        self.assertEqual(clean_text("First\n\n   \nSecond"), "First\nSecond")

    def test_preserves_sentences_containing_promotional_words(self) -> None:
        """Keep body sentences that only contain a configured phrase."""
        sentence = "这篇文章解释为什么不要盲目点赞收藏。"

        self.assertEqual(clean_text(sentence), sentence)
