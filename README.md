# ContextSmith

ContextSmith is an open-source Python CLI that converts messy text into clean,
structured Markdown context for ChatGPT, Codex, Claude, Gemini, and other large
language model tools.

Version 0.1.0 is deliberately deterministic. It does not call an AI API,
generate content, or summarize source material. It performs only three steps:

```text
Clean -> Structure -> Export
```

## Features

- Reads UTF-8 `.txt`, `.md`, and `.markdown` files.
- Accepts multiline pasted content in interactive mode.
- Removes blank lines and repeated horizontal spaces.
- Removes emoji by default, with an option to keep them.
- Removes configured promotional phrases and common footer lines.
- Detects a title from a Markdown H1 or the first short line and removes that
  title line from the exported body.
- Extracts up to 10 frequency-based keywords without an external service.
- Exports a clean context file and a source metadata file.

## Requirements

- Python 3.12 or newer
- No runtime dependencies outside the Python standard library

The project has no third-party runtime or test dependencies.

## Installation

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ContextSmith.git
cd ContextSmith
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Usage

Start the interactive CLI:

```bash
python main.py
```

Choose a text/Markdown file or paste content. When pasting, enter `.done` on a
new line to finish. ContextSmith writes these files to `output/`:

- `context.md`: detected title, an intentionally empty Summary section,
  cleaned content, and keywords.
- `source.md`: input name, timestamp, character and line counts, language
  estimate, and active cleaning rules.

Process a file directly:

```bash
python main.py examples/sample.txt
```

Choose another output directory:

```bash
python main.py examples/sample.txt --output build/context
```

Keep emoji:

```bash
python main.py examples/sample.txt --keep-emoji
```

## Example

Input (`examples/sample.txt`):

```text
Building Better LLM Context

Clear context helps language models work with source material.  
Good structure makes long notes easier to navigate. 🧭

点赞收藏
Copyright 2026 Example Publisher
```

Output (`context.md`):

```markdown
# Building Better LLM Context

## Summary

## Content

Clear context helps language models work with source material.
Good structure makes long notes easier to navigate.

## Keywords

clear
context
helps
language
models
work
source
material
good
structure
```

A complete example output is available in `examples/sample.md`.

## Configuration

Default cleaning phrases and footer patterns are defined in `config.py`.
`CleaningConfig` can be extended by callers without changing cleaning logic.
Boilerplate is removed only when a complete line matches a configured phrase;
this helps preserve legitimate body sentences.

## Testing

```bash
python -m unittest discover -s tests -v
```

The test suite covers cleaning, Markdown export, and keyword extraction.

## Roadmap

- Add more configurable deterministic cleaning rules.
- Improve language-aware keyword tokenization.
- Support batch conversion.
- Add configuration files and additional export templates.
- Package ContextSmith for installation from PyPI.

AI-based generation and summarization are intentionally outside the v0.1.0
scope.

## License

ContextSmith is available under the [MIT License](LICENSE).
