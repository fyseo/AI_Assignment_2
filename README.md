# Adversarial Search in a Network Security Game

**Course:** Artificial Intelligence — Assignment 2

## Overview

This project models a two-player, zero-sum cybersecurity game between an
**Attacker** (Minimizer) and a **Defender** (Maximizer) on a 10-host enterprise
network (`H0`–`H9`). Starting from the Internet entry point (`H0`), the
Attacker attempts to compromise connected machines and exfiltrate the
crown-jewels database on `H5`. The Defender uses a limited budget to patch,
isolate, or restore hosts.

The repository implements the game environment and compares:

- Full-depth Minimax
- Depth-limited Minimax (`depth = 3`)
- Full-depth Alpha-Beta Pruning
- Depth-limited Alpha-Beta Pruning (`depth = 3`)

## Project Structure

```text
.
├── game.py          # Task 1: Game model, legal moves, state updates, and utility
├── algorithms.py    # Task 2: Minimax, Alpha-Beta, heuristic evaluation, and move ordering
├── main.ipynb       # Task 1 demonstrations and Task 2 algorithm comparison
└── README.md        # Project documentation and AI assistance disclosure
```

## Requirements and Installation

The game model and search algorithms use only the Python 3 Standard Library.
The notebook requires Python 3.8 or later and Jupyter Notebook, JupyterLab, or
VS Code with the Jupyter extension.

Clone the repository:

```bash
git clone https://github.com/fyseo/AI_Assignment_2.git
cd AI_Assignment_2
```

If Jupyter is not installed:

```bash
pip install notebook
```

## How to Run

### Notebook

Open `main.ipynb` in VS Code or launch it with:

```bash
jupyter notebook main.ipynb
```

Run the cells from top to bottom. The notebook includes:

1. **Task 1:** Three test cases covering legal actions, isolation, budget
   exhaustion, patching, zero-day attacks, restoration, exfiltration, utility,
   and terminal conditions.
2. **Task 2:** Full-depth and depth-limited Minimax and Alpha-Beta searches
   from the initial state, including runtime, expanded nodes, pruned nodes,
   selected actions, and returned values.

Full-depth Minimax explores a large search tree and may take several minutes
to finish. Full-depth Alpha-Beta produces the same exact result while usually
expanding substantially fewer nodes.

### Python CLI

The algorithms can also be run directly from a terminal:

```bash
python -c "from game import GameState; from algorithms import alpha_beta; print(alpha_beta(GameState(), depth=3))"
```

## Summary of Experimental Results

The following results were recorded from the initial state at ply 0:

| Algorithm | Search Depth | Best Action | Returned Value | Expanded Nodes | Pruned Nodes | Runtime (s) |
| :--- | :--- | :--- | ---: | ---: | ---: | ---: |
| **Minimax** | Full (10 plies) | `('Exploit', 'H1')` | `-44` | 2,402,797 | 0 | 175.412958 |
| **Depth-Limited Minimax** | 3 plies | `('Exploit', 'H1')` | `-20` | 61 | 0 | 0.008497 |
| **Alpha-Beta Pruning** | Full (10 plies) | `('Exploit', 'H1')` | `-44` | 14,858 | 13,519 | 0.652546 |
| **Depth-Limited Alpha-Beta** | 3 plies | `('Exploit', 'H1')` | `-20` | 28 | 81 | 0.001688 |

Runtime values are representative measurements from one run and may vary
depending on hardware, Python version, and system load. Node counts can also
change if the action-ordering strategy changes.

## AI Assistant and Outside Code Disclosure

In accordance with the assignment submission guidelines:

- **Outside Code:** No external third-party libraries or pre-existing game
  engines were used. The game rules and search algorithms were implemented
  from scratch using Python's built-in modules and course lecture materials.
- **AI Assistant Usage:** An AI assistant was used during development to help
  refine comments, structure the Task 1 and Task 2 notebook demonstrations,
  format the Markdown sections and comparison tables, and prepare this
  README.
