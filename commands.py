#!/usr/bin/env python3
"""
Command-line interface for seeding the database.
Usage: python command.py --fill
"""

import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Seed the database with content from data files.")
    parser.add_argument(
        "--fill",
        action="store_true",
        help="Fill the database with data from data/ directory",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually running the seeder",
    )

    args = parser.parse_args()

    if args.dry_run:
        print("Dry run mode - would run: python scripts/seed_data.py")
        sys.exit(0)

    if not args.fill:
        parser.print_help()
        sys.exit(1)

    script_path = os.path.join(os.path.dirname(__file__), "scripts", "seed_data.py")

    if not os.path.exists(script_path):
        print(f"Error: Script not found at {script_path}")
        sys.exit(1)

    print("Starting database seeding...")
    print(f"Running: python {script_path}")
    print("-" * 50)

    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))

        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            env=env,
            check=True,
        )

        print("-" * 50)
        print("Database seeding completed successfully!")
        sys.exit(result.returncode)

    except subprocess.CalledProcessError as e:
        print("-" * 50)
        print(f"Error: Database seeding failed with code {e.returncode}")
        sys.exit(e.returncode)
    except Exception as e:
        print("-" * 50)
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
