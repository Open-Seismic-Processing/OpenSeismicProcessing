"""Utilities for inspecting SEG-Y files and inferring their revision."""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass, field
from typing import Optional, List, Tuple

import segyio


class SegyRevision(enum.Enum):
    REV0 = "SEG-Y Rev 0"
    REV1 = "SEG-Y Rev 1"
    REV2_PLUS = "SEG-Y Rev 2+"
    VENDOR_OR_UNKNOWN = "Vendor/Unknown"


@dataclass
class SegyInspectionResult:
    path: str
    classified_revision: SegyRevision
    revision_word: Optional[int]
    major: Optional[int]
    minor: Optional[int]
    textual_revision: Optional[str]
    trace_count: int
    num_samples: int
    dt_us: int
    sample_format_code: int
    is_variable_length_traces: Optional[bool]
    guessed_is_vendor: bool
    warnings: List[str] = field(default_factory=list)


class SegyInspector:
    """Inspect SEG-Y headers and guess the revision."""

    REVISION_WORD_OFFSET = 3501  # 3200 + 301
    FIXED_LENGTH_FLAG_OFFSET = 3505  # 3200 + 305

    @staticmethod
    def _parse_textual_revision(text_header: str) -> Optional[str]:
        text = text_header.upper()
        match = re.search(r"REV(?:ISION)?\s*([0-9]+(?:\.[0-9]+)?)", text)
        return match.group(1) if match else None

    @staticmethod
    def _classify_revision(
        rev_word: Optional[int],
        textual_rev: Optional[str],
    ) -> Tuple[SegyRevision, Optional[int], Optional[int], bool, List[str]]:
        warnings: List[str] = []
        vendorish = False
        major: Optional[int] = None
        minor: Optional[int] = None

        if rev_word is not None:
            major = (rev_word >> 8) & 0xFF
            minor = rev_word & 0xFF

        if rev_word is None:
            classified = SegyRevision.REV0
        elif rev_word == 0 or (major == 0 and minor == 0):
            classified = SegyRevision.REV0
        elif rev_word in (1, 100, 0x0100) or major == 1:
            classified = SegyRevision.REV1
        elif major is not None and major >= 2:
            classified = SegyRevision.REV2_PLUS
        else:
            classified = SegyRevision.VENDOR_OR_UNKNOWN
            vendorish = True
            warnings.append(
                f"Non-standard revision word {rev_word}; treating as vendor/unknown."
            )

        if textual_rev is not None:
            try:
                textual_major = int(float(textual_rev))
            except ValueError:
                warnings.append(
                    f"Could not parse textual revision '{textual_rev}' as a number."
                )
            else:
                if classified == SegyRevision.REV0 and textual_major >= 1:
                    warnings.append(
                        f"Binary header suggests Rev0, but textual header claims {textual_rev}."
                    )
                    vendorish = True
                if classified == SegyRevision.REV1 and textual_major == 0:
                    warnings.append(
                        "Binary header suggests Rev1, but textual header claims Rev0."
                    )
                    vendorish = True
                if classified in (SegyRevision.REV0, SegyRevision.REV1) and textual_major >= 2:
                    warnings.append(
                        f"Textual header claims revision {textual_rev}; promoting to Rev2+."
                    )
                    classified = SegyRevision.REV2_PLUS
                    vendorish = True
                if classified == SegyRevision.VENDOR_OR_UNKNOWN and textual_major in (0, 1, 2):
                    warnings.append(
                        f"Revision word looks vendor-specific, textual header claims {textual_rev}."
                    )
                    if textual_major == 0:
                        classified = SegyRevision.REV0
                    elif textual_major == 1:
                        classified = SegyRevision.REV1
                    else:
                        classified = SegyRevision.REV2_PLUS

        if classified == SegyRevision.VENDOR_OR_UNKNOWN:
            vendorish = True

        return classified, major, minor, vendorish, warnings

    @classmethod
    def inspect(cls, path: str) -> SegyInspectionResult:
        with segyio.open(path, "r", ignore_geometry=True) as f:
            try:
                rev_word = int(f.bin[cls.REVISION_WORD_OFFSET])
            except Exception:
                rev_word = None

            dt_us = int(f.bin[segyio.BinField.Interval])
            num_samples = int(f.bin[segyio.BinField.Samples])
            sample_format = int(f.bin[segyio.BinField.Format])

            try:
                fixed_len_flag = int(f.bin[cls.FIXED_LENGTH_FLAG_OFFSET])
                is_variable = fixed_len_flag == 2
            except Exception:
                is_variable = None

            trace_count = f.tracecount
            text0 = str(f.text[0])
            textual_rev = cls._parse_textual_revision(text0)

        classified, major, minor, vendorish, warnings = cls._classify_revision(
            rev_word, textual_rev
        )

        return SegyInspectionResult(
            path=path,
            classified_revision=classified,
            revision_word=rev_word,
            major=major,
            minor=minor,
            textual_revision=textual_rev,
            trace_count=trace_count,
            num_samples=num_samples,
            dt_us=dt_us,
            sample_format_code=sample_format,
            is_variable_length_traces=is_variable,
            guessed_is_vendor=vendorish,
            warnings=warnings,
        )


def print_revision_summary(result: SegyInspectionResult) -> None:
    """Print a human-readable summary of the detected SEG-Y revision."""
    rev_text = result.classified_revision.value
    textual = result.textual_revision or "unknown"
    major = result.major if result.major is not None else "?"
    minor = result.minor if result.minor is not None else "?"
    vendor = " (vendor/unknown)" if result.guessed_is_vendor else ""
    print(
        f"[SEG-Y Inspector] {result.path} -> {rev_text} "
        f"(major={major} minor={minor}, textual={textual}){vendor}"
    )
    for warning in result.warnings:
        print(f"  ⚠ {warning}")
