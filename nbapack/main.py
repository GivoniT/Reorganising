"""Entry point for running nbapack as a module."""
from __future__ import annotations
from .cli.main import main as cli_main


def main():
    return cli_main()


if __name__ == "__main__":
    main()
