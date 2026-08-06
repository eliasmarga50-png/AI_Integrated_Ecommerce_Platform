


"""
Shared utility functions for the AI application.

This module contains lightweight, reusable helpers that can be safely
used by every AI engine without introducing business logic.
"""

import hashlib
import re
import time
import uuid
from typing import Iterable


def normalize_text(text: str) -> str:
    """
    Normalize text for searching and AI processing.

    - Remove extra whitespace
    - Convert to lowercase
    - Strip leading/trailing spaces
    """

    if not text:
        return ""

    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)

    return text


def estimate_tokens(text: str) -> int:
    """
    Approximate token count.

    This is intentionally lightweight.
    A production tokenizer can replace this later.
    """

    if not text:
        return 0

    return len(text.split())


def generate_request_id() -> str:
    """
    Generate a unique request identifier.
    """

    return str(uuid.uuid4())


def calculate_execution_time(start_time: float) -> float:
    """
    Return elapsed execution time in seconds.
    """

    return round(time.perf_counter() - start_time, 4)


def start_timer() -> float:
    """
    Return a high-precision timer.
    """

    return time.perf_counter()


def hash_text(text: str) -> str:
    """
    Return SHA-256 hash of text.

    Useful for caching and deduplication.
    """

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def remove_duplicate_items(items: Iterable):
    """
    Remove duplicates while preserving order.
    """

    seen = set()

    unique = []

    for item in items:
        if item not in seen:
            seen.add(item)
            unique.append(item)

    return unique


def truncate_text(text: str, length: int = 200) -> str:
    """
    Shorten text without breaking the application.
    """

    if len(text) <= length:
        return text

    return text[:length].rstrip() + "..."


def confidence_percentage(score: float) -> float:
    """
    Convert confidence score (0-1)
    into percentage.
    """

    score = max(0.0, min(score, 1.0))

    return round(score * 100, 2)


def safe_float(value, default=0.0):
    """
    Safely convert a value to float.
    """

    try:
        return float(value)
    except (ValueError, TypeError):
        return default


