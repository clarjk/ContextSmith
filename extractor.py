"""Title and keyword extraction for ContextSmith."""

from collections import Counter
import re

from config import KEYWORD_LIMIT


MARKDOWN_H1_PATTERN = re.compile(r"^#\s+(.+?)\s*#*$")
TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9'-]{1,}|[\u3400-\u9fff]{2,}")
ENGLISH_STOP_WORDS = {
    "about", "after", "again", "also", "among", "and", "are", "because",
    "been", "before", "being", "between", "both", "but", "can", "could",
    "does", "each", "for", "from", "had", "has", "have", "here", "how",
    "in", "into", "its", "more", "most", "not", "only", "other", "our",
    "out",
    "over", "should", "some", "such", "than", "that", "the", "their",
    "them", "then", "there", "these", "they", "this", "through", "too",
    "to", "under", "very", "was", "were", "what", "when", "where", "which",
    "while", "who", "will", "with", "would", "you", "your",
}
CHINESE_STOP_WORDS = {
    "一个", "一些", "以及", "因为", "所以", "但是", "如果", "这个", "这些",
    "那个", "那些", "我们", "你们", "他们", "可以", "进行", "需要", "没有",
}


def extract_title(text: str) -> str:
    """Extract an H1, a short first line, or the default title."""
    title, _ = extract_title_and_content(text)
    return title


def extract_title_and_content(text: str) -> tuple[str, str]:
    """Extract a title and remove its source line from the body."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        match = MARKDOWN_H1_PATTERN.match(line)
        if match:
            body_lines = lines[:index] + lines[index + 1:]
            return match.group(1).strip(), "\n".join(body_lines)
    if lines and len(lines[0]) <= 120:
        title = lines[0].rstrip(".!！。")
        return title, "\n".join(lines[1:])
    return "Untitled Context", "\n".join(lines)


def extract_keywords(text: str, limit: int = KEYWORD_LIMIT) -> list[str]:
    """Return the most frequent meaningful tokens in deterministic order."""
    if limit < 1:
        return []
    tokens = TOKEN_PATTERN.findall(text)
    normalized_tokens = [
        token.casefold() if token.isascii() else token
        for token in tokens
    ]
    filtered_tokens = [
        token
        for token in normalized_tokens
        if token not in ENGLISH_STOP_WORDS and token not in CHINESE_STOP_WORDS
    ]
    counts = Counter(filtered_tokens)
    first_position = {
        token: index for index, token in reversed(list(enumerate(filtered_tokens)))
    }
    ranked = sorted(
        counts,
        key=lambda token: (-counts[token], first_position[token], token),
    )
    return ranked[:limit]
