#!/usr/bin/env python3
"""
High Lonesome 100 Lottery Monte Carlo Simulator

Simulates the lottery drawing process to calculate probabilities of selection
based on ticket count.
"""

import argparse
import csv
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Entrant:
    name: str
    tickets: float


def load_entrants(filepath: str) -> list[Entrant]:
    """Load entrants from a CSV file."""
    entrants = []
    with open(filepath, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            # Skip empty lines and comments
            if not row or row[0].strip().startswith("#"):
                continue
            # Skip header row (check second column since it must be numeric)
            if len(row) > 1 and row[1].strip().lower() == "tickets":
                continue
            name = row[0].strip()
            tickets = float(row[1].strip())
            if tickets < 1:
                raise ValueError(f"Entrant {name} must have at least 1 ticket")
            entrants.append(Entrant(name=name, tickets=tickets))
    return entrants


def run_single_lottery(entrants: list[Entrant], main_spots: int, waitlist_spots: int) -> dict:
    """
    Run a single lottery drawing using weighted random selection.

    Returns a dict mapping ticket count to list of (position, is_main) tuples.
    Position is 1-indexed draw order.
    """
    # Track results by ticket count
    results = defaultdict(list)

    # Create list of remaining entrants and their weights (tickets)
    remaining = list(entrants)
    position = 0
    total_spots = main_spots + waitlist_spots

    while position < total_spots and remaining:
        # Get weights for remaining entrants
        weights = [e.tickets for e in remaining]

        # Draw one entrant using weighted selection
        selected = random.choices(remaining, weights=weights, k=1)[0]

        # This person is selected
        position += 1
        is_main = position <= main_spots

        # Record result by their ticket count
        results[selected.tickets].append((position, is_main))

        # Remove this person from remaining pool
        remaining = [e for e in remaining if e.name != selected.name]

    return results


def run_simulation(
    entrants: list[Entrant],
    iterations: int,
    main_spots: int,
    waitlist_spots: int,
) -> dict:
    """
    Run Monte Carlo simulation.

    Returns statistics organized by ticket count.
    """

    # Count entrants by ticket count
    ticket_counts = defaultdict(int)
    for e in entrants:
        ticket_counts[e.tickets] += 1

    # Track selections: ticket_count -> {main: count, waitlist: count}
    stats = {
        tc: {"main": 0, "waitlist": 0, "total_entrants": count}
        for tc, count in ticket_counts.items()
    }

    for i in range(iterations):
        if (i + 1) % 1000 == 0:
            print(f"  Iteration {i + 1:,}/{iterations:,}...")

        results = run_single_lottery(entrants, main_spots, waitlist_spots)

        for ticket_count, selections in results.items():
            for position, is_main in selections:
                if is_main:
                    stats[ticket_count]["main"] += 1
                else:
                    stats[ticket_count]["waitlist"] += 1

    return stats


def print_results(stats: dict, iterations: int, main_spots: int, waitlist_spots: int):
    """Print formatted results."""
    print("\n" + "=" * 80)
    print("HIGH LONESOME 100 LOTTERY SIMULATION RESULTS")
    print("=" * 80)
    print(f"\nSimulation Parameters:")
    print(f"  Iterations:      {iterations:,}")
    print(f"  Main spots:      {main_spots}")
    print(f"  Waitlist spots:  {waitlist_spots}")
    print(f"  Total spots:     {main_spots + waitlist_spots}")

    print("\n" + "-" * 80)
    print(f"{'Tickets':<10} {'Entrants':<10} {'Main %':<12} {'Waitlist %':<12} {'Either %':<12}")
    print("-" * 80)

    for ticket_count in sorted(stats.keys()):
        data = stats[ticket_count]
        total_entrants = data["total_entrants"]
        total_chances = total_entrants * iterations

        main_pct = (data["main"] / total_chances) * 100
        waitlist_pct_result = (data["waitlist"] / total_chances) * 100
        either_pct = ((data["main"] + data["waitlist"]) / total_chances) * 100

        print(f"{ticket_count:<10} {total_entrants:<10} {main_pct:<12.2f} {waitlist_pct_result:<12.2f} {either_pct:<12.2f}")

    print("-" * 80)

    # Summary statistics
    total_entrants = sum(d["total_entrants"] for d in stats.values())
    total_tickets = sum(tc * d["total_entrants"] for tc, d in stats.items())
    print(f"\nTotal entrants: {total_entrants}")
    print(f"Total tickets in pool: {total_tickets}")


def main():
    parser = argparse.ArgumentParser(
        description="Monte Carlo simulator for High Lonesome 100 lottery"
    )
    parser.add_argument(
        "-f", "--file",
        default="entrants.csv",
        help="Path to entrants CSV file (default: entrants.csv)"
    )
    parser.add_argument(
        "-i", "--iterations",
        type=int,
        default=10000,
        help="Number of simulation iterations (default: 10000)"
    )
    parser.add_argument(
        "-m", "--main-spots",
        type=int,
        default=125,
        help="Number of main lottery spots (default: 125, per HL100 gender pool)"
    )
    parser.add_argument(
        "-w", "--waitlist-spots",
        type=int,
        default=125,
        help="Number of waitlist spots (default: 125, per HL100 gender pool)"
    )
    parser.add_argument(
        "-s", "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (optional)"
    )

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    # Load entrants
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"Error: Entrants file not found: {filepath}")
        return 1

    print(f"Loading entrants from: {filepath}")
    entrants = load_entrants(filepath)
    print(f"Loaded {len(entrants)} entrants")

    # Run simulation
    print(f"\nRunning {args.iterations:,} iterations...")
    stats = run_simulation(
        entrants=entrants,
        iterations=args.iterations,
        main_spots=args.main_spots,
        waitlist_spots=args.waitlist_spots,
    )

    # Print results
    print_results(stats, args.iterations, args.main_spots, args.waitlist_spots)

    return 0


if __name__ == "__main__":
    exit(main())
