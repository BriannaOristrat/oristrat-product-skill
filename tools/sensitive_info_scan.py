#!/usr/bin/env python3
"""Fail a GitHub submission when repository files contain likely secrets."""

from __future__ import annotations

import math
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 2 * 1024 * 1024
SKIP_DIRS = {".git", "node_modules", "__pycache__", "output", "tmp", "00_入口"}
SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".xlsx",
    ".xls",
    ".docx",
    ".pptx",
    ".pyc",
}

SECRET_PATTERNS = [
    ("private-key-block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{30,}\b")),
    ("github-pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{40,}\b")),
    ("api-secret-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
]

ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b("
    r"password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key|"
    r"private[_-]?key|client[_-]?secret|session|cookie|tenant[_-]?code"
    r")\b\s*[:=]\s*(['\"])([^'\"]{6,})\2"
)

SAFE_VALUES = {
    "changeme",
    "change-me",
    "example",
    "example-value",
    "placeholder",
    "dummy",
    "redacted",
    "masked",
    "password",
    "secret",
    "token",
    "tenant",
    "tenant-code",
    "your-password",
    "your-token",
    "your-api-key",
}


@dataclass
class Finding:
    path: Path
    line_no: int
    rule: str
    snippet: str


def tracked_and_untracked_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return [ROOT / line.strip() for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        return [p for p in ROOT.rglob("*") if p.is_file()]


def should_scan(path: Path) -> bool:
    rel_parts = path.relative_to(ROOT).parts
    if any(part in SKIP_DIRS for part in rel_parts):
        return False
    if path.suffix.lower() in SKIP_SUFFIXES:
        return False
    if not path.exists() or path.stat().st_size > MAX_FILE_BYTES:
        return False
    return True


def is_binary(path: Path) -> bool:
    return b"\0" in path.read_bytes()[:4096]


def entropy(value: str) -> float:
    if not value:
        return 0.0
    counts = {char: value.count(char) for char in set(value)}
    return -sum((count / len(value)) * math.log2(count / len(value)) for count in counts.values())


def looks_safe_assignment_value(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in SAFE_VALUES:
        return True
    if lowered.startswith(("your-", "example-", "sample-", "demo-", "mock-")):
        return True
    if "[" in value or "]" in value or "<" in value or ">" in value:
        return True
    if "${" in value or "process.env" in value or "config." in value:
        return True
    if value.startswith(("http://", "https://")):
        return True
    return False


def redact(snippet: str) -> str:
    compact = snippet.strip()
    if len(compact) <= 18:
        return compact[:3] + "***" if len(compact) > 6 else "***"
    return f"{compact[:8]}...{compact[-6:]}"


def scan_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        if is_binary(path):
            return findings
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return findings

    for line_no, line in enumerate(text.splitlines(), start=1):
        for rule, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(line):
                findings.append(Finding(path, line_no, rule, redact(match.group(0))))

        for match in ASSIGNMENT_PATTERN.finditer(line):
            key = match.group(1)
            value = match.group(3).strip()
            if looks_safe_assignment_value(value):
                continue
            if len(value) >= 16 or entropy(value) >= 3.2:
                findings.append(Finding(path, line_no, f"literal-{key}", redact(value)))
    return findings


def main() -> int:
    findings: list[Finding] = []
    for path in tracked_and_untracked_files():
        if should_scan(path):
            findings.extend(scan_file(path))

    if findings:
        print("Sensitive information scan failed.")
        for item in findings:
            rel = item.path.relative_to(ROOT)
            print(f"{rel}:{item.line_no}: {item.rule}: {item.snippet}")
        print("Remove the secret, rotate the credential if it was real, then rerun this scan.")
        return 1

    print("Sensitive information scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
