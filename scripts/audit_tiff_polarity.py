#!/usr/bin/env python3
"""
Audit TIFF filenames whose declared polarity ("positive" / "negative")
may disagree with image statistics.

The script never renames files. It writes a complete CSV and a suspects-only CSV.
It assumes most existing filename labels are correct.
"""

from __future__ import annotations

import argparse
import math
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import tifffile

LABEL_RE = re.compile(r"(?i)(?:^|[_\-.])(positive|negative)(?=$|[_\-.])")
HIST_BINS = 32


def parse_declared_label(path: Path) -> str | None:
    match = LABEL_RE.search(path.stem)
    return match.group(1).lower() if match else None


def make_base_id(path: Path, root: Path) -> str:
    stem = LABEL_RE.sub("_", path.stem)
    stem = re.sub(r"[_\-.]{2,}", "_", stem).strip("_-." )
    try:
        parent = path.parent.relative_to(root)
    except ValueError:
        parent = path.parent
    return str(parent / stem).lower()


def scalar_tag(page: tifffile.TiffPage, name: str, default: Any = None) -> Any:
    tag = page.tags.get(name)
    if tag is None:
        return default
    value = tag.value
    if isinstance(value, (tuple, list, np.ndarray)) and len(value) == 1:
        return value[0]
    return value


def safe_text(value: Any, max_chars: int = 1000) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")[:max_chars]
    return str(value)[:max_chars]


def metadata_hint(page: tifffile.TiffPage) -> tuple[str | None, str]:
    # Conservative: these fields may merely repeat a filename, so treat as hints only.
    fields = [
        "ImageDescription", "DocumentName", "PageName", "Software",
        "Make", "Model", "Artist", "HostComputer",
    ]
    parts: list[str] = []
    for field in fields:
        value = scalar_tag(page, field)
        if value not in (None, ""):
            parts.append(f"{field}={safe_text(value)}")

    text = " | ".join(parts)
    has_pos = bool(re.search(r"(?i)\bpositive\b", text))
    has_neg = bool(re.search(r"(?i)\bnegative\b", text))
    if has_pos and not has_neg:
        return "positive", text
    if has_neg and not has_pos:
        return "negative", text
    return None, text


def normalize_array(arr: np.ndarray, bits_per_sample: int | None) -> np.ndarray:
    if np.issubdtype(arr.dtype, np.integer):
        info = np.iinfo(arr.dtype)
        if np.issubdtype(arr.dtype, np.unsignedinteger):
            minimum = 0.0
            maximum = float((1 << bits_per_sample) - 1) if bits_per_sample else float(info.max)
        else:
            minimum, maximum = float(info.min), float(info.max)
        if maximum <= minimum:
            raise ValueError(f"Invalid numeric range for {arr.dtype}")
        out = (arr.astype(np.float32) - minimum) / (maximum - minimum)
    elif np.issubdtype(arr.dtype, np.floating):
        out = arr.astype(np.float32)
        finite = out[np.isfinite(out)]
        if finite.size == 0:
            raise ValueError("No finite pixel values")
        lo, hi = np.percentile(finite, [0.1, 99.9])
        if hi <= lo:
            lo, hi = float(finite.min()), float(finite.max())
        out = np.zeros_like(out) if hi <= lo else (out - lo) / (hi - lo)
    else:
        raise ValueError(f"Unsupported dtype: {arr.dtype}")
    return np.clip(out, 0.0, 1.0)


def prepare_image(page: tifffile.TiffPage, max_side: int) -> tuple[np.ndarray, np.ndarray | None]:
    """Return rendered grayscale and optional RGB, both normalized to 0..1."""
    photometric = int(page.photometric) if page.photometric is not None else -1
    if photometric not in (0, 1, 2):
        raise ValueError(
            f"Unsupported PhotometricInterpretation={photometric}; "
            "supports WhiteIsZero, BlackIsZero, and RGB"
        )

    arr = np.asarray(page.asarray())
    while arr.ndim > 3:
        arr = arr[0]
    arr = np.squeeze(arr)
    if arr.ndim == 3 and arr.shape[-1] not in (3, 4) and arr.shape[0] in (3, 4):
        arr = np.moveaxis(arr, 0, -1)

    bits = page.bitspersample
    if isinstance(bits, (tuple, list, np.ndarray)):
        bits_per_sample = int(max(bits))
    else:
        bits_per_sample = int(bits) if bits is not None else None
    arr = normalize_array(arr, bits_per_sample)

    if photometric in (0, 1):
        if arr.ndim == 3:
            arr = arr[..., 0]
        if arr.ndim != 2:
            raise ValueError(f"Unexpected grayscale shape: {arr.shape}")
        if photometric == 0:  # WhiteIsZero: convert to rendered black=0, white=1
            arr = 1.0 - arr
        gray, rgb = arr, None
    else:
        if arr.ndim != 3 or arr.shape[-1] < 3:
            raise ValueError(f"Unexpected RGB shape: {arr.shape}")
        rgb = arr[..., :3]
        gray = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]

    height, width = gray.shape
    stride = max(1, math.ceil(max(height, width) / max_side))
    gray = gray[::stride, ::stride]
    if rgb is not None:
        rgb = rgb[::stride, ::stride, :]
    return gray.astype(np.float32, copy=False), None if rgb is None else rgb.astype(np.float32, copy=False)


def safe_skew(values: np.ndarray) -> float:
    mean, std = float(values.mean()), float(values.std())
    return 0.0 if std < 1e-8 else float(np.mean(((values - mean) / std) ** 3))


def border_and_center(gray: np.ndarray, fraction: float = 0.08) -> tuple[np.ndarray, np.ndarray]:
    height, width = gray.shape
    bw = max(1, int(round(min(height, width) * fraction)))
    bw = min(bw, max(1, min(height, width) // 3))
    border = np.concatenate([
        gray[:bw, :].ravel(),
        gray[-bw:, :].ravel(),
        gray[bw:-bw, :bw].ravel() if height > 2 * bw else np.array([], dtype=gray.dtype),
        gray[bw:-bw, -bw:].ravel() if height > 2 * bw else np.array([], dtype=gray.dtype),
    ])
    center = gray[bw:-bw, bw:-bw].ravel() if height > 2 * bw and width > 2 * bw else gray.ravel()
    return border, center


def extract_features(path: Path, root: Path, max_side: int) -> dict[str, Any]:
    declared = parse_declared_label(path)
    if declared is None:
        raise ValueError("No positive/negative token in filename")

    with tifffile.TiffFile(path) as tif:
        page = tif.pages[0]
        photometric = int(page.photometric) if page.photometric is not None else -1
        photometric_name = getattr(page.photometric, "name", str(page.photometric))
        hint, metadata_text = metadata_hint(page)
        gray, rgb = prepare_image(page, max_side=max_side)

        values = gray.ravel()
        percentiles = np.percentile(values, [1, 5, 10, 25, 50, 75, 90, 95, 99])
        hist, _ = np.histogram(values, bins=HIST_BINS, range=(0.0, 1.0))
        hist = hist.astype(np.float64)
        hist /= max(hist.sum(), 1.0)
        nz = hist[hist > 0]
        border, center = border_and_center(gray)

        result: dict[str, Any] = {
            "path": str(path.resolve()),
            "relative_path": str(path.relative_to(root)),
            "base_id": make_base_id(path, root),
            "declared_label": declared,
            "metadata_hint": hint or "",
            "metadata_conflict": bool(hint and hint != declared),
            "metadata_text": metadata_text,
            "photometric_code": photometric,
            "photometric_name": photometric_name,
            "width": int(page.imagewidth),
            "height": int(page.imagelength),
            "samples_per_pixel": int(page.samplesperpixel or 1),
            "bits_per_sample": safe_text(page.bitspersample),
            "is_color": int(rgb is not None),
            "mean": float(values.mean()),
            "std": float(values.std()),
            "skew": safe_skew(values),
            "entropy": float(-(nz * np.log2(nz)).sum()),
            "dark_fraction_01": float(np.mean(values <= 0.01)),
            "dark_fraction_05": float(np.mean(values <= 0.05)),
            "bright_fraction_95": float(np.mean(values >= 0.95)),
            "bright_fraction_99": float(np.mean(values >= 0.99)),
            "border_mean": float(border.mean()),
            "center_mean": float(center.mean()),
            "border_minus_center": float(border.mean() - center.mean()),
            "border_dark_fraction_05": float(np.mean(border <= 0.05)),
            "border_bright_fraction_95": float(np.mean(border >= 0.95)),
        }

        for name, value in zip(
            ["p01", "p05", "p10", "p25", "p50", "p75", "p90", "p95", "p99"],
            percentiles,
        ):
            result[name] = float(value)
        for i, value in enumerate(hist):
            result[f"hist_{i:02d}"] = float(value)

        color_keys = [
            "red_mean", "green_mean", "blue_mean", "red_median", "green_median", "blue_median",
            "mean_saturation_proxy", "orange_mask_score", "channel_mean_spread",
        ]
        if rgb is None:
            result.update({key: np.nan for key in color_keys})
        else:
            pixels = rgb.reshape(-1, 3)
            means, medians = pixels.mean(axis=0), np.median(pixels, axis=0)
            result.update({
                "red_mean": float(means[0]), "green_mean": float(means[1]), "blue_mean": float(means[2]),
                "red_median": float(medians[0]), "green_median": float(medians[1]), "blue_median": float(medians[2]),
                "mean_saturation_proxy": float(np.mean(rgb.max(axis=2) - rgb.min(axis=2))),
                "orange_mask_score": float((means[0] - means[2]) + 0.5 * (means[1] - means[2])),
                "channel_mean_spread": float(np.std(means)),
            })
        return result


def add_pair_checks(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame["pair_hist_inverse_corr"] = np.nan
    hcols = [f"hist_{i:02d}" for i in range(HIST_BINS)]
    for _, group in frame.groupby("base_id", sort=False):
        pos = group[group["declared_label"] == "positive"]
        neg = group[group["declared_label"] == "negative"]
        if len(pos) != 1 or len(neg) != 1:
            continue
        hp = pos.iloc[0][hcols].to_numpy(dtype=float)
        hn = neg.iloc[0][hcols].to_numpy(dtype=float)[::-1]
        corr = np.nan if np.std(hp) < 1e-12 or np.std(hn) < 1e-12 else float(np.corrcoef(hp, hn)[0, 1])
        frame.loc[group.index, "pair_hist_inverse_corr"] = corr
    return frame


def model_predictions(frame: pd.DataFrame, threshold: float) -> pd.DataFrame:
    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.impute import SimpleImputer
        from sklearn.model_selection import StratifiedGroupKFold, StratifiedKFold, cross_val_predict
        from sklearn.pipeline import make_pipeline
    except ImportError as exc:
        raise SystemExit(
            "Install dependencies with:\n"
            "  python -m pip install numpy pandas tifffile imagecodecs scikit-learn"
        ) from exc

    output = frame.copy()
    excluded = {
        "path", "relative_path", "base_id", "declared_label", "metadata_hint",
        "metadata_conflict", "metadata_text", "photometric_name", "bits_per_sample",
        "width", "height", "samples_per_pixel", "pair_hist_inverse_corr",
    }
    feature_columns = [
        c for c in output.columns
        if (
            c not in excluded
            and pd.api.types.is_numeric_dtype(output[c])
            and output[c].notna().any()
        )
    ]
    y = (output["declared_label"] == "positive").astype(int).to_numpy()
    counts = np.bincount(y, minlength=2)
    if counts.min() < 5:
        raise SystemExit("Need at least 5 readable files in each declared class.")

    X = output[feature_columns]
    groups = output["base_id"].astype(str).to_numpy()
    model = make_pipeline(
        SimpleImputer(strategy="median", add_indicator=True),
        RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=3,
            class_weight="balanced_subsample",
            random_state=42,
            n_jobs=1,
        ),
    )
    n_splits = int(min(5, counts.min()))
    try:
        cv = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=42)
        probabilities = cross_val_predict(
            model, X, y, groups=groups, cv=cv, method="predict_proba", n_jobs=1
        )
    except ValueError:
        cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        probabilities = cross_val_predict(model, X, y, cv=cv, method="predict_proba", n_jobs=1)

    p_positive = probabilities[:, 1]
    predicted = np.where(p_positive >= 0.5, "positive", "negative")
    suspicion = np.where(y == 1, 1.0 - p_positive, p_positive)
    output["probability_positive"] = p_positive
    output["predicted_label"] = predicted
    output["suspicion_score"] = suspicion
    output["model_disagrees"] = predicted != output["declared_label"].to_numpy()
    output["model_flag"] = suspicion >= threshold
    output["flag_for_review"] = output["model_flag"] | output["metadata_conflict"]

    reason = np.full(len(output), "", dtype=object)
    both = output["model_flag"].to_numpy() & output["metadata_conflict"].to_numpy()
    reason[both] = "model+metadata"
    reason[output["model_flag"].to_numpy() & ~both] = "model"
    reason[output["metadata_conflict"].to_numpy() & ~both] = "metadata"
    output["flag_reason"] = reason

    # Batch-level swap detection
    pos_mask = output["declared_label"] == "positive"
    neg_mask = output["declared_label"] == "negative"
    
    if pos_mask.any() and neg_mask.any():
        pos_dark = output.loc[pos_mask, "dark_fraction_05"].mean()
        neg_dark = output.loc[neg_mask, "dark_fraction_05"].mean()
        
        # If declared positives have a significantly higher fraction of dark pixels,
        # it is highly likely the entire batch's labels were swapped.
        if pos_dark > neg_dark + 0.1:
            print(f"\nWARNING: Batch-level swap detected! Declared 'positive' images are significantly darker (avg dark_fraction_05={pos_dark:.2f}) than 'negative' images (avg dark_fraction_05={neg_dark:.2f}).")
            output["flag_for_review"] = True
            output["suspicion_score"] = np.maximum(output["suspicion_score"], 0.99)
            
            has_reason = output["flag_reason"] != ""
            output.loc[has_reason, "flag_reason"] += "+batch_swapped"
            output.loc[~has_reason, "flag_reason"] = "batch_swapped"

    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Flag potentially mislabeled positive/negative TIFF files.")
    parser.add_argument("root", type=Path, help="Root folder to scan recursively")
    parser.add_argument("--output", type=Path, default=Path("tiff_polarity_audit.csv"))
    parser.add_argument("--threshold", type=float, default=0.90)
    parser.add_argument("--max-side", type=int, default=512)
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"Not a directory: {root}")
    if not 0.5 < args.threshold < 1.0:
        parser.error("--threshold must be between 0.5 and 1.0")

    paths = sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in {".tif", ".tiff"} and parse_declared_label(p)
    )
    if not paths:
        raise SystemExit("No labeled TIFFs found.")

    rows, errors = [], []
    for i, path in enumerate(paths, 1):
        print(f"\rReading {i}/{len(paths)}: {path.name[:60]:60}", end="", flush=True)
        try:
            rows.append(extract_features(path, root, args.max_side))
        except Exception as exc:
            errors.append({
                "path": str(path.resolve()),
                "relative_path": str(path.relative_to(root)),
                "error": f"{type(exc).__name__}: {exc}",
            })
    print()
    if not rows:
        raise SystemExit("No files could be analyzed.")

    frame = model_predictions(add_pair_checks(pd.DataFrame(rows)), args.threshold)
    frame = frame.sort_values(["flag_for_review", "suspicion_score"], ascending=[False, False])

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    suspects = output.with_name(f"{output.stem}_suspects{output.suffix}")
    frame[frame["flag_for_review"]].to_csv(suspects, index=False)

    print(f"Analyzed: {len(frame)}")
    print(f"Flagged for review: {int(frame['flag_for_review'].sum())}")
    print(f"Complete report: {output}")
    print(f"Suspects report: {suspects}")
    if errors:
        error_path = output.with_name(f"{output.stem}_errors{output.suffix}")
        pd.DataFrame(errors).to_csv(error_path, index=False)
        print(f"Unreadable/unsupported: {len(errors)}")
        print(f"Errors report: {error_path}")
    print("\nTreat flags as review candidates, not automatic rename decisions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
