#!/usr/bin/env python3
"""This module encrypts personal data"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """obscure/redact return message"""
    for word in fields:
        message = re.sub(f"{word}=.*{separator}",
                         f"{word}={redaction}{separator}",
                         message
                         )
    return message
