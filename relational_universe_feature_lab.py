#!/usr/bin/env python3
"""Backward-compatible wrapper around the refactored feature-lab package."""

from __future__ import annotations

from feature_lab.main import main


if __name__ == "__main__":
    raise SystemExit(main())
