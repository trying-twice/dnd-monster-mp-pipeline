import argparse
from typing import List, Dict, Optional

from pipeline import main_flow

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the D&D monster data pipeline.")
    parser.add_argument(
        "--num-monsters",
        type=int,
        default=5,
        help="The number of random monsters to select."
    )
    args = parser.parse_args()

    main_flow(num_monsters=args.num_monsters)