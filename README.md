# High Lonesome 100 Lottery Simulation

A Monte Carlo simulator to calculate selection probabilities in a weighted lottery system based on ticket counts. Designed for the High Lonesome 100 ultramarathon race lottery where participants earn tickets based on prior unsuccessful lottery entries.

## Historical Lottery Results

Simulation results from past lottery cycles are archived here for reference:

### 2026
- [Men's Lottery Results](historical_lottery_results/2026/mens/lottery_simulation_96_main_125_waitlist_10000_iterations.txt) - 915 entrants, 96 main spots, 125 waitlist spots

## Features

- Weighted lottery simulation where more tickets = better odds
- Configurable number of main spots and waitlist positions
- Runs thousands of iterations for statistical accuracy
- Groups results by ticket count for easy analysis
- Optional random seed for reproducible results
- No external dependencies (standard library only)

## Requirements

- Python 3.7+

## Usage

### Basic Usage

```bash
python3 lottery_simulation.py -f entrants_example.csv
```

### Command-Line Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--file` | `-f` | `entrants.csv` | Path to entrants CSV file |
| `--iterations` | `-i` | `10000` | Number of simulation iterations |
| `--main-spots` | `-m` | `125` | Number of main lottery spots |
| `--waitlist-spots` | `-w` | `125` | Number of waitlist spots |
| `--seed` | `-s` | None | Random seed for reproducibility |

### Examples

```bash
# Run with the example file
python3 lottery_simulation.py -f entrants_example.csv

# Run 50,000 iterations with 120 main spots
python3 lottery_simulation.py -f entrants_example.csv -i 50000 -m 120

# Reproducible results with a fixed seed
python3 lottery_simulation.py -f entrants_example.csv -s 42

# Custom main and waitlist spots
python3 lottery_simulation.py -f entrants_example.csv -m 100 -w 125
```

## Input Format

Create a CSV file with two columns: `name` and `tickets`. Lines starting with `#` are treated as comments.

```csv
# High Lonesome 100 Lottery Entrants
Name,Tickets
John Smith,32
Jane Doe,16
Bob Johnson,8
```

See `entrants_example.csv` for a complete example with 300+ entrants.

## Output

The simulation displays a table showing selection probabilities grouped by ticket count:

```
Tickets    Entrants   Main %       Waitlist %   Either %
45.25      1          100.00       0.00         100.00
32         2          99.85        0.15         100.00
22.63      1          98.50        1.45         99.95
...
2          50         25.30        8.20         33.50

Total entrants: 300
Total tickets in pool: 2500
```

- **Main %**: Probability of being selected for a guaranteed spot
- **Waitlist %**: Probability of being selected for the waitlist
- **Either %**: Combined probability of any selection

## How It Works

1. **Build Pool**: Each entrant's tickets are added to a pool (more tickets = more entries)
2. **Draw**: Randomly select one ticket from the pool
3. **Select**: If the person hasn't been drawn yet, they're selected and all their tickets are removed
4. **Repeat**: Continue until all main and waitlist spots are filled
5. **Aggregate**: Track results across all iterations to calculate probabilities

## High Lonesome 100 Lottery Structure

The actual HL100 lottery has the following structure (as of 2026):

### Entry Cap
- **Total field**: 250 runners

### Discretionary Entries (Non-Lottery)
These spots are allocated outside the lottery:
- **Volunteers**: 5% of cap (~13 spots)
- **Sponsors**: 3% of cap (~8 spots)
- **Race Director**: 3% of cap (~8 spots)
- **Legacy runners**: Up to 6 spots
- **Sawatch 50/50 winners**: Up to 4 spots (male, female, non-binary)
- **Previous year podium finishers**: Up to 9 spots
- **PTRA (Professional Trail Runners)**: 6 spots
- **BIPOC/LGBTQ+ entries**: 4 spots

### Lottery Spots
After discretionary entries (~50 spots), remaining spots (~200) are split evenly between **male** and **female** pools (~100 each).

### Waitlist
Each gender pool has its own waitlist of ~100-125 runners.

### Important Note
Since the HL100 lottery is split into separate male/female pools, you should run this simulation separately for each pool with the appropriate entrants file. The default values (100 main spots, 100 waitlist) reflect a single gender pool.

### Ticket System
- Tickets are earned from previous unsuccessful lottery entries
- Tickets reset to zero after being selected or offered entry from waitlist
- Tickets also reset if you don't apply for 3 consecutive years
- There is no maximum ticket count

## Sources

- [High Lonesome 100 Registration Info](https://www.highlonesome100.com/general-registration-info)
- [HL100 Lottery](https://lottery.highlonesome100.com/)
- [Entry Cap Increase Announcement](https://www.highlonesome100.com/blog/2023/4/28/the-usfs-has-increased-our-entry-cap)
