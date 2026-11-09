#!/usr/bin/env python3
"""Analyze a Project ASTRO single-joint bench CSV using the standard library.

Outputs a JSON summary and four PNG plots: torque/current, backlash screen,
position step response, and temperature rise. Results derived from dry-run
logs are labelled SIMULATED. Torque constant and backlash remain BLOCKED when
the required independent measurement columns are absent.
"""

from __future__ import annotations

import argparse
import binascii
import csv
import json
import math
import statistics
import struct
import zlib
from dataclasses import dataclass
from pathlib import Path


def as_float(row: dict[str, str], key: str) -> float | None:
    value = row.get(key, "").strip()
    if not value:
        return None
    try:
        number = float(value)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("CSV has no data rows")
    required = {
        "elapsed_s",
        "run_mode",
        "command_position_rad",
        "measured_position_rad",
        "measured_velocity_rad_s",
        "measured_current_a",
        "temperature_c",
    }
    missing = sorted(required - set(rows[0]))
    if missing:
        raise ValueError("CSV missing required columns: " + ", ".join(missing))
    return rows


def regression_slope(x: list[float], y: list[float], through_origin: bool = False) -> float | None:
    if len(x) != len(y) or len(x) < 2:
        return None
    if through_origin:
        den = sum(v * v for v in x)
        return None if den == 0 else sum(a * b for a, b in zip(x, y)) / den
    xbar = statistics.fmean(x)
    ybar = statistics.fmean(y)
    den = sum((v - xbar) ** 2 for v in x)
    return None if den == 0 else sum((a - xbar) * (b - ybar) for a, b in zip(x, y)) / den


@dataclass
class Canvas:
    width: int = 1200
    height: int = 700

    def __post_init__(self) -> None:
        self.pixels = bytearray([255, 255, 255] * self.width * self.height)

    def point(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            offset = (y * self.width + x) * 3
            self.pixels[offset : offset + 3] = bytes(color)

    def line(self, x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.point(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def save(self, path: Path) -> None:
        def chunk(kind: bytes, payload: bytes) -> bytes:
            return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", binascii.crc32(kind + payload) & 0xFFFFFFFF)

        scanlines = bytearray()
        row_bytes = self.width * 3
        for y in range(self.height):
            scanlines.append(0)
            start = y * row_bytes
            scanlines.extend(self.pixels[start : start + row_bytes])
        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", struct.pack(">IIBBBBB", self.width, self.height, 8, 2, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(bytes(scanlines), 9))
        png += chunk(b"IEND", b"")
        path.write_bytes(png)


def plot(path: Path, x: list[float], series: list[tuple[list[float | None], tuple[int, int, int]]]) -> None:
    canvas = Canvas()
    left, right, top, bottom = 80, canvas.width - 40, 40, canvas.height - 70
    canvas.line(left, top, left, bottom, (20, 20, 20))
    canvas.line(left, bottom, right, bottom, (20, 20, 20))
    if not x:
        canvas.save(path)
        return
    values = [v for ys, _ in series for v in ys if v is not None and math.isfinite(v)]
    if not values:
        canvas.save(path)
        return
    xmin, xmax = min(x), max(x)
    ymin, ymax = min(values), max(values)
    if math.isclose(xmin, xmax):
        xmax = xmin + 1.0
    if math.isclose(ymin, ymax):
        pad = max(1.0, abs(ymin) * 0.1)
        ymin, ymax = ymin - pad, ymax + pad
    for tick in range(1, 5):
        y = top + (bottom - top) * tick // 5
        canvas.line(left, y, right, y, (225, 225, 225))
    for ys, color in series:
        prior: tuple[int, int] | None = None
        for xv, yv in zip(x, ys):
            if yv is None or not math.isfinite(yv):
                prior = None
                continue
            px = left + int((xv - xmin) / (xmax - xmin) * (right - left))
            py = bottom - int((yv - ymin) / (ymax - ymin) * (bottom - top))
            if prior is not None:
                canvas.line(prior[0], prior[1], px, py, color)
            prior = (px, py)
    canvas.save(path)


def detect_step_response(rows: list[dict[str, str]]) -> dict[str, float | str | None]:
    t = [as_float(r, "elapsed_s") for r in rows]
    cmd = [as_float(r, "command_position_rad") for r in rows]
    pos = [as_float(r, "measured_position_rad") for r in rows]
    valid = [(a, b, c) for a, b, c in zip(t, cmd, pos) if a is not None and b is not None and c is not None]
    if len(valid) < 5:
        return {"status": "BLOCKED - insufficient position data"}
    t2, c2, p2 = map(list, zip(*valid))
    jumps = [abs(c2[i] - c2[i - 1]) for i in range(1, len(c2))]
    index = 1 + max(range(len(jumps)), key=jumps.__getitem__)
    amplitude = c2[index] - c2[index - 1]
    if abs(amplitude) < 1e-6:
        return {"status": "BLOCKED - no command step found"}
    start = p2[index - 1]
    target = c2[index]
    delta = target - start
    direction = 1.0 if delta >= 0 else -1.0

    def crossing(level: float) -> float | None:
        threshold = start + level * delta
        for j in range(index, len(p2)):
            if direction * (p2[j] - threshold) >= 0:
                return t2[j]
        return None

    t10, t90 = crossing(0.10), crossing(0.90)
    peak = max(p2[index:]) if direction > 0 else min(p2[index:])
    overshoot = max(0.0, direction * (peak - target) / abs(delta) * 100.0)
    band = max(abs(delta) * 0.02, 1e-5)
    settling = None
    for j in range(index, len(p2)):
        if all(abs(v - target) <= band for v in p2[j:]):
            settling = t2[j] - t2[index]
            break
    return {
        "status": "SCREENED - verify test protocol and sample rate",
        "step_time_s": t2[index],
        "command_step_rad": amplitude,
        "rise_time_10_90_s": None if t10 is None or t90 is None else t90 - t10,
        "overshoot_percent": overshoot,
        "settling_time_2_percent_s": settling,
    }


def analyze(rows: list[dict[str, str]], gear_ratio: float) -> dict[str, object]:
    mode = {r.get("run_mode", "") for r in rows}
    provenance = "SIMULATED - NOT HARDWARE EVIDENCE" if mode == {"dry-run"} else "RECORDED INPUT - REVIEW REQUIRED"
    currents, torques = [], []
    for row in rows:
        current = as_float(row, "measured_current_a")
        torque = as_float(row, "measured_torque_nm")
        if current is not None and torque is not None and abs(current) > 1e-6:
            currents.append(current)
            torques.append(torque)
    kt = regression_slope(currents, torques, through_origin=True)
    torque_check = {
        "status": "BLOCKED - independent torque measurement missing" if kt is None else provenance,
        "sample_count": len(currents),
        "torque_constant_nm_per_a": kt,
        "method": "least-squares slope through origin; does not establish rated torque or safety",
    }

    residuals = []
    for row in rows:
        motor = as_float(row, "motor_position_rad")
        output = as_float(row, "output_position_rad")
        if motor is not None and output is not None:
            residuals.append(motor / gear_ratio - output)
    backlash = None if len(residuals) < 2 else max(residuals) - min(residuals)
    backlash_check = {
        "status": "BLOCKED - motor/output position pair missing" if backlash is None else provenance,
        "sample_count": len(residuals),
        "screened_backlash_rad": backlash,
        "method": "range of motor/gear_ratio minus output position; fixture compliance is not separated",
    }

    temperatures = [as_float(r, "temperature_c") for r in rows]
    times = [as_float(r, "elapsed_s") for r in rows]
    pairs = [(t, v) for t, v in zip(times, temperatures) if t is not None and v is not None]
    if pairs:
        tvals, temps = map(list, zip(*pairs))
        base_count = max(1, min(len(temps), 10))
        baseline = statistics.fmean(temps[:base_count])
        rise = max(temps) - baseline
        rate = regression_slope(tvals, temps)
        thermal = {
            "status": provenance,
            "baseline_temperature_c": baseline,
            "maximum_temperature_c": max(temps),
            "temperature_rise_c": rise,
            "linear_rate_c_per_min": None if rate is None else rate * 60.0,
            "method": "screen only; sensor location, ambient, cooling and duty must be recorded",
        }
    else:
        thermal = {"status": "BLOCKED - temperature data missing"}

    step_response = detect_step_response(rows)
    if not str(step_response.get("status", "")).startswith("BLOCKED"):
        step_response["status"] = provenance

    return {
        "provenance": provenance,
        "rows": len(rows),
        "run_modes": sorted(mode),
        "torque_constant_check": torque_check,
        "backlash_screen": backlash_check,
        "step_response": step_response,
        "temperature_rise": thermal,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("bench_analysis"))
    parser.add_argument("--gear-ratio", type=float, default=1.0, help="External ratio only; default 1.0 for direct bench output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.gear_ratio <= 0:
        raise SystemExit("--gear-ratio must be positive")
    rows = read_rows(args.csv)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary = analyze(rows, args.gear_ratio)
    (args.out_dir / "bench_analysis_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    time_s = [as_float(r, "elapsed_s") or 0.0 for r in rows]
    plot(
        args.out_dir / "torque_constant_check.png",
        time_s,
        [
            ([as_float(r, "measured_current_a") for r in rows], (0, 90, 180)),
            ([as_float(r, "measured_torque_nm") for r in rows], (190, 60, 40)),
        ],
    )
    plot(
        args.out_dir / "backlash_screen.png",
        time_s,
        [
            ([as_float(r, "motor_position_rad") for r in rows], (0, 90, 180)),
            ([as_float(r, "output_position_rad") for r in rows], (190, 60, 40)),
        ],
    )
    plot(
        args.out_dir / "step_response.png",
        time_s,
        [
            ([as_float(r, "command_position_rad") for r in rows], (35, 35, 35)),
            ([as_float(r, "measured_position_rad") for r in rows], (0, 130, 90)),
        ],
    )
    plot(
        args.out_dir / "temperature_rise.png",
        time_s,
        [([as_float(r, "temperature_c") for r in rows], (200, 80, 20))],
    )
    print(json.dumps(summary, indent=2))
    print(f"wrote summary and 4 PNG plots to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
