"""Deterministic text-cleaning functions for ContextSmith."""

import re

from config import CleaningConfig, DEFAULT_CONFIG


EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E6-\U0001F1FF"
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FAFF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "]+",
    flags=re.UNICODE,
)
VARIATION_AND_JOINER_PATTERN = re.compile(r"[\u200d\ufe0e\ufe0f]")
MULTIPLE_SPACES_PATTERN = re.compile(r"[ \t]+")


def remove_emojis(text: str) -> str:
    """Remove common emoji code-point ranges from text."""
    without_emoji = EMOJI_PATTERN.sub("", text)
    return VARIATION_AND_JOINER_PATTERN.sub("", without_emoji)


def normalize_whitespace(line: str) -> str:
    """Trim a line and collapse repeated horizontal whitespace."""
    return MULTIPLE_SPACES_PATTERN.sub(" ", line).strip()


def is_removable_line(line: str, config: CleaningConfig) -> bool:
    """Return whether a complete line matches boilerplate or a footer."""
    normalized = line.strip().casefold().strip(".!！。?？:：-—| ")
    removable = {
        phrase.casefold().strip(".!！。?？:：-—| ")
        for phrase in config.removable_phrases
    }
    if normalized in removable:
        return True
    return any(
        normalized == phrase.casefold()
        or normalized.startswith(f"{phrase.casefold()} ")
        or normalized.startswith(f"{phrase.casefold()}：")
        or normalized.startswith(f"{phrase.casefold()}:")
        for phrase in config.footer_phrases
    )


def clean_text(
    text: str,
    config: CleaningConfig = DEFAULT_CONFIG,
) -> str:
    """Clean text while preserving the order and wording of body content."""
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
    if config.remove_emoji:
        normalized_text = remove_emojis(normalized_text)

    cleaned_lines: list[str] = []
    for raw_line in normalized_text.splitlines():
        line = normalize_whitespace(raw_line)
        if not line or is_removable_line(line, config):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def cleaning_rule_names(config: CleaningConfig) -> list[str]:
    """Return human-readable names for the active cleaning rules."""
    rules = [
        "Remove blank lines",
        "Collapse repeated spaces",
        "Remove promotional boilerplate",
        "Remove common footers",
    ]
    if config.remove_emoji:
        rules.append("Remove emoji")
    return rules
