#!/usr/bin/env python3
"""Safe-by-default single-joint bench logger for ProjectBayMax.

The default mode is a software-only dry run. Hardware mode is intentionally
blocked until an adapter is implemented and checked against the exact
RobStride 04 hardware and firmware revision in the official protocol manual:
https://www.robstride.com/assets/product_manual_robStride04-37549d59.pdf

No CAN identifiers, registers, byte layouts, or enable sequences are guessed
in this file. A hardware run also requires an explicit permit identifier,
software current limit, and second-person acknowledgement.

Examples:
    python3 single_joint_bench.py --duration-s 8 --profile step
    python3 single_joint_bench.py --profile sine --output dry_sine.csv

The dry-run telemetry is simulated and must never be reported as hardware
evidence. It exists to test logging, clamping, stop, and watchdog behavior.
"""

from __future__ import annotations

import argparse
import csv
import math
import signal
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol


LOG_FIELDS = [
    "timestamp_utc",
    "elapsed_s",
    "run_mode",
    "profile",
    "command_position_rad",
    "command_velocity_rad_s",
    "command_current_a",
    "measured_position_rad",
    "measured_velocity_rad_s",
    "measured_current_a",
    "temperature_c",
    "motor_position_rad",
    "output_position_rad",
    "measured_torque_nm",
    "watchdog_state",
    "notes",
]


@dataclass(frozen=True)
class Command:
    position_rad: float
    velocity_rad_s: float
    current_a: float


@dataclass(frozen=True)
class Telemetry:
    position_rad: float
    velocity_rad_s: float
    current_a: float
    temperature_c: float
    motor_position_rad: float | None = None
    output_position_rad: float | None = None
    torque_nm: float | None = None
    notes: str = ""


class BenchBackend(Protocol):
    def enable(self) -> None: ...

    def command(self, command: Command) -> None: ...

    def read(self, now_s: float) -> Telemetry: ...

    def stop(self) -> None: ...

    def close(self) -> None: ...


class DryRunBackend:
    """Small deterministic plant used only to exercise the software path."""

    SIMULATED_TORQUE_CONSTANT_NM_PER_A = 2.1

    def __init__(self) -> None:
        self._enabled = False
        self._command = Command(0.0, 0.0, 0.0)
        self._position = 0.0
        self._velocity = 0.0
        self._temperature_c = 22.0
        self._last_s: float | None = None

    def enable(self) -> None:
        self._enabled = True

    def command(self, command: Command) -> None:
        if not self._enabled:
            raise RuntimeError("dry-run backend is not enabled")
        self._command = command

    def read(self, now_s: float) -> Telemetry:
        dt = 0.0 if self._last_s is None else max(0.0, min(now_s - self._last_s, 0.1))
        self._last_s = now_s
        if self._enabled and dt:
            position_error = self._command.position_rad - self._position
            target_velocity = self._command.velocity_rad_s + 8.0 * position_error
            self._velocity += (target_velocity - self._velocity) * min(1.0, 8.0 * dt)
            self._position += self._velocity * dt
            self._temperature_c += (abs(self._command.current_a) * 0.025 - 0.006) * dt
        measured_current = self._command.current_a if self._enabled else 0.0
        simulated_backlash = 0.002 if self._velocity >= 0 else -0.002
        return Telemetry(
            position_rad=self._position,
            velocity_rad_s=self._velocity,
            current_a=measured_current,
            temperature_c=self._temperature_c,
            motor_position_rad=self._position,
            output_position_rad=self._position - simulated_backlash,
            torque_nm=measured_current * self.SIMULATED_TORQUE_CONSTANT_NM_PER_A,
            notes="SIMULATED DRY RUN; torque and backlash are generated values, not measurements",
        )

    def stop(self) -> None:
        self._command = Command(self._position, 0.0, 0.0)
        self._enabled = False

    def close(self) -> None:
        self.stop()


class RobStride04HardwareBackend:
    """Deliberately incomplete boundary for the future verified CAN adapter."""

    MANUAL_URL = "https://www.robstride.com/assets/product_manual_robStride04-37549d59.pdf"

    def __init__(self, firmware_revision: str) -> None:
        self.firmware_revision = firmware_revision
        raise NotImplementedError(
            "Hardware mode is blocked. TODO: implement and review the exact RobStride 04 "
            "protocol for the recorded firmware revision using the official manual at "
            f"{self.MANUAL_URL}. Verify captured frames on an isolated bench before enable. "
            "Do not copy CAN IDs or parameter addresses from an unverified community example."
        )

    def enable(self) -> None:
        raise NotImplementedError

    def command(self, command: Command) -> None:
        raise NotImplementedError

    def read(self, now_s: float) -> Telemetry:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


class StopRequested(Exception):
    pass


def clamp_current(requested_a: float, current_limit_a: float) -> tuple[float, bool]:
    limited = max(-current_limit_a, min(current_limit_a, requested_a))
    return limited, not math.isclose(limited, requested_a, rel_tol=0.0, abs_tol=1e-12)


def command_for(profile: str, elapsed_s: float, duration_s: float, current_limit_a: float) -> Command:
    if profile == "step":
        position = 0.0
        if duration_s * 0.25 <= elapsed_s < duration_s * 0.75:
            position = 0.10
        requested_current = current_limit_a * (0.35 if position else -0.10)
        current, _ = clamp_current(requested_current, current_limit_a)
        return Command(position, 0.0, current)
    frequency_hz = 0.25
    phase = 2.0 * math.pi * frequency_hz * elapsed_s
    position = 0.08 * math.sin(phase)
    velocity = 0.08 * 2.0 * math.pi * frequency_hz * math.cos(phase)
    requested_current = current_limit_a * 0.35 * math.sin(phase)
    current, _ = clamp_current(requested_current, current_limit_a)
    return Command(position, velocity, current)


def nonnegative_float(value: str) -> float:
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("value must be nonnegative")
    return number


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return number


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("dry-run", "hardware"), default="dry-run")
    parser.add_argument("--profile", choices=("step", "sine"), default="step")
    parser.add_argument("--duration-s", type=positive_float, default=8.0)
    parser.add_argument("--rate-hz", type=positive_float, default=100.0)
    parser.add_argument(
        "--current-limit-a",
        type=positive_float,
        default=2.0,
        help="Software clamp. The 2 A dry-run default is an ASSUMPTION, not an approved hardware limit.",
    )
    parser.add_argument("--watchdog-s", type=positive_float, default=0.10)
    parser.add_argument("--output", type=Path, default=Path("single_joint_bench_log.csv"))
    parser.add_argument("--permit-id", default="")
    parser.add_argument("--second-person", default="")
    parser.add_argument("--firmware-revision", default="")
    return parser.parse_args(argv)


def validate_hardware_preconditions(args: argparse.Namespace) -> None:
    if args.mode != "hardware":
        return
    missing = []
    if not args.permit_id.strip():
        missing.append("--permit-id")
    if not args.second_person.strip():
        missing.append("--second-person")
    if not args.firmware_revision.strip():
        missing.append("--firmware-revision")
    if missing:
        raise SystemExit("Hardware mode blocked; missing " + ", ".join(missing))


def run(args: argparse.Namespace) -> int:
    validate_hardware_preconditions(args)
    backend: BenchBackend
    if args.mode == "dry-run":
        backend = DryRunBackend()
    else:
        backend = RobStride04HardwareBackend(args.firmware_revision)

    stop_flag = {"requested": False}

    def request_stop(_signum: int, _frame: object) -> None:
        stop_flag["requested"] = True

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    period_s = 1.0 / args.rate_hz
    started = time.monotonic()
    next_tick = started
    last_telemetry_s = started
    row_count = 0
    watchdog_state = "OK"

    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_FIELDS)
        writer.writeheader()
        try:
            backend.enable()
            while True:
                now = time.monotonic()
                elapsed = now - started
                if stop_flag["requested"]:
                    raise StopRequested("operator or process stop requested")
                if elapsed >= args.duration_s:
                    break
                if now < next_tick:
                    time.sleep(min(next_tick - now, period_s))
                    continue
                command = command_for(args.profile, elapsed, args.duration_s, args.current_limit_a)
                clamped_current, clamped = clamp_current(command.current_a, args.current_limit_a)
                command = Command(command.position_rad, command.velocity_rad_s, clamped_current)
                backend.command(command)
                telemetry = backend.read(now)
                last_telemetry_s = time.monotonic()
                if last_telemetry_s - now > args.watchdog_s:
                    watchdog_state = "TRIPPED"
                    raise StopRequested("telemetry watchdog expired")
                note_parts = [telemetry.notes]
                if clamped:
                    note_parts.append("software current clamp applied")
                writer.writerow(
                    {
                        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                        "elapsed_s": f"{elapsed:.6f}",
                        "run_mode": args.mode,
                        "profile": args.profile,
                        "command_position_rad": f"{command.position_rad:.9f}",
                        "command_velocity_rad_s": f"{command.velocity_rad_s:.9f}",
                        "command_current_a": f"{command.current_a:.9f}",
                        "measured_position_rad": f"{telemetry.position_rad:.9f}",
                        "measured_velocity_rad_s": f"{telemetry.velocity_rad_s:.9f}",
                        "measured_current_a": f"{telemetry.current_a:.9f}",
                        "temperature_c": f"{telemetry.temperature_c:.6f}",
                        "motor_position_rad": "" if telemetry.motor_position_rad is None else f"{telemetry.motor_position_rad:.9f}",
                        "output_position_rad": "" if telemetry.output_position_rad is None else f"{telemetry.output_position_rad:.9f}",
                        "measured_torque_nm": "" if telemetry.torque_nm is None else f"{telemetry.torque_nm:.9f}",
                        "watchdog_state": watchdog_state,
                        "notes": "; ".join(part for part in note_parts if part),
                    }
                )
                handle.flush()
                row_count += 1
                next_tick += period_s
                if next_tick < time.monotonic() - period_s:
                    next_tick = time.monotonic()
        except StopRequested as exc:
            watchdog_state = "TRIPPED" if "watchdog" in str(exc) else "STOPPED"
            print(f"STOP: {exc}", file=sys.stderr)
        finally:
            try:
                backend.stop()
            finally:
                backend.close()

    print(
        f"wrote {row_count} rows to {args.output} | mode={args.mode} | "
        f"current_limit={args.current_limit_a:g} A | watchdog={watchdog_state}"
    )
    if args.mode == "dry-run":
        print("DRY RUN ONLY: all telemetry is simulated and is not robot evidence.")
    return 0 if watchdog_state in ("OK", "STOPPED") else 2


def main(argv: list[str] | None = None) -> int:
    return run(parse_args(argv))


if __name__ == "__main__":
    raise SystemExit(main())
