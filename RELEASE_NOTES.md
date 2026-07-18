# ContextSmith v0.1.0

ContextSmith v0.1.0 is the initial open-source release for converting
unstructured text into predictable Markdown context files. It uses
deterministic local text processing only: no AI features, external model APIs,
generation, or summaries.

## Highlights

- Interactive input from UTF-8 text files, Markdown files, or pasted content.
- Optional command-line file input and custom output directory.
- Removal of blank lines, repeated spaces, emoji, promotional phrases, and
  common footer lines.
- Automatic title detection and Top 10 frequency-based keyword extraction.
- Export of `context.md` and `source.md` with processing metadata.
- Configurable emoji preservation through `--keep-emoji`.
- Standard-library tests and Python 3.12/3.13 GitHub Actions CI.

## Installation

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ContextSmith.git
cd ContextSmith
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Upgrade Notes

This is the initial release. There are no migration steps.
