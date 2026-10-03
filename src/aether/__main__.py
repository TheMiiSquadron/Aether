"""Command-line entry point for the Aether Foundation runtime."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence

from aether.config import RuntimeConfig
from aether.logging import configure_logging
from aether.runtime import AetherRuntime


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="aether",
        description="Start the minimal Aether Foundation runtime.",
    )
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Runtime log level.",
    )
    args = parser.parse_args(argv)

    configure_logging(args.log_level)

    runtime = AetherRuntime(RuntimeConfig(log_level=args.log_level))
    startup_report = runtime.start()
    print(json.dumps(startup_report, indent=2, sort_keys=True))
    runtime.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
