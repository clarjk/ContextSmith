"""Configuration values for ContextSmith."""

from dataclasses import dataclass, field


__version__ = "0.1.0"


DEFAULT_REMOVABLE_PHRASES: tuple[str, ...] = (
    "点赞收藏",
    "关注我",
    "分享一下",
    "更多精彩内容",
    "广告",
)

DEFAULT_FOOTER_PHRASES: tuple[str, ...] = (
    "all rights reserved",
    "copyright",
    "privacy policy",
    "terms of service",
    "unsubscribe",
    "版权所有",
    "免责声明",
    "阅读原文",
)


@dataclass(frozen=True, slots=True)
class CleaningConfig:
    """Define deterministic rules used by the text cleaner."""

    remove_emoji: bool = True
    removable_phrases: tuple[str, ...] = field(
        default=DEFAULT_REMOVABLE_PHRASES
    )
    footer_phrases: tuple[str, ...] = field(default=DEFAULT_FOOTER_PHRASES)


DEFAULT_CONFIG = CleaningConfig()
DEFAULT_OUTPUT_DIRECTORY = "output"
CONTEXT_FILENAME = "context.md"
SOURCE_FILENAME = "source.md"
KEYWORD_LIMIT = 10
