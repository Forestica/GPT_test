from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Iterable

TOKEN_RE = re.compile(r"[a-zA-Z]{3,}")


def load_keyword_bank(path: Path) -> list[str]:
    """Load one keyword phrase per line."""
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in TOKEN_RE.findall(text)]


def select_keywords(
    image_name: str,
    description: str,
    keyword_bank: Iterable[str],
    max_keywords: int = 8,
) -> list[str]:
    """
    Lightweight keyword matcher:
    - compares tokens from image filename + description
    - scores each bank phrase by token overlap
    - falls back to the most generic phrases
    """
    context_counter = Counter(_tokens(image_name) + _tokens(description))

    scored: list[tuple[int, str]] = []
    for phrase in keyword_bank:
        phrase_tokens = _tokens(phrase)
        if not phrase_tokens:
            continue
        score = sum(context_counter[t] for t in phrase_tokens)
        if score > 0:
            scored.append((score, phrase))

    scored.sort(key=lambda x: (-x[0], x[1]))
    matched = [phrase for _, phrase in scored[:max_keywords]]

    if len(matched) < max_keywords:
        for phrase in keyword_bank:
            if phrase not in matched:
                matched.append(phrase)
            if len(matched) >= max_keywords:
                break

    return matched
