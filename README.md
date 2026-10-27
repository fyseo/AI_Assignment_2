# Adversarial Search in a Network Security Game

**Course:** Artificial Intelligence — Assignment 2

## Overview

This project models a two-player, zero-sum turn-based cybersecurity game between an **Attacker** (Minimizer) and a **Defender** (Maximizer) on a 10-host enterprise network (`H0`–`H9`). Starting from the Internet entry point (`H0`), the Attacker attempts to compromise connected machines and exfiltrate the crown jewels database on `H5`, while the Defender allocates a limited defence budget to patch, isolate, or restore hosts.

The repository implements the complete game environment alongside three adversarial search algorithms to select optimal actions:
- **Minimax (Full Depth)**
- **Depth-Limited Minimax (`depth = 3`)**
- **Alpha-Beta Pruning (Full Depth & `depth = 3`)**

## Project Structure

```text
.
├── game.py          # Task 1: Host and GameState classes (network topology, legal moves, state updates, utility)
├── algorithms.py    # Task 2: Minimax, Depth-Limited Minimax, Alpha-Beta Pruning, heuristic evaluation, and move ordering
├── main.ipynb       # Main Jupyter Notebook running Task 1 test cases and Task 2 algorithm comparisons
└── README.md        # Project documentation, setup instructions, and AI assistance disclosure
```

## Requirements & Installation

The core game model (`game.py`) and search algorithms (`algorithms.py`) rely **exclusively on the Python 3 Standard Library** (`copy`, `math`, `time`), so no external packages are required to import or run the modules.

To run the interactive notebook (`main.ipynb`), you only need:
- **Python 3.8+**
- **Jupyter Notebook / JupyterLab** (or VS Code with the Jupyter extension)

### Setup

1. Clone the repository (or download the project folder):
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```
2. *(Optional)* If you do not have Jupyter installed:
   ```bash
   pip install notebook
   ```

## How to Run

### Option 1: Using VS Code or Jupyter Notebook (Recommended)
1. Open the project folder in **VS Code** or launch Jupyter from your terminal:
   ```bash
   jupyter notebook main.ipynb
   ```
2. Run all cells from top to bottom (**Run All**).
   - **Task 1 Cells:** Initialize the 10-host network and execute the three deliverable test cases:
     1. *Test Case 1:* Legal moves, host isolation, budget exhaustion, and verification of the Section 2.6 Worked Example (`U = -30`).
     2. *Test Case 2:* Patching (`Patch`), Zero-Day bypass (`ZeroDay`), and host restoration (`Restore`).
     3. *Test Case 3:* Terminal conditions comparing early Attacker victory (`Exfiltrate` at Ply 7, `U = -244`) against a 10-ply Defender hold (`Isolate H5`, `U = -135`).
   - **Task 2 Cells:** Run Full Minimax, Depth-Limited Minimax (`depth = 3`), Full Alpha-Beta, and Depth-Limited Alpha-Beta (`depth = 3`) from the initial state and print the runtime, expanded nodes, pruned nodes, best action, and utility comparison.

### Option 2: Running Directly from Python CLI
You can also test the game and algorithms directly from a terminal:
```bash
python -c "from game import GameState; from algorithms import alpha_beta; print(alpha_beta(GameState(), depth=3))"
```

## Summary of Experimental Results (Initial State — Ply 0)

| Algorithm | Search Depth | Best Action | Returned Value | Expanded Nodes | Pruned Nodes | Runtime (s) |
| :--- | :--- | :--- | ---: | ---: | ---: | ---: |
| **Minimax** | Full (10 plies) | `('Exploit', 'H1')` | `-44` | 2,402,797 | 0 | ~190.19s |
| **Depth-Limited Minimax** | 3 plies | `('Exploit', 'H1')` | `-20` | 61 | 0 | ~0.0057s |
| **Alpha-Beta Pruning** | Full (10 plies) | `('Exploit', 'H1')` | `-44` | 14,858 | 13,519 | ~0.6615s |
| **Depth-Limited Alpha-Beta** | 3 plies | `('Exploit', 'H1')` | `-20` | 28 | 81 | ~0.0014s |

## AI Assistant & Outside Code Disclosure

In accordance with the assignment submission guidelines:
- **Outside Code:** No external third-party libraries or pre-existing game engines were used; all game rules and search algorithms were implemented from scratch using Python's built-in modules (`copy`, `math`, `time`) and course lecture materials.
- **AI Assistant Usage:** An AI assistant was used during development for:
  - Adding and refining inline code comments across `game.py`, `algorithms.py`, and `main.ipynb`.
  - Generating the structured test case scenarios and print formatting for Task 1 and Task 2 in `main.ipynb`.
  - Writing and formatting the Markdown section headers, comparison tables, conclusion section, and this `README.md`.
